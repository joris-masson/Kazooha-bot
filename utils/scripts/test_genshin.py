import os
import genshin
import asyncio

from dotenv import load_dotenv

load_dotenv()

async def claim_daily(client: genshin.Client) -> None:
    try:
        reward = await client.claim_daily_reward()
        async for reward in client.claimed_rewards():
            print(f"{reward.time} - {reward.amount}x {reward.name}")
    except genshin.AlreadyClaimed:
        print("Daily reward already claimed")
    else:
        print(f"Claimed {reward.amount}x {reward.name}")


async def get_username(client: genshin.Client):
    res = await client.get_partial_genshin_user(702750106)
    print(res.info)

client = genshin.Client(game=genshin.Game.GENSHIN)
client.set_cookies(ltuid=os.getenv("LAB_LTUID"), ltoken=os.getenv("LAB_LTOKEN"))

asyncio.run(get_username(client))
