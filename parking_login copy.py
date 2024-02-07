from selenium import webdriver
from selenium.webdriver.common.by import By
from decouple import config
from datetime import datetime
from localStorage import LocalStorage
import json
import requests
import time

email = config("email")
password = config("password")

parking_url = "https://reserve.altaparking.com/login"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

class ParkingLogin:
    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)
        
    
    def login(self):
        self.driver.get(parking_url)
        self.driver.find_element(By.XPATH, value='//*[@id="emailAddress"]').send_keys(email)
        self.driver.find_element(By.XPATH, value='//*[@id="password"]').send_keys(password)
        self.driver.find_element(By.XPATH, value='//*[@id="root"]/div/div/div/div[1]/div[2]/div/div/form/div[3]/button').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, value='//*[@id="root"]/div/div[3]/div/div/div/div[1]/a/div/div').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, value='//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/div/div/div[3]/button').click()
        time.sleep(1)
        # cookieString = ""
        # for cookie in cookies_list[:-1]:
        #     cookieString = cookieString + cookie["name"] + "="+cookie["value"]+"; "

        # cookieString = cookieString  + cookies_list[-1]["name"] + "="+ cookies_list[-1]["value"]
        # # xsrf_token = cookieString.split("XSRF-TOKEN=")[1].split("; ")[0].replace("%3D", "=")
        # # return {
        # #     "cookieString": cookieString,
        # #     "xsrf_token": xsrf_token
        # # }
        return
    
    def getHonkGuid(self):
        storage = LocalStorage(self.driver)
        return storage["honkGUID"]
    
    def getAuthHeader(self):
        storage = LocalStorage(self.driver)
        return storage["oaTag"]
    
    def createCart(self, authHeader, honkGuid):
        url = f"https://platform.honkmobile.com/graphql?honkGUID={honkGuid}"
        headers = {
            "content-type": "application/json",
            "user-agent": "PostmanRuntime/7.36.1",
            'X-Authentication': authHeader,
            # 'cookie': '__cf_bm=QPcEfR53mDMnYZ1MemyM6zcbQfDmH6QIgzWereCS56w-1707329203-1-AdA482iReWiGqeYpXnDhEcE37pKKs7QHA0rvK9c+q+xymJtrUZ+jodGdy1C3rxDzCjRRuWGTQaeWlK/9hHS0PM8='
        }
        payload = {
            "operationName": "CreateCart",
            "variables": {
                "input": {
                "startTime": "2024-02-10T08:00:00-07:00",
                "zoneId": "elP1Tp",
                "productType": "RESERVE"
                }
            },
            "query": "mutation CreateCart($input: CreateCartInput!) {createCart(input: $input) {cart { hashid __typename} errors __typename }}"
        }
        response = requests.request("POST", url, headers=headers, json=payload)
        print(response.text)
        return response.json()
    
    def getVehicles(self, authHeader, honkGuid):
        url = f"https://platform.honkmobile.com/vehicles?oa_tag={authHeader}&honkGUID={honkGuid}&app_version=69000"
        headers = {
            "content-type": "application/json",
            "user-agent": "PostmanRuntime/7.36.1"
        }
        response = requests.request("GET", url, headers=headers)
        cookie = ''
        for item in response.cookies:
            cookie = item.__dict__['value']
        return {"vehicle": response.json(), "cookie": cookie}
    
    def getPromoHashId(self, authHeader, honkGuid, cookie):
        url = f"https://platform.honkmobile.com/graphql?honkGUID={honkGuid}"
        payload = {
            "operationName": "AccountPromoCodes",
            "variables": {
                "zoneId": "elP1Tp"
            },
            "query": "fragment CorePromoCodeFields on PromoCode{hashid redeemCode shortDesc totalUses totalUsesCount expiry __typename}query AccountPromoCodes($zoneId: ID){accountPromoCodes(zoneId: $zoneId){...CorePromoCodeFields timezone startDate expiry promoCodesRates{activeSessionLimit activeSessionCount rate{hashid description zone{hashid __typename}__typename}__typename}__typename}}"
        }
        headers = {
            "Content-Type": "application/json",
            'X-Authentication': authHeader,
            'Cookie': '__cf_bm=LDedadeWTuCCtM7VmukxxmRPqomRycyvDIxRl7FRBq8-1707343101-1-AZBREH+WQYQ8evkbZBT2VSrdewGDOfi9WWLHsgUSKmnOC+Brhbauch7xguRRswHPWTN8pjNU3xQ9No4RnspwatI='
        }
        print(headers)
        response = requests.request("POST", url, headers=headers, json=payload)
        print(response.text)
        

        return response.json()
    
        
    # def getSeasonId(self, web_id, cookies, xsrf_token): 
    #     req_params = {
    #         "wtp": web_id,
    #         "productId": 0
    #     }
    #     req_headers = {
    #         "Cookie": cookies,
    #         "X-Requested-With": "XMLHttpRequest",
    #         "X-Xsrf-Token": xsrf_token
    #     }

    #     response = requests.post(url="https://shop.alta.com/axess/ride-data", json=req_params, headers=req_headers)
    #     return response.json()
        
    # def getSkiHistory(self, nposno, nprojno, nserialno, szvalidfrom, cookies, xsrf_token):
    #     req_params = {
    #         "nposno": nposno,
    #         "nprojno": nprojno,
    #         "nserialno": nserialno,
    #         "szvalidfrom": szvalidfrom
    #     }
    #     req_headers = {
    #         "Cookie": cookies,
    #         "X-Requested-With": "XMLHttpRequest",
    #         "X-Xsrf-Token": xsrf_token
    #     }

    #     response = requests.post(url="https://shop.alta.com/axess/rides", json=req_params, headers=req_headers)
    #     return response.json()  
    
        
        
    # def enter_web_id(self, web_id):
    #     self.driver.find_element(By.XPATH, value='//*[@id="wtp-0"]').send_keys(web_id)
    #     self.driver.find_element(By.XPATH, value='//*[@id="app"]/main/section/div[3]/div/div/div[1]/div/div/div/form/div/div[2]/div/div/div/button').click()
    #     time.sleep(3)
    #     error_or_success_msg = self.driver.find_element(By.CLASS_NAME, value="feedback")
    #     if len(error_or_success_msg.text) > 0:
    #         self.driver.quit()
    #         return False
        
    # def get_ski_history(self):
    #     self.driver.find_element(By.XPATH, value='//*[@id="app"]/main/section/div[3]/div/div/div[1]/div/div/div[3]/div/h4/a/i').click()
    #     time.sleep(5)
    #     return self.driver.find_element(By.XPATH, value='//*[@id="app"]/main/section/div[3]/div/div/div[1]/div/div/div[3]/div/h5')
        
    # def get_each_day(self):
    #     day_list = []
    #     each_day = self.driver.find_elements(By.CSS_SELECTOR, ".card-body .row .col-12 div h6")
    #     for day in each_day:
    #         feet = int(day.text.split("")[0].split("VERTICAL FEET ")[1].replace(",", ""))
    #         date = day.text.split("")[1].split(", ")[1]
    #         date = date.lower().replace("rd", "").replace("nd", "").replace("st", "").replace("th", "")
    #         date = datetime.strptime(date, "%B %d %Y").strftime("%m/%d/%Y")
    #         obj = {
    #             "date": date,
    #             "feet": feet
    #         }
    #         day_list.append(obj)
    #     return day_list
    
    # def get_runs_each_day(self, day_list):
    #     runs_each_day = self.driver.find_elements(By.CSS_SELECTOR, ".card-body .row .col-12 div .table-responsive table")
    #     runs_in_day_index = 0
    #     for runs in runs_each_day:
    #         each_run = runs.text.split("")
    #         run_array = []
    #         for run in each_run:
    #             if "Lift Time" not in run:
    #                 obj = {
    #                     "lift": run.split(" ")[0],
    #                     "time": run.split(" ")[1] + " " + run.split(" ")[2] 
    #                 }
    #                 run_array.append(obj)
    #         day_list[runs_in_day_index]["runs"] = run_array
    #         runs_in_day_index += 1
            
    #     return day_list
        
        