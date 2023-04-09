import datetime
import threading
import time
import re

from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from main2pro import auto_v2, start_selection

def auto_search():
    '''
    自动返回所有课程的时间和对应的selector
    '''
    #后台加载，在chrome(),加上参数chrome_options= option
    #option = webdriver.ChromeOptions()
    #option.add_argument('headless')
    #option = Options()
    #option.page_load_strategy = 'eager'
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

    # 打开指定的网页
    driver.get('https://spdpo.nottingham.edu.cn/study/auth/web')
    driver.switch_to.frame('blank')
    
    username = driver.find_element(By.ID, 'UserName')
    password = driver.find_element(By.ID, 'Password')
    login_button = driver.find_element(By.ID, 'btnLogin')
    username.send_keys('username') #输入你的用户名
    password.send_keys('password') #输入你的密码
    login_button.click()
    # 点击‘开始选课’
    specific_button = driver.find_element(By.CSS_SELECTOR, '[href="/study/selection"]')
    specific_button.click()


    #获取到所有课程的时间信息
    target_dates = driver.find_elements(By.CSS_SELECTOR, '[class = "divDataList"] > div:nth-child(4)')
    target_dates_textlist = []
    for i in target_dates:
        target_dates_textlist.append(i.text)
    #print(target_dates_textlist)

    #获取到所有对应的selector
    target_selector_textlist = []
    for i in range(len(target_dates_textlist)):
        target_selector_textlist.append('#divLectureItem > :nth-child('+str(i+1)+') > :nth-child(10) > a')
    #print(target_selector_textlist)
    driver.quit()

    return target_dates_textlist, target_selector_textlist
    





def extract_dates(List):
    #使用正则表达式提取时间，并输出“ xx:xx:xx.xxxxxx"格式的时间到一个列表
    result_list=[]
    pattern = r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}'
    for i in List:
        a=re.search(pattern, i)
        if a != None:
            result_list.append(a.group())
        else:
            raise ValueError("没有匹配到合规的时间")
    
    return result_list


def prefun3(List):
    '''
    将格式为'2023-03-09 12:00'的字符串转化为时间类型并以列表输出
    '''
    result_list=[]
    for i in List:
        next_time = datetime.datetime.strptime(i, "%Y-%m-%d %H:%M")
        result_list.append(next_time)
    return result_list


def auto_main3(List, sele_list):
    '''
    main3主体, 输入datetime 类型的时间列表, 和对应课程selector(存储在sele_list里)
    '''
    #开始重排List 和 sele_list 创造以sele_list 为第一个的元组对列表[(a,b),(c,d),...]
    listpair = list(zip(sele_list, List))
    #根据元组对里的时间升序排序
    listpair = sorted(listpair, key= lambda x: x[1])
    #将元组对重新拆分成两个元组
    sele_list, List = zip(*listpair)
    i=0
    for next_time in List:
        now_time = datetime.datetime.now()
        selector = sele_list[i]
        print(next_time)
        print(selector)
        if now_time > next_time:
            print('列表中第', List.index(next_time)+1,'次活动时间已过, 尝试下一个活动, 此次活动原定时间为', next_time)
        else:
            timer_start_time = (next_time- now_time).total_seconds()
            timer = threading.Timer(timer_start_time - 15, auto_v2)
            timer2 = threading.Timer(timer_start_time, start_selection, args=[selector])
            # 运行线程
            timer.start()
            timer2.start()
            print('冷启动后启动func的时间',timer_start_time)
            print('第',List.index(next_time)+1,'抢课时间信息为:', next_time)
            time.sleep(timer_start_time+60)
        i+=1
    


if __name__ == '__main__':
    x=auto_search()
    a=x[0]            #返回时间列表
    b=x[1]            #返回selector列表
    a=prefun3(extract_dates(a)) #处理一下时间列表, 现在列表里都是datetime对象
    auto_main3(a, b)
    


