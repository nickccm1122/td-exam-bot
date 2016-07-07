"""
Class: Single Attempt of application
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class Attempt:

    def __init__(self, client):
        self.driver = webdriver.Chrome('./bin/chromedriver')
        self.client = client
        self.alive = False

        def go(self):
            self.alive = self.processFirstPage()
            if self.alive:
                self.alive = self.processSencondPage()
            if self.alive:
                self.alive = self.processThirdPage()
            if self.alive:
                self.alive = self.processForthPage()
            if self.alive:
                self.alive = self.processFifthPage()

    def go(self):
        self.alive = self.processFirstPage()
        if self.alive:
            self.alive = self.processSencondPage()
        if self.alive:
            self.alive = self.processThirdPage()
        if self.alive:
            self.alive = self.processForthPage()
        if self.alive:
            self.alive = self.processFifthPage()

    def killAttempt(self):
        self.driver.quit()

    def processFirstPage(self):

        # create the chrome driver
        driver = self.driver

        # Page 1:
        # https://eapps2.td.gov.hk/repoes/td-es-app517/Welcome.do?language=zh
        # task 1: select radio button 2
        driver.get(
            'https://eapps2.td.gov.hk/repoes/td-es-app517' +
            '/Welcome.do?language=zh')

        print("[Start]: " + driver.current_url)
        radioChoice = driver.find_element_by_xpath(
            '//*[@id="contentPanel"]/div[3]/div[1]/div/' +
            'div[2]/table/tbody/tr/td/table/tbody/tr/td/form/input[2]')
        radioChoice.click()

        # task 2: goto next Page
        nextPage = driver.find_element_by_xpath(
            '//*[@id="contentPanel"]/div[4]/div/a[@class="redbutton"]')
        nextPage.click()

        return True

    def processSencondPage(self):

        driver = self.driver
        # Page 2:
        # https://eapps2.td.gov.hk/repoes/td-es-app517/SelectServiceAction.do
        # task 1: wait the page to be loaded
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "app517Form"))
            )
        except:
            driver.quit()
            return False

        print("[Start]: " + driver.current_url)

        radioChoice = driver.find_element_by_xpath(
            '//input[@name="serviceChoice"][@value="appointment"]')
        radioChoice.click()

        # task 2: goto next page, rely on the class="redbutton"
        nextButton = driver.find_element_by_xpath('//a[@class="redbutton"]')
        nextButton.click()

        return True

    def processThirdPage(self):

        driver = self.driver

        def waitForInput():

            count = 0
            elem = driver.find_element_by_id('jcaptcha_response')

            while True:
                count += 1
                if count > 40:
                    print("Key entered or Timing out after 20 seconds")
                    return False
                if len(elem.get_attribute('value')) == 6:
                    return True
                time.sleep(.5)

            return True

        # Page 3:
        # https://eapps2.td.gov.hk/repoes/td-es-app517/Welcome.do?language=zh
        # task 1: wait the page to be loaded
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "instructionForm"))
            )
        except:
            driver.quit()
            return False

        print("[Start]: " + driver.current_url)

        # task 2: check agree radio
        radioChoice = driver.find_element_by_xpath('//input[@name="agree"]')
        radioChoice.click()

        # task 3: check captcha
        captcha = driver.find_element_by_id('jcaptcha_response')
        driver.execute_script(
            "window.scrollTo(0,document.body.scrollHeight);" +
            "document.getElementById('jcaptcha_response').focus();")

        # Check if the captcha has been filled
        if not waitForInput():
            driver.quit()
            return False

        driver.find_element_by_xpath('//a[@class="redbutton"]').click()

        print("Jumping to next page!")
        return True

    def processForthPage(self):
        driver = self.driver
        client = self.client
        # check if the page is loaded
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "main"))
            )
        except:
            print("Can't load page 4..")
            driver.quit()
            return False

        finally:
            driver.switch_to_default_content
            driver.switch_to_frame('main')

        print("[Start]: " + driver.current_url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.ID, "testFormNumForLastAttempt"))
            )
        finally:
            print("Ready to input..")

        # Inputs the client's data:
        try:
            driver.find_element_by_id(
                'testFormNumForLastAttempt').send_keys(client['code'])
            driver.find_element_by_id(
                'testFormBirthYear').send_keys(client['b-year'])
            driver.find_element_by_id(
                'testFormBirthMonth').send_keys(client['b-month'])
            driver.find_element_by_id(
                'testFormBirthDay').send_keys(client['b-date'])

            driver.find_element_by_xpath('//a[@class="redbutton"]').click()
        except:
            print('Cant assign inputs')
            driver.quit()
            return False

        print("Jumping to next page!")
        return True

    def processFifthPage(self):

        driver = self.driver
        client = self.client

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//input[@name="telephoneNo"]'))
            )
            print("[Start]: " + driver.current_url)
        except:
            driver.quit()
            return False

        # Inputs the client's data:
        print("Ready to input..")
        try:
            driver.find_element_by_xpath(
                '//input[@name="telephoneNo"]').send_keys(client['mobile'])

            if client["lens"] == "n":
                driver.find_elements_by_xpath(
                    '//input[@name="wearLensesInd"]')[1].click()
            else:
                driver.find_elements_by_xpath(
                    '//input[@name="wearLensesInd"]')[0].click()

            driver.find_elements_by_xpath(
                '//input[@name="wearAidsInd"]')[1].click()
            driver.find_elements_by_xpath(
                '//input[@name="physicalHandicapInd"]')[1].click()

            driver.find_element_by_xpath('//a[@class="redbutton"]').click()
        except:
            raise
            driver.quit()
            return False

        print("Jumping to next page!")
        return True
