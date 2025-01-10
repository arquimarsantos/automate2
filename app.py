from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from datetime import datetime
from threading import Thread
from flask import Flask
import pickle
import time

app = Flask(__name__)

def automate2():
    try:
        options = webdriver.ChromeOptions()
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36'
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-gpu')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless")
        options.add_argument("--start-maximized")
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=options)
        dtime = datetime.now()
        dt_string = dtime.strftime("%d/%m/%Y %H:%M:%S")
        print("Automação iniciada! - ", dt_string)     
        ##gruposwhats.app##
        driver.get("https://gruposwhats.app")
        with open("cookies.pkl", "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        driver.get("https://gruposwhats.app/meus-grupos")
        #time.sleep(3)
        bt_element = driver.find_element(By.XPATH, "//button[contains(@class, 'btn-success') and text()='Impulsionar!']")
        ActionChains(driver).move_to_element(bt_element).click().perform()
        print("Grupo impulsionado em gruposwhats.app - ", dt_string)
        ####
        driver.quit()
        print("Automação #2 concluída com sucesso! - ", dt_string)
    except Exception as e:
        print(e)
        automate2()


@app.route('/')
def index():
    automate2()
    return 'Automação #2 ativada!'


if __name__ == '__main__':
    app.run()
    
