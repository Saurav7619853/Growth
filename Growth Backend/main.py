import json
from Bot import Bot
from selenium.webdriver.common.by import By
from time import sleep
import itertools
import urllib
from selenium.common.exceptions import NoSuchElementException
import os
import copy
from random import shuffle
import dateparser
'''timestrings = ['1 years 2 days ago' ,'3 hours 4 mins ago','5 mins 6 secs ago']

for timestring in timestrings:
    dt = dateparser.parse(timestring)
    print(dt.strftime("%Y-%m-%d %H:%M"))'''

var = "I2Cbhb bSuYSc"

class StackScraper(Bot):
    def __init__(self):
        super().__init__(verbose=True)
        role_names = ["mechanic"]
        companies = ["delhi"]
        shuffle(companies)
        shuffle(role_names)
        self.driver.get("https://www.google.com")
        for role_name, company in itertools.product(role_names, companies):
            self.save_job(self.get_all_jobs(role_name, company),role_name, company)
            

    def get_all_jobs(self, role_name, company):
        query = f"https://www.google.com/search?q={role_name} {company} posted in last {1} day &ibp=htl;jobs#htivrt=jobs".replace(
            ' ', '+')
        print(query)
        self.driver.get(query)
        listings = self.driver.find_elements(By.XPATH, "//div[@class='PwjeAc']")
        full_listing = 0
        i = 0
        jobs = []
        #print(listings)
        sleep(0.5)
        while full_listing!=len(listings):
            full_listing=len(listings)
            for idx, listing in enumerate(listings):
                if idx>=i*10:
                    self.scroll_into_view(listing)
                    listing.click()
                    sleep(1)
                    #job = self.__get__job()
                    try:
                        job = self.__get__job()
                    except Exception as e:
                        continue
                    jobs.append(job)
                    print(job)
                    #self.save_job(job, role_name, company)
            i=i+1
            listings = self.driver.find_elements(By.XPATH, "//div[@class='PwjeAc']")
            sleep(0.5)
        #print(listings)
        return jobs

    def scroll_into_view(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true)", element)

    def __get__job(self):
        return {
            "id": self.__get_job_id(),
            "title": self.__get_job_title(),
            "company": self.__get_company(),
            "location": self.__get_job_location(),
            "date": self.__get_job_info()[0],
            "job_type": self.__get_job_info()[2],
            "job_category": self.__get_job_info()[1],
            "job_salary": self.__get_job_salary(),
            "description": self.__get_job_description(),
            "job_url": self.__get_job_url()
        }

    def __get_job_id(self):
        parsed_url = urllib.parse.urlparse(self.driver.current_url)
        id = urllib.parse.parse_qs(parsed_url.fragment)['htidocid'][0]
        return id

    def __get_company(self):
        company = ''
        try:
            job_container = self.driver.find_element(
            By.XPATH, '//div[@class="whazf bD1FPe"]')
            company = job_container.find_element(
            By.XPATH, './/div[@class="nJlQNd sMzDkb"]').text
        except:
            pass
        return company
    
    def __get_job_title(self):
        job_title = ''
        try:
            job_title_container = self.driver.find_element(
            By.XPATH, '//div[@class="whazf bD1FPe"]')
            job_title = job_title_container.find_element(
            By.XPATH, './/div[@class="sH3zFd"]').find_element(By.TAG_NAME,'h2').text
        except:
            pass
        return job_title

    def __get_job_location(self):
        job_location = ''
        try:
            job_title_container = self.driver.find_element(
                By.XPATH, '//div[@class="whazf bD1FPe"]')
            job_location = job_title_container.find_element(
                By.XPATH, './/div[@class="sMzDkb"]').text
        except:
            pass
        return job_location
    
    def __get_job_info(self):
        job_info_data = ['','','']
        try:
            job_title_container = self.driver.find_element(
            By.XPATH, '//div[@class="whazf bD1FPe"]')
            job_info = job_title_container.find_elements(
            By.XPATH, './/div[@class="I2Cbhb"]')
            if len(job_info)==1:
                try:
                    job_info_data[1] = job_info[0].find_element(By.XPATH,'.//span[@class="LL4CDc"]').text
                except:
                    pass
            elif len(job_info)==2:
                try:
                    date = job_info[0].find_element(By.XPATH,'.//span[@class="LL4CDc"]').text
                    dt = dateparser.parse(date)
                    job_info_data[0] = dt.strftime("%Y-%m-%d %H:%M")
                except:
                    pass
                try:
                    job_info_data[2] = job_info[1].find_element(By.XPATH,'.//span[@class="LL4CDc"]').text
                except:
                    pass
            elif len(job_info)==3:
                try:
                    job_info_data[0] = job_info[0].find_element(By.XPATH,'.//span[@class="LL4CDc"]').text
                except:
                    pass
                try:
                    job_info_data[1] = job_info[1].find_element(By.XPATH,'.//span[@class="LL4CDc"]').text
                except:
                    pass
                try:
                    job_info_data[2] = job_info[2].find_element(By.XPATH,'.//span[@class="LL4CDc"]').text
                except:
                    pass
        except:
            pass
        return job_info_data
    
    def __get_job_salary(self):
        job_salary = ''
        try:
            job_title_container = self.driver.find_element(
            By.XPATH, '//div[@class="whazf bD1FPe"]')
            job_salary = job_title_container.find_elements(
            By.XPATH, './/div[@class="I2Cbhb bSuYSc"]')[0].find_element(By.XPATH,'.//span[@class="LL4CDc"]').text
        except:
            pass
        return job_salary

    def __get_job_description(self):
        try:
            job_container = self.driver.find_element(
            By.XPATH, '//div[@class="whazf bD1FPe"]')
            expand_description_button = job_container.find_element(
                By.XPATH, ".//div[@class='CdXzFe j4kHIf']")
            self.scroll_into_view(expand_description_button)
            expand_description_button.click()
        except NoSuchElementException:
            pass
        description = ''
        try:
            description = job_container.find_element(
            By.XPATH, ".//span[@class='HBvzbc']").text
        except:
            pass
        return description
    
    def __get_job_url(self):
        job_url = ''
        try:
            job_title_container = self.driver.find_element(
            By.XPATH, '//div[@class="whazf bD1FPe"]')
            job_url = job_title_container.find_element(
            By.XPATH, '//a[@class="pMhGee Co68jc j0vryd"]').get_attribute("href")
        except:
            pass
        return job_url

    def save_job(self, jobs, role_name, company):
        if self.verbose:
            print(f'Saving {role_name} job at {company}')
        folder_path = os.path.join("raw_data", role_name.replace(
            " ", "-"), company.replace(" ", "-"))
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, "Ml.json")
        print(file_path)
        '''with open(file_path, 'w') as f:
            json.dump(job, f, indent=4)'''

        with open(file_path, 'w', encoding='utf-8') as jsonf:
            jsonf.write(json.dumps(jobs,indent=4))


if __name__ == '__main__':
    StackScraper()
