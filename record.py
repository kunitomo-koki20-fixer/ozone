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

MONTH = (By.CLASS_NAME, "hasMonthpicker")
SEARCH = (By.CLASS_NAME, "BtnShow")
TIME = 'div_getsuji_grid_SYUKKIN_JIKAN_row'
DATE = 'div_getsuji_grid_NIPPOU_DATE_row'
MESSAGE = (By.ID, "div_sub_message")
PROJECT = (By.ID, "text_project_1")
WORK = (By.ID, "div_sub_editlist_WORK_TIME_row1")
REGISTER = (By.ID, "div_sub_buttons_regist")
OK = (By.XPATH , "//input[@value='ＯＫ']")
CLOSE = (By.ID, "div_sub_buttons_close")

def record(chrome, month, url, project, headless):
    options = webdriver.ChromeOptions()
    options.binary_location = chrome
    if headless : options.add_argument('--headless')
    driver = webdriver.Chrome(options=options, service_log_path="chromedriver.log")

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

        m = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(MONTH))
        m.clear()
        m.send_keys(month)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(SEARCH)).click()
        sleep(0.5)

        i = 1
        while True:
            time_locator = (By.ID, TIME + str(i))
            try:
                working_time =  WebDriverWait(driver, 1).until(EC.presence_of_element_located(time_locator)).find_element_by_tag_name("span")
            except:
                break
            if str(working_time.get_attribute("style")).startswith("color: rgb(255, 0, 0)"):
                date_locator = (By.ID, DATE + str(i))
                date = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(date_locator))
                date.click()
                sleep(0.5)
                if WebDriverWait(driver, 10).until(EC.presence_of_element_located(MESSAGE)).text == "":
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(PROJECT)).send_keys(project)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located(WORK)).find_element_by_tag_name("input").send_keys(working_time.text)
                    sleep(0.5)
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(REGISTER)).click()
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(OK)).click()
                    print(date.text + "の工数入力完了")
                else:
                    print(date.text + "の工数入力はスキップしました。")
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(CLOSE)).click()
            i+=1
    finally:
        print("終了しています...")
        driver.quit()

def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('-c', '--chrome', type=str,default=chrome, help='Chromeのバイナリパス')
    argparser.add_argument('-e', '--email', type=str,default=email, help='ログインするメアド')
    argparser.add_argument('-H', '--headless', action='store_true', help='Chromeを非表示にするかどうか')
    argparser.add_argument('-m', '--month', type=str,default=month, help='記録する月 YYYY/MM')
    argparser.add_argument('-p', '--project', type=str,default=project, help='Project name.')
    argparser.add_argument('-P', '--password', action='store_true', help='パスワードを要求するかどうか')
    argparser.add_argument('-u', '--url', type=str, default=url, help='工数入力ページのURL')
    return argparser.parse_args()

if __name__ == '__main__':
    chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    email = ''
    month = '2021/05'
    project = ''
    pwd = ''
    url = ''

    args = get_option()

    chrome = args.chrome
    email = args.email
    EMAIL = email
    month = args.month
    project = args.project

    if(args.password):
        pwd = getpass('Your password :')
    else:
        pwd = keyring.get_password(LOGINURL, EMAIL)
    PWD = pwd

    url = args.url
    record(chrome,month,url,project,args.headless)
