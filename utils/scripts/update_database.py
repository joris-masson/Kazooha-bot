import os
import genshin
import asyncio

from dotenv import load_dotenv
from utils.database import open_connection


async def get_genshin_user_info(uid: str) -> genshin.models.PartialGenshinUserStats or None:
    load_dotenv()
    client = genshin.Client(game=genshin.Game.GENSHIN)
    client.set_cookies(ltuid=os.getenv("LAB_LTUID"), ltoken=os.getenv("LAB_LTOKEN"))
    try:
        res = await client.get_partial_genshin_user(int(uid))
        return res
    except genshin.errors.DataNotPublic:
        return None


async def get_honkai_user_info(uid: str) -> genshin.models.HonkaiUserStats or None:
    load_dotenv()
    client = genshin.Client(game=genshin.Game.HONKAI)
    client.set_cookies(ltuid=os.getenv("LAB_LTUID"), ltoken=os.getenv("LAB_LTOKEN"))
    try:
        res = await client.get_honkai_user(int(uid))
        return res
    except genshin.errors.DataNotPublic:
        return None


async def update_all(jeu: str):
    db = open_connection()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM Kazooha.GameUid WHERE game='{jeu}' ORDER BY discordId")
    uids = cursor.fetchall()

    for uid in uids:
        user_id = uid[3]
        infos = await get_honkai_user_info(user_id)
        if infos is not None:
            nickname = infos.info.nickname
            level = infos.info.level
            cursor.execute(f"UPDATE GameUid SET nickname='{nickname}', level='{level}' WHERE uid='{user_id}'")

    db.commit()
    cursor.close()
    db.close()

asyncio.run(update_all("honkai"))
