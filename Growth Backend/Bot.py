from selenium import webdriver
import json
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.support.ui import webDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from time import sleep,time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService 
import random
import re
import subprocess
import os
import requests
from atexit import register

max_time = 10

'''def open_chrome(port=9220, on_mac=True):
    my_env = os.environ.copy()
    if on_mac:
        print('opening chrome (mac)')
        subprocess.Popen(['open','-a',"Google Chrome",'--args',f'--remote-debugging-port={port}','http://wwww.example.com'])
    else:
        print('opening chrome (Linux)')
        subprocess.Popen(f'google-chrome -remote-debugging-port={port} --user-data-dir=data_dir'.split(),env=my_env)
    print('opened chrome')'''

class Bot():
    def __init__(self, port_no=9220, headless=False, verbose=False):
        print('initialising bot')
        options = Options()
        '''if headless:
            Options.add_argument("--headless")
        else:
            open_chrome()
            options.add_experimental_option(f"debuggerAddress",f"127.0.0.1:{port_no}")'''
        #self.driver = webdriver.Chrome(ChromeDriverManager().install())
        #options.add_argument("--no-sandbox")
        #self.driver = webdriver.Chrome(options=options)
        op = webdriver.ChromeOptions()
        op.add_argument('--headless=new')
        self.driver =  webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=op)
        self.verbose = verbose

    def scroll(self, x=0, y=1000000):
        self.driver.execute_script(f'window.scrollBy({x},{y})')

    def click_btn(self, text):
        if self.verbose:
            print(f'clicking {text} btn')
        element_types = ['button','div','input','a','label']
        for element_type in element_types:
            btns = self.driver.find_elements(By.XPATH, f'//{element_type}')
            try:
                btn = [b for b in btns if b.text.lower() == text.lower()][0]
                btn.click()
                return 
            except IndexError:
                pass

            try:
                btn = self.driver.find_elements(By.XPATH,f'//{element_type}[@value="{text}]')[0]
                btn.click()
                return
            except:
                continue
        raise ValueError(f'button containing "{text}" not found')
    
    def _search(self, query, _type='search', placeholder=None):
        sleep(1)
        s = self.driver.find_elements(By.XPATH,f'//input[@type="{_type}"]')
        print(s)
        if placeholder:
            s = [i for i in s if i.get_attribute('placeholder').lower() == placeholder.lower()][0]
        else:
            s = s[0]
        s.send_keys(query)

    def toggle_verbose(self):
        self.verbose = not self.verbose
    
    def download_file(self, src_url, local_destination):
        response = requests.get(src_url)
        with open(local_destination, 'wb+') as f:
            f.write(response.content)

    def __exit__(self):
        self.driver.quit()
