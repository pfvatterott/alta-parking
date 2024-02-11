from selenium import webdriver
from seleniumrequests import Firefox
from selenium.webdriver.common.by import By
from decouple import config
from localStorage import LocalStorage
import requests
import time

email = config("email")
password = config("password")

parking_url = "https://reserve.altaparking.com/login"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

class ParkingLogin:
    def __init__(self):
        self.driver = Firefox()
        
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
        return
    
    def getHonkGuid(self):
        storage = LocalStorage(self.driver)
        self.honkGuid = storage["honkGUID"]

    
    def getAuthHeader(self):
        storage = LocalStorage(self.driver)
        self.authHeader = storage["oaTag"]
    
    def getVehicles(self):
        self.driver.get('https://platform.honkmobile.com')
        url = f"https://platform.honkmobile.com/vehicles?oa_tag={self.authHeader}&honkGUID={self.honkGuid}&app_version=69000"
        response = self.driver.request("GET", url=url)
        json = response.json()
        return json['data']['vehicles'][0]['id']
    
    def getPromoHashId(self): 
        url = f"https://platform.honkmobile.com/graphql?honkGUID={self.honkGuid}"
        headers = {
            'X-Authentication': self.authHeader,
        }
        payload = {
            "operationName": "AccountPromoCodes",
            "variables": {
                "zoneId": "elP1Tp"
            },
            "query": "fragment CorePromoCodeFields on PromoCode{hashid redeemCode shortDesc totalUses totalUsesCount expiry __typename}query AccountPromoCodes($zoneId: ID){accountPromoCodes(zoneId: $zoneId){...CorePromoCodeFields timezone startDate expiry promoCodesRates{activeSessionLimit activeSessionCount rate{hashid description zone{hashid __typename}__typename}__typename}__typename}}"
        }
        response = self.driver.request("POST", url=url, json=payload, headers=headers)
        json = response.json()
        return json['data']['accountPromoCodes'][0]['promoCodesRates'][0]['rate']['hashid']
    
    def createCart(self, date):
        url = f"https://platform.honkmobile.com/graphql?honkGUID={self.honkGuid}"
        headers = {
            'X-Authentication': self.authHeader,
        }
        payload = {
            "operationName": "CreateCart",
            "variables": {
                "input": {
                "startTime": f"{date}T08:00:00-07:00",
                "zoneId": "elP1Tp",
                "productType": "RESERVE"
                }
            },
            "query": "mutation CreateCart($input: CreateCartInput!) {createCart(input: $input) {cart { hashid __typename} errors __typename }}"
        }
        response = self.driver.request("POST", url, headers=headers, json=payload)
        json = response.json()
        return json['data']['createCart']['cart']['hashid']
    
    def claimCart(self, cartId):
        url = f"https://platform.honkmobile.com/graphql?honkGUID={self.honkGuid}"
        headers = {
            'X-Authentication': self.authHeader,
        }
        payload = {
            "operationName": "ClaimCart",
            "variables": {
                "input": {
                "id": cartId
                }
            },
            "query": "mutation ClaimCart($input: ClaimCartInput!) { claimCart(input: $input) { cart { hashid __typename } errors __typename }}"
        }
        response = self.driver.request("POST", url, headers=headers, json=payload)
        return response.json()
    
    def getAccountPromoCode(self):
        url = f"https://platform.honkmobile.com/graphql?honkGUID={self.honkGuid}"
        headers = {
            'X-Authentication': self.authHeader,
        }
        payload = {
            "operationName": "AccountPromoCodes",
            "variables": {
                "zoneId": "elP1Tp"
            },
            "query": "fragment CorePromoCodeFields on PromoCode { hashid redeemCode shortDesc totalUses totalUsesCount expiry __typename} query AccountPromoCodes($zoneId: ID) { accountPromoCodes(zoneId: $zoneId) { ...CorePromoCodeFields timezone startDate expiry promoCodesRates { activeSessionLimit activeSessionCount rate { hashid description zone { hashid __typename } __typename } __typename } __typename }}"
        }
        response = self.driver.request("POST", url, headers=headers, json=payload)
        json = response.json()
        return json['data']['accountPromoCodes'][0]['redeemCode']
    
    def addPromoToCart(self, promoCode, cartId):
        url = f"https://platform.honkmobile.com/graphql?honkGUID={self.honkGuid}"
        headers = {
            'X-Authentication': self.authHeader,
        }
        payload = {
            "operationName": "AddPromoToCart",
            "variables": {
                "input": {
                "cartId": cartId,
                "promoCode": promoCode,
                "validate": False
                }
            },
            "query": "mutation AddPromoToCart($input: AddPromoToCartInput!) { addPromoToCart(input: $input) { cart { hashid promoCode { hashid shortDesc redeemCode promoCodesRates { rate { hashid description zone { hashid __typename } __typename } __typename } __typename } __typename } errors __typename }}"
        }
        response = self.driver.request("POST", url, headers=headers, json=payload)
        return response.json()
    
    def addRateToCart(self, rateId, cartId):
        url = f"https://platform.honkmobile.com/graphql?honkGUID={self.honkGuid}"
        headers = {
            'X-Authentication': self.authHeader,
        }
        payload = {
            "operationName": "AddRateToCart",
            "variables": {
                "input": {
                    "rateId": rateId,
                    "cartId": cartId
                }
            },
            "query": "mutation AddRateToCart($input: AddRateToCartInput!) { addRateToCart(input: $input) { cart { id hashid __typename } errors __typename }}"
        }
        response = self.driver.request("POST", url, headers=headers, json=payload)
        self.driver.quit()
        json = response.json()
        return json['data']['addRateToCart']['cart']['id']
    
    def purchaseCart(self, vehicleId, cartId):
        url = f"https://platform.honkmobile.com/parking_sessions"
        payload = {
            "cart_id": int(cartId),
            "source": "web-app",
            "vehicle": vehicleId,
            "oa_tag": self.authHeader,
            "honkGUID": self.honkGuid,
            "app_version": 69000
        }
        response = requests.post(url, json=payload)
        return response.json()
    
