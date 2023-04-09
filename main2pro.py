import datetime
import threading
import time

from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from mainpro import preFun
mark_time=" 15:55:00.000000" #注意有空格，格式不能改
#输入课程按钮对应的href,如href="/study/selection/activitydetail/55011425-6886-43ab-805b-bc2817d06a70"
selector = '#divLectureItem > :nth-child(3) > :nth-child(10) > a'


def auto_v2():
    #后台加载，在chrome(),加上参数chrome_options= option
    #option = webdriver.ChromeOptions()
    #option.add_argument('headless')
    #option = Options()
    #option.add_argument('headless')
    global driver
    driver = webdriver.Chrome()

    # 打开指定的网页
    driver.get('https://spdpo.nottingham.edu.cn/study/auth/web')
    # 等待网页加载完成, 使用显性等待
    wait = WebDriverWait(driver, 10, 0.2)
    wait.until(EC.frame_to_be_available_and_switch_to_it('blank'))

    username = wait.until(EC.presence_of_element_located((By.ID, 'UserName')))
    password = wait.until(EC.presence_of_element_located((By.ID, 'Password')))
    
    login_button = wait.until(EC.presence_of_element_located((By.ID, 'btnLogin')))
    
    
    '''
    element=driver.find_element(By.ID, "Password")
    element.send_keys('abcd')
    #ActionChains(driver)\
           # .send_keys("abcd")\
            #.perform()
    '''
    
    
    # 输入用户名和密码
    username.send_keys('password')
    password.send_keys('username')
    
    # 点击登录按钮
    login_button.click()
    
    # 等待页面加载
    
    
    # 点击‘开始选课’
    specific_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[href="/study/selection"]')))
    specific_button.click()
    #完成选课界面加载
    print('加载完成')
    
    
def start_selection(sele):
    wait = WebDriverWait(driver, 10, 0.1)
    #使用频率更快的显性等待
    wait_quicker = WebDriverWait(driver, 0.5, 0.02)
    
    selecor = sele
    class_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selecor)))
    class_button.click()
    num=0
    while num<100:
        try:
            #依次点击两个确定
            # #layui-m-layer0 > div.layui-m-layermain > div > div > div.layui-m-layerbtn > span:nth-child(2) 或者 span[type='1']
            
            
            btn_save = wait_quicker.until(EC.presence_of_element_located((By.ID, 'btnSave')))
            btn_save.click()
        
            btn_confirm = wait_quicker.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[type='1']")))
            btn_confirm.click()
        except:
            return_btn = wait_quicker.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[href="javascript:;"]')))
            return_btn.click()
            class_button = wait_quicker.until(EC.presence_of_element_located((By.CSS_SELECTOR, selecor)))
            class_button.click()
            num +=1
        else:
            print('Success!!!')
            break
    
    #停留10秒
    time.sleep(10)

    #点击退出按钮
    
    return_btn = driver.find_element(By.CSS_SELECTOR, '[href="javascript:;"]')
    return_btn.click()
    
    time.sleep(7)
    # 关闭浏览器
    driver.quit()


def auto_start():
    timer_start_time=preFun(mark_time)
    # 把与处理得时间放进去  然后线程在start（）后
    # 会在规定秒数后启动你的func里的代码, 在设定时间的前五秒加载到界面
    timer = threading.Timer(timer_start_time - 15, auto_v2)
    timer2 = threading.Timer(timer_start_time, start_selection, args=[selector])
    # 运行线程
    timer.start()
    timer2.start()
    print('冷启动后启动func的时间',timer_start_time)
if __name__ == '__main__':
    auto_start()