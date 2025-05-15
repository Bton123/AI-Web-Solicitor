from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from usernames import get_random_username

def simulate_typing(driver, element, text, delay=0.05):
    element.clear()
    for char in text:
        element.send_keys(char)
        time.sleep(delay)

def perform_login(driver, base_username, gender, age, state, max_attempts=5):
    wait = WebDriverWait(driver, 15)

    for attempt in range(max_attempts):
        random_username = get_random_username()

        username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
        simulate_typing(driver, username_input, random_username)
        print(f"🔐 Generated username: {random_username}")

        # Gender
        if gender.lower() != "female":
            try:
                gender_input = driver.find_element(By.XPATH, f'//input[@type="radio" and @value="{gender.lower()}"]')
                driver.execute_script("arguments[0].checked = true;", gender_input)
            except:
                print("⚠️ Gender input not found or already selected.")

        # Age & State
        age_dropdown = wait.until(EC.presence_of_element_located((By.ID, "age")))
        state_dropdown = wait.until(EC.presence_of_element_located((By.ID, "city")))
        driver.execute_script("arguments[0].value = arguments[1];", age_dropdown, age)
        driver.execute_script("arguments[0].value = arguments[1];", state_dropdown, state)
        for el in [age_dropdown, state_dropdown]:
            driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", el)

        # Trigger validators
        driver.execute_script("window.scrollBy(0, 200);")
        ActionChains(driver).move_to_element_with_offset(driver.find_element(By.TAG_NAME, "body"), 10, 10).click().perform()
        time.sleep(0.3)

        # Dispatch input/change/blur events
        driver.execute_script("""
          ['username', 'age', 'city'].forEach(id => {
            const el = document.getElementById(id);
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            el.dispatchEvent(new Event('blur', { bubbles: true }));
          });
        """)

        try:
            # Wait until button is enabled
            wait.until(lambda d: not d.find_element(By.ID, "startChatNow").get_attribute("disabled"))
            start_btn = driver.find_element(By.ID, "startChatNow")
            driver.execute_script("arguments[0].scrollIntoView(true);", start_btn)
            ActionChains(driver).move_to_element(start_btn).click().perform()
            print("✅ Clicked Start Chat Now.")

            # Wait for confirmation that login succeeded
            try:
                WebDriverWait(driver, 8).until(
                    EC.presence_of_element_located((By.ID, "msg"))  # chat screen
                )
                print("✅ Chat UI detected — login successful.")

                # Check for ToS modal
                try:
                    agree_btn = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Agree")]'))
                    )
                    agree_btn.click()
                    print("✅ Clicked ToS agree button.")
                except:
                    print("ℹ️ No ToS modal appeared after start.")

                return  # Login successful

            except:
                print("❌ Chat UI never appeared. Username likely rejected. Retrying...")
                username_input.clear()
                continue

        except:
            print("❌ Start button still disabled. Retrying...")
            username_input.clear()
            continue

    raise Exception("🚫 Login failed after multiple attempts.")
