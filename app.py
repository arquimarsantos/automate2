from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from datetime import datetime
from flask import Flask
import schedule
import os
import pickle
import time

app = Flask(__name__)

gruposdewhatss_email = "arqqsantos@gmail.com"
gruposdewhatss_pass = "030303$$"

next_gruposwhats = 1
next_grupos_whatss = 1

def now():
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S')

def create_driver():
    options = webdriver.ChromeOptions()
    user_agent = 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Mobile Safari/537.36'
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-gpu')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=options)

def automate_gruposwhats():
    global next_gruposwhats
    driver = None
    try:
        driver = create_driver()
        print("Automação iniciada em 'gruposwhats.app' - ", now())
        driver.get("https://gruposwhats.app")
        if os.path.exists("cookies.pkl"):
            with open("cookies.pkl", "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    driver.add_cookie(cookie)
            print("Cookies carregados com sucesso - ", now())
            driver.get("https://gruposwhats.app/meus-grupos")
        else:
            print("Arquivo de cookies não encontrado. É necessário ter os cookies salvos antes de utilizar a automação. - ", now())
            driver.get("https://gruposwhats.app/meus-grupos")
            driver.quit()
            return
        if next_gruposwhats == 1:
            boost_grupos_whats = '/html/body/section[2]/div/div[3]/div[2]/div/div/form/div/button'
            already_boosted = '/html/body/section[2]/div/div[3]/div[2]/div/div/div[1]/div[1]'
            group_name = "#1"
        else:
            boost_grupos_whats = '/html/body/section[2]/div/div[3]/div[3]/div/div/form/div/button'
            already_boosted = '/html/body/section[2]/div/div[3]/div[3]/div/div/div[1]/div[1]'
            group_name = "#2"
        boost_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, f"{boost_grupos_whats} | {already_boosted}")))
        status_text = boost_element.text.lower()
        is_button = boost_element.tag_name == 'button'
        if is_button and "impulsionado" not in status_text:
            boost_element.click()
            print(f"Impulsionamento {group_name} concluído em 'gruposwhats.app' - ", now())
        else:
            print(f"{group_name} já está impulsionado em 'gruposwhats.app' - ", now())
        next_gruposwhats = 2 if next_gruposwhats == 1 else 1
    except Exception as e:
        print(e)
    finally:
        if driver:
            driver.quit()

def automate_gruposdewhatss():
    global next_grupos_whatss
    driver = None
    try:
        driver = create_driver()
        print("Automação iniciada em 'gruposdewhatss.com.br' - ", now())
        driver.get("https://www.gruposdewhatss.com.br/entrar")
        time.sleep(3)
        driver.find_element(By.XPATH, '/html/body/main/div/div/form/div[1]/input').send_keys(gruposdewhatss_email)
        driver.find_element(By.XPATH, '/html/body/main/div/div/form/div[2]/input').send_keys(gruposdewhatss_pass)
        driver.find_element(By.XPATH, '/html/body/main/div/div/form/button').click()
        time.sleep(3)
        driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div[1]/div/a[4]').click()
        time.sleep(3)
        if next_grupos_whatss == 1:
            boost_grupos_whatss = '/html/body/main/div[2]/div[1]/div[2]/div/div[6]/div[2]/div/div[3]/a[2]'
            group_name = "#1"
        else:
            boost_grupos_whatss = '/html/body/main/div[2]/div[1]/div[2]/div/div[6]/div[3]/div/div[3]/a[2]'
            group_name = "#2"
        boost_grupos_whatss_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, boost_grupos_whatss)))
        classes = (boost_grupos_whatss_btn.get_attribute("class") or "").lower()
        text = (boost_grupos_whatss_btn.text or "").lower()
        disabled_attr = boost_grupos_whatss_btn.get_attribute("disabled")
        if "disabled" in classes or disabled_attr is not None or "aguarde" in text:
            print(f"{group_name} já está impulsionado em 'gruposdewhatss.com.br' - ", now())
        else:
            boost_grupos_whatss_btn.click()
            time.sleep(3)
            driver.find_element(By.XPATH, '/html/body/main/div[2]/div[1]/div[2]/div/div[7]/div/div/div[3]/form/button[1]').click()
            print(f"Impulsionamento {group_name} concluído em 'gruposdewhatss.com.br' - ", now())
        next_grupos_whatss = 2 if next_grupos_whatss == 1 else 1
    except Exception as e:
        print(e)
    finally:
        if driver:
            driver.quit()

def start_schedule():
    schedule.every(1).hours.do(automate_gruposwhats)
    schedule.every(1).hours.do(automate_gruposdewhatss)
    while True:
        schedule.run_pending()
        time.sleep(1)

print("Script iniciado com sucesso! - ", now())

start_schedule()

@app.route('/')
def index():
    return 'Automação ativada!'
    
if __name__ == '__main__':
    app.run()
    
