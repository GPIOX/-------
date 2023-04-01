'''
Descripttion: 
version: 
Author: Cai Weichao
Date: 2022-12-15 21:52:49
LastEditors: Cai Weichao
LastEditTime: 2022-12-15 21:52:50
'''
from requests_html import HTMLSession

session = HTMLSession()

url = 'http://www.win4000.com/'

obj = session.get(url)

obj.encoding = 'utf-8'

obj.html.render()  