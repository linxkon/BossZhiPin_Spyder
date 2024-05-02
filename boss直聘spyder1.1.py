from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import csv


# 创建Chrome浏览器驱动程序
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
zone_dict_shanghai = {
            '崇明区':'310151',
            '黄浦区':'310101',
            '虹口区':'310109',
            '杨浦区':'310110',
            '徐汇区':'310104',
            '长宁区':'310105',
            '静安区':'310106',
            '普陀区':'310107',
            '金山区':'310116',
            '松江区':'310117',
            '青浦区':'310118',
            '闵行区':'310112',
            '宝山区':'310113',
            '嘉定区':'310114',
            '浦东新区':'310115',
            '奉贤区':'310120',
                    }
zone_dict_jinan = {
            '长清区': '370113',
            '历城区': '370112',
            '市中区': '370103',
            '历下区': '370102',
            '天桥区': '370105',
            '槐荫区': '370104'
            # '钢城区':'370117',
            # '莱芜区':'370116',
            # '济阳区':'370115',
            # '章丘区':'370114',
            # '平阴县':'370124',
            # '商河县':'370126',
                    }
zone_dict_beijing = {
            '东城区': '110101',
             '西城区': '110102',
             '朝阳区': '110105',
             '石景山区': '110107',
             '丰台区': '110106',
             '门头沟区': '110109',
             '海淀区': '110108',
             '房山区': '110111',
             '顺义区': '110113',
             '通州区': '110112',
             '大兴区': '110115',
             '昌平区': '110114',
             '平谷区': '110117',
             '怀柔区': '110116',
             '延庆区': '110119',
             '密云区': '110118'
}
#1.选择爬取城市
def select_city(zonecode=None):
    global city_name
    global zone_dict
    city = input('请选择爬取城市:1.上海,2.北京,3.济南:')
    if city == '1':         #上海
        city_name = '上海'
        zonecode = '101020100'
        zone_dict=zone_dict_shanghai
    elif city == '2':         #北京
        city_name = '北京'
        zonecode = '101010100'
        zone_dict=zone_dict_beijing
        # return zone_dict,zonecode
    elif city == '3':         #济南
        city_name = '济南'
        zonecode = '101120100'
        zone_dict=zone_dict_jinan
        # return zone_dict,zonecode
    else:
        print('输入错误,请重新输入')
        select_city()
    if zonecode is not None:
        # 进入要爬取的城市页面
        main_url = f'https://www.zhipin.com/web/geek/job?city={zonecode}'
        driver.get(main_url)
        return zone_dict,zonecode
#2.定义进入要爬取的页面函数
def selec_job():
    ###### 进入要爬取的页面

    # 进入要爬取的关键词页面
    keywords=input('请输入要爬取岗位的关键词,如算法工程师,并按回车键继续:')
    wait = WebDriverWait(driver, 10)  # 设置等待时间为10秒        //*[@id="wrap"]/div[2]/div[1]/div[1]/div/div/div/input
    search_box='//*[@id="wrap"]/div[2]/div[1]/div[1]/div/div/div/input'
    input_element = wait.until(EC.element_to_be_clickable((By.XPATH, search_box)))
    input_element.send_keys(keywords, Keys.RETURN)

    refirm=input('是否已经登录并且进入了要爬取的页面？重置请输入reset,继续请回车')
    if refirm == 'reset':
        input_element = driver.find_element(By.XPATH, search_box)
        input_element.clear()
        selec_job()
#定义检查是否需要输入验证码函数
def check_code():
    # 检查是否需要输入验证码
    try:                                           #//*[@id="wrap"]/div/div[1]/div/button
        code = driver.find_element(By.XPATH, '//*[@id="wrap"]/div/div[1]/div/button')
        return True
    except:
        return False
#定义输入验证码函数
def input_code():
    # 输入验证码
    print('请输入验证码,完成后按回车键继续')
    input('请输入验证码:')
    # 检查是否需要输入验证码
    if check_code():
        input_code()
#定义页面爬取写入函数
def craw_page(page_dive,zn):          #page_dive:页面的div位置,第0页是2,其他页是1
    # 等待元素加载
    wait = WebDriverWait(driver, 10)
    for j in range(1, 30):
        xpath_name = f'//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[{page_dive}]/ul/li[{j}]/div[1]/a/div[1]/span[1]'
        element_name = wait.until(EC.visibility_of_element_located((By.XPATH, xpath_name)))
        element_name = driver.find_element(By.XPATH, xpath_name)

        xpath_lo = f'//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[{page_dive}]/ul/li[{j}]/div[1]/a/div[1]/span[2]'
        element_lo = driver.find_element(By.XPATH, xpath_lo)
        xpath_money = f'//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[{page_dive}]/ul/li[{j}]/div[1]/a/div[2]/span'
        element_money = driver.find_element(By.XPATH, xpath_money)
        xpath_needs = f'//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[{page_dive}]/ul/li[{j}]/div[1]/a/div[2]/ul'
        element_needs = driver.find_element(By.XPATH, xpath_needs).text
        element_needs= element_needs.replace('\n', ',')

        xpath_url=f'//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[{page_dive}]/ul/li[{j}]/div[1]/a'
        target_element = driver.find_element(By.XPATH,xpath_url)
        element_url = target_element.get_attribute('href')
        # 打印当前爬取内容
        # print(element_name.text,'|', element_money.text,'|', element_needs,'|', element_url)
        # 写入爬取内容
        writer.writerow([element_name.text, element_lo.text, element_money.text,element_needs,element_url,zn])

#点击下一页并执行是否为最后一页的判断
def next_page():  # page_dive:页面的div位置,第0页是2,其他页是1
    # 获取点击前链接地址
    current_url = driver.current_url
    # 定位到下一页按钮
    driver.execute_script("window.scrollTo(0, 4500);")
    # 点击下一页
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ui-icon-arrow-right"))
    )
    element.click()
    # 等待新页面加载完成
    time.sleep(0.3)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ui-icon-arrow-right")))
    # 获取新网址
    new_url = driver.current_url
    # 如果新网址和旧网址相同,则说明已经到达最后一页
    if current_url == new_url:
        # 二次核实
        time.sleep(3)
        new_url = driver.current_url
        if current_url == new_url:
            print('已到达最后一页')
            global i
            i = 11

    # return i
# 分区爬取函数
def multy_zone_craw(zone_dict):
    # 分区爬取招聘数据,可突破10页限制
    # 获取当前页面的网址
    current_url = driver.current_url
    for zn in zone_dict:
        print('正在获取:',zn)
        url= current_url + f'&areaBusiness={zone_dict[zn]}'
        try_times = 0
        while try_times <5:
            try:
                driver.get(url)
                single_zone_craw(zn)
                break
            except:
                try_times +=1
# 爬取当前页面及后续的9页,若遇到错误会尝试5次.
def single_zone_craw(zn):
    global i
    i=2
    # 爬取第一页
    craw_page(2,zn)        ##正常改为2
    # 点击第一页的下一页
    next_page()
    # print('i值为',i)
    while i <=10: #爬取页数
        print(f'第{i}页')
        try_times = 0
        # 尝试爬取5次
        while try_times < 5:
            try:
                # 爬取页面
                craw_page(1,zn)
                print('爬取成功')
                i += 1
                # 点击下一页
                next_page()
                # end_page = False
                break
            except:
                time.sleep(3)
                # 检查是否有验证码
                if check_code():
                    input_code()
                    i=i
                    continue
                try_times += 1
                print('爬取失败,正在重新尝试:',try_times)
                # 尝试5次后,若仍然无法爬取,则跳过该区域
                if try_times == 5:
                    print('爬取失败,该区域将被跳过,当前网址是:',driver.current_url)
                    input('press any key to continue')
                    i = 11    #跳出大循环
                    break
        if i >10:
            print('本区域循环结束,准备获取下个区域')

if __name__ == '__main__':
    # 登录页面
    driver.get("https://www.zhipin.com/web/user/?ka=header-login")
    input('请扫码登录,并在此按回车键')
    select_city()
    selec_job()

    # 获取当前日期
    current_date = datetime.now().strftime("%Y%m%d")
    # 构建新的文件名
    filename = f"{city_name}boss直聘{current_date}.csv"
    # 创建csv文件
    with open(f'data/{filename}', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # 写入表头
        writer.writerow(['名称', '地点', '薪资', '招聘需求', '详情网址','区域'])  # 根据你爬取的数据添加表头
        # 写入爬取数据
        # single_zone_craw()
        multy_zone_craw(zone_dict)
        print(f'爬取完成,数据已保存为{filename}')
