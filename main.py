'''
Descripttion: 
version: 
Author: Cai Weichao
Date: 2022-12-16 17:31:42
LastEditors: Cai Weichao
LastEditTime: 2023-02-10 21:45:43
'''
'''
Descripttion: 
version: 
Author: Cai Weichao
Date: 2022-12-15 20:59:30
LastEditors: Cai Weichao
LastEditTime: 2023-02-09 15:35:59
'''
import argparse
import json
import os
# import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

# 读取配置文件
with open(os.path.join(os.path.expanduser("~"), 'getbib', 'config.json'), 'r') as f:
    config = json.load(f)

options = webdriver.EdgeOptions()
# options.add_argument('--headless')

# 使用edge浏览器
driver = webdriver.Edge(options=options, executable_path=config["executable_path"])

# parser参数设置
def parse_args():
    # description为自动获取文献bib注释的英文
    parser = argparse.ArgumentParser(description='reference from sci-hub')
    parser.add_argument('--paper-name', type=str, default=None, help='paper full name ')
    parser.add_argument('--save-mode', type=str, default='appending', help='[save or appending], Saving or appending citation information')
    parser.add_argument('--config', action='store_true', default=False, help='config the executable_path of msedgedriver.exe')
    parser.add_argument('--save-path', type=str, default=f"{os.path.join(os.path.expanduser('~'), 'getbib', 'reference.bib')}", help='path to save the citation information')

    return parser.parse_args()



def main(arg):
    # 使用edge浏览器

    driver.get('https://0-scholar-google-com.brum.beds.ac.uk/schhp?hl=zh-CN')

    wait = WebDriverWait(driver, 20)

    # 输入文献名
    search_input = driver.find_element_by_xpath('//*[@id="gs_hdr_tsi"]')
    search_input.send_keys(arg.paper_name)
    search_input.send_keys(Keys.ENTER)

    # 等待页面加载并点击引用
    wait.until(lambda driver: driver.find_element_by_xpath('//*[@id="gs_res_ccl_mid"]/div[1]/div/div[3]/a[2]/span'))
    # 点击第一个文献
    driver.find_element_by_xpath('//*[@id="gs_res_ccl_mid"]/div[1]/div/div[3]/a[2]/span').click()
    
    # 等待页面加载并点击引用
    wait.until(lambda driver: driver.find_element_by_xpath('//*[@id="gs_citi"]/a[1]'))
    driver.find_element_by_xpath('//*[@id="gs_citi"]/a[1]').click()

    # 等待页面加载并获取引用信息
    wait.until(lambda driver: driver.find_element_by_xpath('/html/body/pre'))
    # 获取引用信息
    bib = driver.find_element_by_xpath('/html/body/pre').text
    # print(bib)

    # 保存引用信息
    if arg.save_mode == 'save':
        with open(arg.save_path, 'w') as f:
            f.write(bib+'\n')

    elif arg.save_mode == 'appending':
        with open(arg.save_path, 'a+') as f:
            f.write(bib+'\n')

    # 打印完成信息
    print(f'The bib format of {arg.paper_name} has been written successfully.')

    # 关闭浏览器
    driver.quit()
    

if __name__ == '__main__':
    arg = parse_args()

    if arg.paper_name is None:
        raise Exception('paper_name is None')

    if arg.config:
        if not os.path.exists(os.path.join(os.path.expanduser("~"), 'getbib')):
            os.mkdir(os.path.join(os.path.expanduser("~"), 'getbib'))

        if not os.path.exists(os.path.join(os.path.expanduser("~"), 'getbib', 'config.json')):
            with open(os.path.join(os.path.expanduser("~"), 'getbib', 'config.json'), 'w') as f:
                json.dump({'executable_path': f"{os.path.join(os.environ.get('CONDA_PREFIX'), 'msedgedriver.exe')}"}, f)

    main(arg)
