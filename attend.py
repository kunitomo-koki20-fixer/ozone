from argparse import ArgumentParser
import chromedriver_binary
from getpass import getpass
import keyring
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


LOGINURL = 'https://login.microsoftonline.com'

EMAILFIELD = (By.ID, "i0116")
PASSWORDFIELD = (By.ID, "i0118")
NEXTBUTTON = (By.ID, "idSIButton9")

ATTEND_BTN = (By.ID, "btn03")

def attend(chrome, url, headless):
    options = webdriver.ChromeOptions()
    options.binary_location = chrome
    if headless : options.add_argument('--headless')
    driver = webdriver.Chrome(options=options, service_log_path="chromedriver.log")

    try:
        driver.get(url)
        print("ログイン中...")
        cur_url = driver.current_url
        if cur_url.startswith(LOGINURL):
            WebDriverWait(driver, 100).until(EC.element_to_be_clickable(EMAILFIELD)).send_keys(EMAIL)
            WebDriverWait(driver, 100).until(EC.element_to_be_clickable(NEXTBUTTON)).click()
            WebDriverWait(driver, 100).until(EC.element_to_be_clickable(PASSWORDFIELD)).send_keys(PWD)
            WebDriverWait(driver, 100).until(EC.element_to_be_clickable(NEXTBUTTON)).click()
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable(NEXTBUTTON)).click()
        print("ログイン成功")

        WebDriverWait(driver, 100).until(EC.presence_of_element_located(ATTEND_BTN)).find_element_by_tag_name("a").click()
        sleep(2)

    finally:
        print("終了しています...")
        driver.quit()

def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('-c', '--chrome', type=str,default=chrome, help='Chromeのバイナリパス')
    argparser.add_argument('-e', '--email', type=str,default=email, help='ログインするメアド')
    argparser.add_argument('-H', '--headless', action='store_true', help='Chromeを非表示にするかどうか')
    argparser.add_argument('-P', '--password', action='store_true', help='パスワードを要求するかどうか')
    argparser.add_argument('-u', '--url', type=str, default=url, help='出勤・退勤ページのURL')
    return argparser.parse_args()

if __name__ == '__main__':
    chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    email = ''
    pwd = ''
    url = ''

    args = get_option()

    chrome = args.chrome
    email = args.email
    EMAIL = email

    if(args.password):
        pwd = getpass('Your password :')
    else:
        pwd = keyring.get_password(LOGINURL, EMAIL)
    PWD = pwd

    url = args.url
    attend(chrome,url,args.headless)
