import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
from gemini_responder import generate_reply
from navigation import click_random_chat

def wait_for_new_message(driver, previous_messages, timeout=60):
    wait = WebDriverWait(driver, 10)
    message_log = list(previous_messages)
    new_message = None

    for _ in range(timeout):
        time.sleep(1)
        try:
            current = driver.execute_script("""
                const container = document.querySelector('div#message_container');
                if (!container) return [];

                return Array.from(container.querySelectorAll('.incoming_msg, .message'))
                    .map(e => e.innerText.trim())
                    .filter(Boolean);
            """)
        except UnexpectedAlertPresentException:
            try:
                alert = driver.switch_to.alert
                print(f"⚠️ Dismissed alert: {alert.text}")
                alert.accept()
                continue
            except:
                continue

        new_messages = [m for m in current if m not in message_log]
        if new_messages:
            new_message = new_messages[-1]
            message_log.extend(new_messages)
            print(f"🎉 Received reply: {new_message}\n")
            break

    return new_message, message_log

def send_message(driver, text):
    wait = WebDriverWait(driver, 10)

    try:
        typing_box = wait.until(EC.presence_of_element_located((By.ID, "contenteditablediv")))
        if typing_box.get_attribute("contenteditable") == "true":
            driver.execute_script(f"arguments[0].innerText = `{text}`;", typing_box)
            driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", typing_box)
            time.sleep(0.3)

            send_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "msg_send_btn")))
            send_btn.click()
            print(f"✅ Message sent: '{text}'")
        else:
            print("❌ Typing box not editable.")
    except Exception as e:
        print(f"❌ Failed to send message: {e}")

def chat_loop(driver, initial_message="hello!"):
    message_log = []
    attempt = 1

    while True:
        print(f"➡️ Attempt {attempt}")
        click_random_chat(driver)
        time.sleep(1)

        send_message(driver, initial_message)
        message_log.append(initial_message)

        print("⏳ Waiting for reply (60s)...")
        reply, message_log = wait_for_new_message(driver, message_log, timeout=60)

        if not reply:
            print("❌ No reply. Switching chat...")
            attempt += 1
            continue

        while True:
            time.sleep(1.5)  # Slight delay before responding
            chat_history = "\n".join(message_log)
            response = generate_reply(chat_history)

            print(f"🤖 Generated response: {response}")
            print("💬 Sending reply in current chat...")
            send_message(driver, response)
            message_log.append(response)

            print("⏳ Waiting for further reply (90s)...")
            further_reply, message_log = wait_for_new_message(driver, message_log, timeout=90)

            if not further_reply:
                print("❌ No reply in 90 seconds. Moving on.\n")
                break  # Restart new chat loop
