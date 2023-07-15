from PIL import Image
from utils.database import open_connection
from math import ceil


class MatsImageMaker:
    def __init__(self, days: list[str]):
        self.MAX_COLUMNS = 12
        self.SINGLE_PIC_SIZE = (256, 256)

        self.days = days
        self.weapons = self.__get_weapons()
        self.chars = self.__get_chars()

    def __make_weapons(self):
        image = Image.new("RGBA", self.__calculate_pic_size(self.weapons), color=(0, 0, 0, 0))
        image_list = self.__get_weapons_image_list()
        pos_x = 0
        pos_y = 0
        pic_counter = 0
        for pic in image_list:
            image.paste(pic, (pos_x, pos_y))
            pos_x += self.SINGLE_PIC_SIZE[0]
            if pic_counter >= self.MAX_COLUMNS - 1:
                pos_y += self.SINGLE_PIC_SIZE[1]
                pos_x = 0
                pic_counter = -1
            pic_counter += 1
        image.save("data/out/mats_weapons.png", quality=100)

    def __make_chars(self):
        image = Image.new("RGBA", self.__calculate_pic_size(self.chars), color=(0, 0, 0, 0))
        image_list = self.__get_chars_image_list()
        pos_x = 0
        pos_y = 0
        pic_counter = 0
        for pic in image_list:
            image.paste(pic, (pos_x, pos_y))
            pos_x += self.SINGLE_PIC_SIZE[0]
            if pic_counter >= self.MAX_COLUMNS - 1:
                pos_y += self.SINGLE_PIC_SIZE[1]
                pos_x = 0
                pic_counter = -1
            pic_counter += 1
        image.save("data/out/mats_chars.png", quality=100)

    def make(self):
        self.__make_weapons()
        self.__make_chars()

    def __get_weapons(self) -> list[tuple[str, str]]:
        res = []
        db = open_connection()
        cursor = db.cursor()
        for day in self.days:
            cursor.execute(f"SELECT name, dungeon FROM Weapon WHERE farmableDay='{day}' ORDER BY dungeon")
            for name, dungeon in cursor.fetchall():
                res.append((name, dungeon))
        cursor.execute("SELECT name, dungeon FROM Weapon WHERE farmableDay='All'")
        for name, dungeon in cursor.fetchall():
            res.append((name, dungeon))
        return res

    def __get_chars(self) -> list[tuple[str, str]]:
        res = []
        db = open_connection()
        cursor = db.cursor()
        for day in self.days:
            cursor.execute(f"SELECT name, dungeon FROM `Character` WHERE farmableDay='{day}' ORDER BY dungeon")
            for name, dungeon in cursor.fetchall():
                res.append((name, dungeon))
        cursor.execute("SELECT name, dungeon FROM `Character` WHERE farmableDay='All'")
        for name, dungeon in cursor.fetchall():
            res.append((name, dungeon))
        return res

    def __get_weapons_image_list(self) -> list[Image]:
        res = []
        for name, dungeon in self.weapons:
            res.append(Image.open(f"data/img/weapons/{name}.png"))
        return res

    def __get_chars_image_list(self) -> list[Image]:
        res = []
        for name, dungeon in self.chars:
            res.append(Image.open(f"data/img/persos/{name}.png"))
        return res

    def __calculate_pic_size(self, elements: list[tuple[str, str]]) -> tuple[int, int]:
        width = self.MAX_COLUMNS * self.SINGLE_PIC_SIZE[0]
        height = ceil(len(elements) / self.MAX_COLUMNS) * self.SINGLE_PIC_SIZE[1]
        return width, height
