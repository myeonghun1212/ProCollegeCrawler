from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from parse import *
from html_table_parser import parser_functions as parser
from bs4 import BeautifulSoup
import pandas as pd

def SetEdge():
    # Setup opitons
    option = Options()
    option.add_argument("disable-infobars")
    option.add_argument("disable-extensions")
    # option.add_argument("start-maximized")
    option.add_argument('disable-gpu')
    # option.add_argument('headless')

    # Selenium 4.0 - load webdriver
    try:
        s = Service(EdgeChromiumDriverManager().install())
        browser = webdriver.Edge(service=s, options=option)
        return browser
    except Exception as e:
        print(e)
        return -1
    

def GetValue(item):
    return item.text


def ScrapeProCollage(targetyear, pages = -1):
    colname = ['년도수', '지역', '대학명', '모집시기', '전공명', '모집시기별 입학정원', '주야구분', '전형구분', '전형구분2', '점수산출기준수능', '점수산출기준학생부', '경쟁률', '합격자평균수능', '합격자평균학생부', '합격자최저수능', '합격자최저학생부']
    df = pd.DataFrame(columns=colname)
    driver = SetEdge()
    driver.get("https://www.procollege.kr/web/entrance/webEntrancePreResult.do?")
    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/section/div[2]/form/div[1]/fieldset/div/div/div[1]/button'))).click()
    selectYear = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "sel_1")))
    selectYear = Select(selectYear)
    selectYear.select_by_value(str(targetyear))

    #마지막 페이지 구하기
    lastpage = driver.find_element(By.XPATH, "/html/body/div[1]/section/div[2]/div[2]").find_element(By.CLASS_NAME, "nextAll")
    lastpage = lastpage.get_attribute("onclick")
    lastpage = int(parse("fn_linkPage({}); return false;", lastpage)[0])
    if pages == -1:
        pages = lastpage
    for pagen in range(1, min(lastpage + 1, pages + 1)):
        table = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/section/div[2]/div[1]/div/div/div[1]/table')))
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        table = soup.find("table")

        p = parser.make2d(table)
        tempdf = pd.DataFrame(p[2:], columns=colname[1:])
        tempdf['년도수'] = targetyear
        df = pd.concat([df, tempdf], ignore_index=True)
        driver.execute_script(f"fn_linkPage({pagen + 1}); return false;")
    return df
