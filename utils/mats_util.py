from interactions import Embed, EmbedAttachment, File, Timestamp
from math import ceil
from PIL import Image
from datetime import datetime
from utils.util import open_db_connection, log


MAX_COLUMNS = 6
SINGLE_PIC_SIZE = (256, 256)


def get_today_mats(chars: bool) -> list[tuple[str, str]]:
    db = open_db_connection()
    cursor = db.cursor()

    day = datetime.now().weekday()
    query = f"SELECT name, region FROM Kazooha.Material WHERE utility='{'Personnage' if chars else 'Arme'}'"

    match day:
        case 0 | 3:
            query += " and day='Lundi'"
        case 1 | 4:
            query += " and day='Mardi'"
        case 2 | 5:
            query += " and day='Mercredi'"

    cursor.execute(query)
    res = cursor.fetchall()

    cursor.close()
    db.close()

    return res


def get_today_farmable(chars: bool) -> dict[str:list[str]]:
    # mats[0] → nom
    res = {}

    db = open_db_connection()
    cursor = db.cursor()

    query = f"SELECT name FROM Kazooha.{'Character' if chars else 'Weapon'} WHERE material=%s and beta=0 ORDER BY id"
    for mat in get_today_mats(chars):
        cursor.execute(query, (mat[0], ))
        chars = cursor.fetchall()

        region = mat[1]

        if region not in res.keys():
            res[region] = []
        for char in chars:
            res[region].append(char[0])

    cursor.close()
    db.close()

    return res


def generate_embeds(chars: bool) -> tuple[list[Embed], list[File]]:
    elements = get_today_farmable(chars)
    res = ([], [])

    for region in elements:
        generate_images(region, elements[region], chars)
        region_image = File(f"data/img/regions/{region}.png")
        image = File(f"data/out/givemats/mats_{'chars' if chars else 'weaps'}_{region.lower()}.png")
        embed = Embed(title=region, timestamp=Timestamp.fromtimestamp(datetime.now().timestamp()))
        embed.set_thumbnail(f"attachment://{region}.png")
        embed.set_image(f"attachment://mats_{'chars' if chars else 'weaps'}_{region.lower()}.png")
        res[0].append(embed)
        res[1].append(region_image)
        res[1].append(image)

    return res


def generate_images(region: str, elements: list[str], chars: bool) -> None:
    log("IMAGE", f"Génération de l'image des matériaux de la région {region}")
    image = Image.new("RGBA", calculate_pic_size(elements), color=(0, 0, 0, 0))
    image_list = get_image_list(elements, chars)
    pos_x = 0
    pos_y = 0
    pic_counter = 0
    for pic in image_list:
        image.paste(pic, (pos_x, pos_y))
        pos_x += SINGLE_PIC_SIZE[0]
        if pic_counter >= MAX_COLUMNS - 1:
            pos_y += SINGLE_PIC_SIZE[1]
            pos_x = 0
            pic_counter = -1
        pic_counter += 1
    image.save(f"data/out/givemats/mats_{'chars' if chars else 'weaps'}_{region.lower()}.png", quality=100)


def calculate_pic_size(elements: list[str]) -> tuple[int, int]:
    width = MAX_COLUMNS * SINGLE_PIC_SIZE[0]
    height = ceil(len(elements) / MAX_COLUMNS) * SINGLE_PIC_SIZE[1]
    return width, height


def get_image_list(elements: list[str], chars: bool) -> list[Image]:
    res = []
    directory = "persos" if chars else "weapons"
    for name in elements:
        res.append(Image.open(f"data/img/{directory}/{name}.png"))
    return res
