def convert_discord_id_to_time(discord_id: int):
    return int((int(bin(discord_id)[:-22], 2) + 1420070400000) / 1000)
