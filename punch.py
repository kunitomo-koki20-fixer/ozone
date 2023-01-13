from argparse import ArgumentParser
from getpass import getpass
import keyring
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


LOGINURL = 'https://login.microsoftonline.com'

EMAILFIELD = (By.ID, "i0116")
PASSWORDFIELD = (By.ID, "i0118")
NEXTBUTTON = (By.ID, "idSIButton9")

ATTEND_BTN = (By.ID, "btn03")
LEAVE_BTN = (By.ID, "btn04")

def punch(chrome, url, headless, out):
    options = webdriver.ChromeOptions()
    options.binary_location = chrome
    if headless : options.add_argument('--headless')
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        print("ログイン中...")
        cur_url = driver.current_url
        if cur_url.startswith(LOGINURL):
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(EMAILFIELD)).send_keys(EMAIL)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(NEXTBUTTON)).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(PASSWORDFIELD)).send_keys(PWD)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(NEXTBUTTON)).click()
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable(NEXTBUTTON)).click()
        print("ログイン成功")

        if(out):
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(LEAVE_BTN)).find_element(By.TAG_NAME,"a").click()
            sleep(2)
            print("退勤成功")
        else:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(ATTEND_BTN)).find_element(By.TAG_NAME,"a").click()
            sleep(2)
            print("出勤成功")

    finally:
        print("終了しています...")
        driver.quit()

def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('-c', '--chrome', type=str,default=chrome, help='Chromeのバイナリパス')
    argparser.add_argument('-e', '--email', type=str,default=email, help='ログインするメアド')
    argparser.add_argument('-H', '--headless', action='store_true', help='Chromeを非表示にするかどうか')
    argparser.add_argument('-P', '--password', action='store_true', help='パスワードを要求するかどうか')
    argparser.add_argument('-t', '--type', type=str, default='', help='出勤もしくは退勤 ("in" もしくは "out")')
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

    if args.type == 'in':
        punch(chrome,url,args.headless,False)
    elif args.type == 'out':
        punch(chrome,url,args.headless,True)
    else:
        print("出勤もしくは退勤を選択してください")

