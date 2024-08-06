import os
import genshin

from dotenv import load_dotenv


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

