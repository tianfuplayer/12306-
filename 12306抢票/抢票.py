from logging import Formatter
from selenium import webdriver
from time import sleep
from selenium.webdriver import ActionChains
import json
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
import re

option  = ChromeOptions()
option.add_argument("start-maximized")
option.add_argument("--disable-blink-features")
option.add_argument("--disable-blink-features=AutomationControlled")

with open('./info.json','r') as fp:
    checi = json.load(fp)



bro = webdriver.Chrome(executable_path='./chromedriver',options=option)
u1 = 'https://kyfw.12306.cn/otn/resources/login.html'
u2 = 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E6%BB%95%E5%B7%9E%E4%B8%9C,TEK&ts=%E6%9D%AD%E5%B7%9E%E4%B8%9C,HGH&date=2022-09-01&flag=N,N,Y'
u2 = format('https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%s,TEK&ts=%s,HGH&date=%s&flag=N,N,Y' %(checi['s'],checi['d'],checi['t']))
url = 'https://www.12306.cn/index/index.html'
bro.get(u1)
sleep(1)

bro.find_element_by_id('J-userName').send_keys(checi['user'])
bro.find_element_by_id('J-password').send_keys(checi['password'])
sleep(0.5)
bro.find_element_by_id('J-login').click()

#滑动验证码
#定位验证码的头位置元素
sleep(1)

picture_start=bro.find_element_by_id('nc_1_n1z')

#移动到相应的位置，并左键鼠标按住往右边拖
ActionChains(bro).move_to_element(picture_start).click_and_hold(picture_start).move_by_offset(300,0).perform()
#验证成功后，页面会出现一个窗口 把他叉掉或者确定掉

sleep(5)
bro.get(u2)
sleep(1)

handle = bro.window_handles
bro.switch_to.window(handle[-1])
train_list = bro.find_elements_by_xpath('//tbody[@id="queryLeftTable"]/tr[not(@datatran)]')

count = 0
for t in train_list:
    msg = t.text.replace('\n',' ').split(' ')[0]
    count = count + 1
    sleep(1)
    if msg == checi['no']:
        print('find',msg)
        print('running script********************************')
        count = count * 2 -1
        while t.find_element_by_xpath('.//td[4]').text == '候补':
            
            print('refreshing******************************')
            bro.find_element_by_class_name('btn-area').click()
            sleep(2)
            t = bro.find_element_by_xpath('//*[@id="queryLeftTable"]/tr[%d]'%count)
            print(t)
            sleep(2)
        print('find tickts********************************')
        t.find_element_by_class_name('btn72').click()
        sleep(1)
        bro.find_element_by_xpath('//*[@id="normal_passenger_id"]/li[1]/label').click()
        bro.find_element_by_xpath('//*[@id="dialog_xsertcj_ok"]').click()
        bro.find_element_by_xpath('//*[@id="submitOrder_id"]').click()
        sleep(0.5)
        bro.find_element_by_xpath('//*[@id="qr_submit_id"]').click()
        print('end*******************************************')
        break

 


