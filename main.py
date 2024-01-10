import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from mongo import MongoDB
db = MongoDB()


# driver = webdriver.Chrome('./driver/chromedriver.exe')
url = 'https://www.google.com'
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

#웹 개발자
jobkorea_url = 'https://www.jobkorea.co.kr/Search/?stext=%EC%9B%B9%20%EA%B0%9C%EB%B0%9C%EC%9E%90&Page_No={}&local=I000%2CB000%2CA090&careerType=2%2C4&jobtype=1&tabType=recruit&Ord=RegDtDesc'
#등록순 
saramin_url = 'https://www.saramin.co.kr/zf_user/search?searchType=search&recruitPage=1&searchword=%EC%9B%B9+%EA%B0%9C%EB%B0%9C%EC%9E%90&loc_mcd=101000%2C102000&loc_cd=109090&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7&job_type=1&panel_type=&search_optional_item=y&search_done=y&panel_count=y&preview=y&recruitSort=reg_dt&recruitPageCount=100&inner_com_type=&show_applied=&quick_apply=&except_read=&ai_head_hunting=n&mainSearch=y'

job_title = ''
job_comp = ''
job_exp = ''
job_edu = ''
# job_type = ''
job_loc = ''
job_duedate = ''
job_keyword = ''

page_size = 10

jobkorea_size_path = "//div[@class='list-default']/ul/li[@class='list-post']"
jobkorea_comp_path = "//*[@id='content']/div/div/div[1]/div/div[2]/div[2]/div/div[1]/ul/li[{}]/div/div[1]/a"
jobkorea_title_path="//*[@id='content']/div/div/div[1]/div/div[2]/div[2]/div/div[1]/ul/li[{}]/div/div[2]/a"
jobkorea_exp_path = "//*[@id='content']/div/div/div[1]/div/div[2]/div[2]/div/div[1]/ul/li[{}]/div/div[2]/p[1]/span[@class='exp']"
jobkorea_edu_path = "//*[@id='content']/div/div/div[1]/div/div[2]/div[2]/div/div[1]/ul/li[{}]/div/div[2]/p[1]/span[@class='edu']"
jobkorea_loc_path = "//*[@id='content']/div/div/div[1]/div/div[2]/div[2]/div/div[1]/ul/li[{}]/div/div[2]/p[1]/span[@class='loc long']"
jobkorea_duedate_path = "//*[@id='content']/div/div/div[1]/div/div[2]/div[2]/div/div[1]/ul/li[{}]/div/div[2]/p[1]/span[@class='date']"

saramin_size_path = "//*[@id='recruit_info_list']/div[1]/div[@class='item_recruit']"
saramin_title_path = "//*[@id='recruit_info_list']/div[1]/div[{}]/div[2]/h2/a/span"


job_list = []

for n in range(1, page_size + 1) :
    newUrl = jobkorea_url.format(n)
    # print(newUrl)
    driver.get(newUrl)

    WebDriverWait(driver, 3).until(
        # presence_of_all_elements_located
        # EC.presence_of_element_located(
        #     (By.XPATH, jobkorea_size_path)
        # )

        EC.presence_of_all_elements_located(
            (By.XPATH, jobkorea_size_path)
        )
    )

    jobkorea_size = driver.find_elements_by_xpath(jobkorea_size_path)

    #n페이지 시작
    for i in range(1, len(jobkorea_size) + 1) :
        try:
            job_comp = driver.find_element_by_xpath(jobkorea_comp_path.format(i)).text
        except:
            job_comp = ''
        
        try:
            job_title = driver.find_element_by_xpath(jobkorea_title_path.format(i)).text
        except:
            job_title = ''
    
        try:
            job_exp = driver.find_element_by_xpath(jobkorea_exp_path.format(i)).text
        except:
            job_exp = ''
        try:
            job_edu = driver.find_element_by_xpath(jobkorea_edu_path.format(i)).text
        except:
            job_edu = ''
        try:
            job_loc = driver.find_element_by_xpath(jobkorea_loc_path.format(i)).text
            
        except:
            job_loc = ''
        try:
            job_duedate = driver.find_element_by_xpath(jobkorea_duedate_path.format(i)).text
            
        except:
            job_duedate = ''
 
        job_item = {
            'job_comp': job_comp,
            'job_title': job_title,
            'job_exp': job_exp,
            'job_edu': job_edu,
            'job_loc': job_loc,
            'job_duedate': job_duedate,
            'add_date': time.time()

        }

        if job_comp != '' and job_title != '':
            job_list.append(job_item)

    #n페이지 종료   
    print(n, '페이지 : ' , len(job_list))
    # driver.



# db.insertList(job_list)
driver.quit()