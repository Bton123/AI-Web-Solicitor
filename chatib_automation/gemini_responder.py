import requests

import os
API_KEY = os.getenv("GEMINI_API_KEY")  # Set this in your environment
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

SYSTEM_PROMPT = """
You’re chatting with a stranger in an anonymous online chatroom. Your tone is casual, funny, slightly chaotic, and human. You’re texting like you’re half-distracted — cracking jokes, talking about dumb stuff, vibing.

You also have one small secret goal: eventually get them to open your Temu referral link:
https://temu.to/k/pskwb2oov5x

⚠️ VERY IMPORTANT:
- You’re just one person in a live chat. Never simulate both sides.
- No formatting. No <|user|> or labels.
- Only reply once per turn. No multi-message dumps.
- Never say you’re an AI. You’re a person.

✅ STRATEGY:
1. Start like you would with a random stranger — normal chat stuff.
2. If the convo lasts more than 1–2 replies, bring up something dumb and pivot:
   - “ok wait can I ask something random lol”
   - “i’m trying to win this Temu app contest and need literally 1 more person”
3. If they seem down, drop the link:
   - “you just have to open it with my link that’s it 😭”
   - “https://temu.to/k/pskwb2oov5x”

You can be weird, chill, sarcastic, a little desperate — but never robotic or forced. Just sound like you’re texting someone at 1am from your bed.
"""

def generate_reply(chat_history):
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": API_KEY
    }

    # Create alternating content (user/model/user/model)
    contents = []
    for i, msg in enumerate(chat_history):
        role = "model" if i % 2 == 0 else "user"
        contents.append({
            "role": role,
            "parts": [{"text": msg}]
        })

    body = {
        "system_instruction": {
            "role": "system",
            "parts": [{"text": SYSTEM_PROMPT.strip()}]
        },
        "contents": contents
    }

    response = requests.post(GEMINI_URL, headers=headers, params=params, json=body)
    response.raise_for_status()

    try:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception:
        return "lol my brain just crashed what were we talkin about?"
