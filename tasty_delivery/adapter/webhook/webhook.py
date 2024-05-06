from discordwebhook import Discord


def send_webhook(msg):
    discord = Discord(
        url="https://discord.com/api/webhooks/1197712776156696656/Tmy0uQKxMqlYM0L-5Ez2sRyt9FwkMyp0c2fCq_ikQFoPzylIcQF9l0hQ_VfAeaHpKLkH")
    discord.post(content=msg)
