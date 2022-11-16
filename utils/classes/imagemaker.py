from PIL import Image


class ImageMaker:
    def __init__(self, liste_noms: list[str], mode: int):
        self.MAX_COLUMNS = 9
        if mode == 0:
            self.IMAGE_NAME = "data/out/final.png"
        else:
            self.IMAGE_NAME = "data/out/final_w.png"
        self.mode = mode

        self.liste_noms = liste_noms
        self.card_img_list = self.__make_card_img_list()
        self.image = Image.new("RGBA", self.__calculate_pic_size(), color=(0, 0, 0, 0))
        self.__create_final_image()

    def __make_card_img_list(self) -> list[Image]:
        res = []
        if self.mode == 0:
            for name in self.liste_noms:
                res.append(Image.open(f"data/img/persos/{name.lower()}.png"))
        else:
            for name in self.liste_noms:
                res.append(Image.open(f"data/img/weapons/{name.lower()}.png"))
        return res

    def __calculate_height(self) -> int:
        return (int(len(self.liste_noms) / self.MAX_COLUMNS + 1)) * self.card_img_list[0].size[1]

    def __calculate_width(self) -> int:
        res = 0
        pic_counter = 0
        for pic in self.card_img_list:
            if pic_counter > self.MAX_COLUMNS:
                break
            res += pic.size[0]
            pic_counter += 1
        return res

    def __calculate_pic_size(self) -> tuple[int, int]:
        return self.__calculate_width(), self.__calculate_height()

    def __create_final_image(self):
        pos_x = 0
        pos_y = 0
        pic_counter = 0
        for pic in self.card_img_list:
            self.image.paste(pic, (pos_x, pos_y))
            pos_x += self.card_img_list[0].size[0]
            if pic_counter >= self.MAX_COLUMNS:
                pos_y += self.card_img_list[0].size[1]
                pos_x = 0
                pic_counter = -1
            pic_counter += 1

        self.image.save(self.IMAGE_NAME, quality=100)
