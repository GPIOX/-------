'''
Descripttion: 
version: 
Author: Cai Weichao
Date: 2023-02-10 16:52:13
LastEditors: Cai Weichao
LastEditTime: 2023-04-01 16:14:13
'''
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

def get_bib_format(executable_path, paper_name, save_path, former_select):
    options = webdriver.EdgeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu') # 上面代码就是为了将Chrome不弹出界面
    options.add_argument('--incognito') #无痕隐身模式
    options.add_argument("disable-cache") #禁用缓存
    options.add_argument('log-level=3') #设置等级为3，只显示warning和error
    options.add_argument('disable-infobars')
    options.add_experimental_option('excludeSwitches', ['enable-automation']) # 设置开发者模式
    options.add_experimental_option('excludeSwitches', ['enable-logging'])    

    # 使用edge浏览器
    driver = webdriver.Edge(options=options, executable_path=executable_path)
    driver.get('https://0-scholar-google-com.brum.beds.ac.uk/schhp?hl=zh-CN')

    wait = WebDriverWait(driver, 20)

    # 输入文献名
    search_input = driver.find_element_by_xpath('//*[@id="gs_hdr_tsi"]')
    search_input.send_keys(paper_name)
    search_input.send_keys(Keys.ENTER)
    # text_editor.setText("正在搜索文献...")

    # 等待页面加载并点击引用
    reference_span_xpath = '//*[@id="gs_res_ccl_mid"]/div[1]/div/div[3]/a[2]/span'
    wait.until(lambda driver: driver.find_element_by_xpath(reference_span_xpath))
    # 点击第一个文献
    driver.find_element_by_xpath(reference_span_xpath).click()
    # text_editor.setText("正在获取文献信息...")
    # print(former_select)
    
    if former_select == 'bib格式':
        # 等待页面加载并点击引用
        wait.until(lambda driver: driver.find_element_by_xpath('//*[@id="gs_citi"]/a[1]'))
        driver.find_element_by_xpath('//*[@id="gs_citi"]/a[1]').click()

        # 等待页面加载并获取引用信息
        wait.until(lambda driver: driver.find_element_by_xpath('/html/body/pre'))
        # 获取引用信息
        bib = driver.find_element_by_xpath('/html/body/pre').text
        # text_editor.setText("正在保存文献信息并显示...")
        # print(bib)

        # 保存引用信息
        # if arg.save_mode == 'save':
        #     with open(arg.save_path, 'w') as f:
        #         f.write(bib+'\n')

        # elif arg.save_mode == 'appending':
        with open(save_path, 'a+') as f:
            f.write(bib+'\n')

        # 打印完成信息
        # print(f'The bib format of {arg.paper_name} has been written successfully.')

        # 关闭浏览器
        return bib
    elif former_select == '国标GB/T 7714':
        gbt = wait.until(lambda driver: driver.find_element_by_xpath('//*[@id="gs_citt"]/table/tbody/tr[1]/td/div')).text
        return gbt
    driver.quit()
