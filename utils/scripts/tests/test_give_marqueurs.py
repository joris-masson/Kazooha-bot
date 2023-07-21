import os
from random import shuffle


def give_marqueurs(img_list: list[str]) -> dict[int, int]:
    res = {}
    while len(res) != len(img_list):
        ze_list = img_list.copy()
        shuffle(ze_list)
        for participant in [int(img_name[:-4]) for img_name in img_list]:
            for img_name in ze_list:
                act_img = int(img_name[:-4])
                if participant != act_img and check_if_inversion(participant, act_img, res):
                    res[participant] = act_img
                    ze_list.remove(img_name)
                    break
    return res


def check_if_inversion(participant: int, img_name: int, res_dict: dict[int, int]) -> bool:
    for id_participant in res_dict:
        if img_name == id_participant and res_dict[id_participant] == participant:
            return False
    return True


def test_res(res_dict: dict[int, int]) -> bool:
    ok = True
    for participant_id in res_dict:
        if participant_id == res_dict[participant_id]:
            ok = False
            break
    return ok and len(give_marqueurs(os.listdir("../../../data/commands/admin/give_marqueurs/img"))) == len(os.listdir("../../../data/commands/admin/give_marqueurs/img"))


for i in range(100):
    res = give_marqueurs(os.listdir("../../../data/commands/admin/give_marqueurs/img"))
    assert test_res(res)
    print(res)
