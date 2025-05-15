import random

usernames = [
    "dogpetter", "chatwizard", "nightowl93", "memelord", "catlover22", "lonelybot",
    "sweettalker", "icebreaker", "dreamcatcher", "tacoking", "sassypants", "flirtyfox",
    "wittywhale", "gamerbabe", "bananarider", "vibingnow", "boredhuman", "robotron",
    "crushrush", "emojimaster", "nerdynick", "quietstorm", "wildspark", "firestarter",
    "pinkpanther", "gentlegiant", "blueberryjam", "trollhunter", "missclick", "whoami123",
    "bubblychick", "speakeasy", "mysterio69", "fasttypist", "snackattack", "chatgoblin",
    "cloudtalker", "meowmixx", "kawaiikitten", "coderkid", "nightcrawler", "textualhealer",
    "goodvibes24", "pillowfight", "icequeenxx", "puppywhisper", "randomvoice", "midnightmint",
    "sunnytalks", "gigglesnort", "ghosttype", "sleeplesssoul", "invisibleone", "serialtexter",
    "butterflywave", "theawkward1", "replyguy88", "zingzapper", "sparklepony", "bananahands",
    "lastplace", "talkalottt", "onewordonly", "fastandcurious", "chatattack", "palmtreemagic",
    "openheart007", "whisperwiz", "chatsniper", "yeetfleet", "scrollstopper", "cyberhugz",
    "penguintime", "nachonacho", "superzebra", "tickletap", "lofilass", "frappfrapp", "spoilerqueen",
    "dreambubble", "typefaster", "typeracerpro", "fuzzmonster", "tickleghost", "emojidump",
    "lurkmaster", "lolnope", "seenbutnot", "memethinker", "friendlybot", "midnightshift",
    "notaserialkiller", "readreceipt", "outoftheblue", "quickquokka", "whosawake", "imposturr",
    "wordwizard", "peepthis", "replyplease", "talkytalky", "hearthebeat", "saysomething"
]

def get_random_username():
    base = random.choice(usernames)
    suffix = "".join(random.choices("0123456789", k=3))
    return f"{base}{suffix}"
