from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from login import perform_login
from navigation import click_random_chat
from chat_loop import chat_loop

def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)

if __name__ == "__main__":
    driver = setup_driver()
    driver.get("https://www.chatib.us/")
    perform_login(driver, "dogpetter", "Female", "18", "Massachusetts")

    click_random_chat(driver)
    chat_loop(driver, initial_message="hello!")

    driver.quit()
