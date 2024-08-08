import os
import genshin
import enka
import requests

from PIL import Image
from dotenv import load_dotenv
from io import BytesIO
from utils.mats_util import calculate_pic_size, SINGLE_PIC_SIZE


def prepare_player_characters_image(uid: str, characters: list[enka.gi.Character]) -> tuple[str, str]:
    img_name = f"data/out/genshininfo/{uid}_chars.png"
    image_list = []
    for character in characters:
        response = requests.get(character.icon.front)
        image_list.append(Image.open(BytesIO(response.content)))
    image = Image.new("RGBA", calculate_pic_size(characters, 4), color=(0, 0, 0, 0))
    pos_x = 0
    pos_y = 0
    pic_counter = 0
    for pic in image_list:
        image.paste(pic, (pos_x, pos_y))
        pos_x += SINGLE_PIC_SIZE[0]
        if pic_counter >= 4 - 1:
            pos_y += SINGLE_PIC_SIZE[1]
            pos_x = 0
            pic_counter = -1
        pic_counter += 1
    image.save(img_name, quality=100)
    return img_name, f"{uid}_chars.png"


# ----- genshin.py -----
def get_cookies() -> dict:
    load_dotenv()

    ltuid = os.getenv("LTUID")
    ltoken = os.getenv("LTOKEN")
    ltmid = os.getenv("LTMID")

    return {
        "ltuid_v2": int(ltuid),
        "ltoken_v2": ltoken,
        "ltmid_v2": ltmid
    }


def get_genshin_client() -> genshin.Client:
    return genshin.Client(get_cookies(), lang="fr-fr", game=genshin.Game.GENSHIN)


# ----- enka ----
async def get_genshin_player_info(uid: str) -> dict:
    async with enka.GenshinClient(enka.gi.Language.FRENCH) as client:
        response = await client.fetch_showcase(uid)
        res = {
            "icon": response.player.profile_picture_icon.front,
            "nickname": response.player.nickname,
            "signature": response.player.signature,
            "adventure_rank": response.player.level,
            "characters": response.characters
        }
    return res
