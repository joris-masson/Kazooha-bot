import os
from random import shuffle


def give_marqueurs():
    res = []
    img_list = os.listdir("../../../data/commands/admin/give_marqueurs/img")
    shuffle(img_list)
    for participant in [int(img_name[:-4]) for img_name in img_list]:
        for img_name in img_list:
            if participant != int(img_name[:-4]):
                res.append(f"{participant} -> {img_name}")
                img_list.remove(img_name)
    return res


for i in range(1000):
    assert len(give_marqueurs()) == len(os.listdir("../../../data/commands/admin/give_marqueurs/img"))
