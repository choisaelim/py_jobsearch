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

jobkorea_url = 'https://www.jobkorea.co.kr/Search/?stext=%EC%9B%B9%20%EA%B0%9C%EB%B0%9C%EC%9E%90&Page_No=1&local=I000%2CB000%2CA090&careerType=2%2C4&jobtype=1&tabType=recruit&Ord=RegDtDesc'
saramin_url = 'https://www.saramin.co.kr/zf_user/search?searchType=search&recruitPage=1&searchword=%EC%9B%B9+%EA%B0%9C%EB%B0%9C%EC%9E%90&loc_mcd=101000%2C102000&loc_cd=109090&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7&job_type=1&panel_type=&search_optional_item=y&search_done=y&panel_count=y&preview=y&recruitSort=reg_dt&recruitPageCount=100&inner_com_type=&show_applied=&quick_apply=&except_read=&ai_head_hunting=n&mainSearch=y'

#웹 개발자
jobkorea_url = 'https://www.jobkorea.co.kr/Search/?stext=%EC%9B%B9%20%EA%B0%9C%EB%B0%9C%EC%9E%90&Page_No={}&local=I000%2CB000%2CA090&careerType=2%2C4&jobtype=1&tabType=recruit&Ord=RegDtDesc'
#등록순 
saramin_url = 'https://www.saramin.co.kr/zf_user/search?searchType=search&recruitPage={}&searchword=%EC%9B%B9+%EA%B0%9C%EB%B0%9C%EC%9E%90&loc_mcd=101000%2C102000&loc_cd=109090&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7&job_type=1&panel_type=&search_optional_item=y&search_done=y&panel_count=y&preview=y&recruitSort=reg_dt&recruitPageCount=100&inner_com_type=&show_applied=&quick_apply=&except_read=&ai_head_hunting=n&mainSearch=y'

job_title = ''
job_comp = ''
job_exp = ''
job_edu = ''
# job_type = ''
job_loc = ''
job_duedate = ''
job_keyword = ''

#*20
jobkorea_page_size = 50
#*100
saramin_page_size = 10

# jobkorea_page_size = 10
# saramin_page_size = 2

jobkorea_size_path = "//div[@class='list-default']/ul/li[@class='list-post']"
jobkorea_comp_path = "//*[@id='content']/div/div/div[1]/div/div[2]/div[2]/div/div[1]/ul/li[{}]/div/div[1]/a"
jobkorea_title_path="//*[@id='content']/div/div/div[1]/div/div[2]/div[2]/div/div[1]/ul/li[{}]/div/div[2]/a"
jobkorea_exp_path = "//*[@id='content']/div/div/div[1]/div/div[2]/div[2]/div/div[1]/ul/li[{}]/div/div[2]/p[1]/span[@class='exp']"
jobkorea_edu_path = "//*[@id='content']/div/div/div[1]/div/div[2]/div[2]/div/div[1]/ul/li[{}]/div/div[2]/p[1]/span[@class='edu']"
jobkorea_loc_path = "//*[@id='content']/div/div/div[1]/div/div[2]/div[2]/div/div[1]/ul/li[{}]/div/div[2]/p[1]/span[@class='loc long']"
jobkorea_duedate_path = "//*[@id='content']/div/div/div[1]/div/div[2]/div[2]/div/div[1]/ul/li[{}]/div/div[2]/p[1]/span[@class='date']"

saramin_size_path = "//*[@id='recruit_info_list']/div[@class='content']/div[@class='item_recruit']"
saramin_title_path = "//*[@id='recruit_info_list']/div[@class='content']/div[{}]/div[@class='area_job']/h2[@class='job_tit']/a/span"
saramin_comp_path = "//*[@id='recruit_info_list']/div[1]/div[{}]/div[@class='area_corp']/strong[@class='corp_name']/a"
saramin_exp_path = "//*[@id='recruit_info_list']/div[@class='content']/div[{}]/div[@class='area_job']/div[@class='job_condition']/span[2]"
saramin_edu_path = "//*[@id='recruit_info_list']/div[@class='content']/div[{}]/div[@class='area_job']/div[@class='job_condition']/span[3]"
saramin_loc1_path = "//*[@id='recruit_info_list']/div[@class='content']/div[{}]/div[@class='area_job']/div[@class='job_condition']/span[1]/a[1]"
saramin_loc2_path = "//*[@id='recruit_info_list']/div[@class='content']/div[{}]/div[@class='area_job']/div[@class='job_condition']/span[1]/a[2]"
saramin_duedate_path = "//*[@id='recruit_info_list']/div[@class='content']/div[{}]/div[@class='area_job']/div[@class='job_date']/span"


job_list = []

for n in range(1, saramin_page_size + 1) :
    driver.get(saramin_url.format(n))

    WebDriverWait(driver, 3).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, saramin_size_path)
        )
    )

    saramin_size = driver.find_elements_by_xpath(saramin_size_path)

    #n페이지 시작
    for i in range(1, len(saramin_size) + 1) :
        try:
            job_comp = driver.find_element_by_xpath(saramin_comp_path.format(i)).text
        except:
            job_comp = ''
        
        try:
            job_title = driver.find_element_by_xpath(saramin_title_path.format(i)).text
        except:
            job_title = ''
        try:
            job_exp = driver.find_element_by_xpath(saramin_exp_path.format(i)).text
        except:
            job_exp = ''
        try:
            job_edu = driver.find_element_by_xpath(saramin_edu_path.format(i)).text
        except:
            job_edu = ''
        try:
            job_loc1 = driver.find_element_by_xpath(saramin_loc1_path.format(i)).text
        except:
            job_loc1 = ''
        try:
            job_loc2 = driver.find_element_by_xpath(saramin_loc2_path.format(i)).text
        except:
            job_loc2 = ''
        try:
            job_duedate = driver.find_element_by_xpath(saramin_duedate_path.format(i)).text  
        except:
            job_duedate = ''
 
        job_item = {
            'job_comp': job_comp,
            'job_title': job_title,
            'job_exp': job_exp,
            'job_edu': job_edu,
            'job_loc': job_loc1 + ' ' + job_loc2,
            'job_duedate': job_duedate,
            'add_date': time.time()
        }

        if job_comp != '' and job_title != '':
            job_list.append(job_item)
        else:
            print(job_title)

    #n페이지 종료   
    print(n, '페이지 : ' , len(job_list))


for n in range(1, jobkorea_page_size + 1) :
    driver.get(jobkorea_url.format(n))

    WebDriverWait(driver, 3).until(
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
try:
    db.insertList(job_list)
except:
    print('중복')

driver.quit()