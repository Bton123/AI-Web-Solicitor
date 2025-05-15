from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def click_random_chat(driver):
    wait = WebDriverWait(driver, 10)

    # ✅ Corrected class name based on working script
    random_chat = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "new_random")))

    driver.execute_script("arguments[0].scrollIntoView(true);", random_chat)
    time.sleep(0.3)

    ActionChains(driver).move_to_element(random_chat).click().perform()
    print("✅ Clicked Random Chat.")
