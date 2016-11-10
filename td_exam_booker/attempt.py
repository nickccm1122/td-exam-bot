"""
Class: Single Attempt of application
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time
# from PIL import Image


class Attempt:

    def __init__(self, client):
        self.driver = webdriver.Chrome('./bin/chromedriver')
        self.client = client
        self.alive = False

    def go(self):

        while not self.alive:

            # Make sure no cookie
            self.driver.delete_all_cookies()

            self.alive = self.processFirstPage()

            if self.alive:
                self.alive = self.processSencondPage()
            # if self.alive:
            #     self.alive = self.processWarningPage()
            if self.alive:
                self.alive = self.processThirdPage()

        print("** Server is Up! **")
        if self.alive:
            self.alive = self.processForthPage()
        if self.alive:
            self.alive = self.processFifthPage()
        if self.alive:
            self.processLastPage()

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

        print("[Start]: " + driver.current_url + "\n")
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

        print("[Start]: " + driver.current_url + "\n")

        radioChoice = driver.find_element_by_xpath(
            '//input[@name="serviceChoice"][@value="appointment"]')
        radioChoice.click()

        # task 2: goto next page, rely on the class="redbutton"
        nextButton = driver.find_element_by_xpath('//a[@class="redbutton"]')
        nextButton.click()

        return True

    def processWarningPage(self):

        driver = self.driver
        # Page 2:
        # https://eapps2.td.gov.hk/repoes/checkclientconfig/warning.jsp
        # task 1: wait the page to be loaded
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "errorPanel"))
            )
        except:
            driver.quit()
            return False

        print("[Start]: " + driver.current_url + "\n")

        # task 2: goto next page, rely on the class="redbutton"
        nextButton = driver.find_element_by_css_selector('input.actionBtnCom')
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
                    print(">> Key entered or Timing out after 20 seconds..\n")
                    return False
                if len(elem.get_attribute('value')) == 6:
                    return True
                time.sleep(.5)

            return True

        # Page 3:
        # https://eapps2.td.gov.hk/repoes/td-es-app517/Welcome.do?language=zh
        # task 1: wait the page to be loaded
        try:
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.NAME, "instructionForm"))
            )
        except:
            # driver.quit()
            return False

        print("[Start]: " + driver.current_url + "\n")

        # task 2: check agree radio
        radioChoice = driver.find_element_by_xpath('//input[@name="agree"]')
        radioChoice.click()

        # task 3: check captcha
        # captcha = driver.find_element_by_id('jcaptcha_response')
        driver.execute_script(
            "window.scrollTo(0,document.body.scrollHeight);" +
            "document.getElementById('jcaptcha_response').focus();")

        # captcha = driver.find_element_by_xpath('//*[@id="contentPanel"]/form/div[3]/div/table/tbody/tr[2]/td/div/table/tbody/tr[1]/td/img')
        # location = element.location
        # size = element.size
        # im = Image.open(StringIO(base64.decodestring(driver.get_screensho‌​t_as_base64())))
        # left = location['x']
        # top = location['y']
        # right = location['x'] + size['width']
        # bottom = location['y'] + size['height']
        # im = im.crop((left, top, right, bottom))
        # im.save('screenshot.png')

        # Check if the captcha has been filled
        if not waitForInput():
            return False

        driver.find_element_by_xpath('//a[@class="redbutton"]').click()

        print(">> Jumping to next page..\n")
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
            print(">> Can't load first input page\n")
            driver.quit()
            return False

        finally:
            driver.switch_to_default_content
            driver.switch_to_frame('main')

        print("[Start]: First input page\n")

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.ID, "testFormNumForLastAttempt"))
            )
        finally:
            print(">> Ready to input..\n")

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
            print('>> Cant assign inputs..\n')
            driver.quit()
            return False

        print(">> Jumping to next page..\n")
        return True

    def processFifthPage(self):

        driver = self.driver
        client = self.client

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//input[@name="telephoneNo"]'))
            )
            print("[Start]: Second input page\n")
        except:
            print(">> Can't load second inputendar page\n")
            driver.quit()
            return False

        # Inputs the client's data:
        print(">> Ready to input..\n")
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

        print(">> Jumping to next page..\n")
        return True

    def processLastPage(self):

        # This method aims to located the available's link and
        # click on it if possible

        driver = self.driver
        client = self.client
        timeslot = None
        nextMonth = None
        testAreaCodeOption = None

        # check if the page is loaded
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html"))
            )
            print("[Start]: Calendar page\n")
        except:
            print(">> Can't load calendar page\n")
            driver.quit()
            return False
        else:
            driver.switch_to_default_content()
            driver.switch_to_frame('main')

        # If user are from kowloon, change to kowloon then
        if client["district"] == 'kowloon':
            # Try find the availale link and click it
            try:
                testAreaCodeOption = select = Select(driver.find_element_by_id('testAreaCode'))
            except:
                print(">> trouble selecting areaCode..\n")
            else:
                testAreaCodeOption.select_by_value('2')

        # check if the page is loaded
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html"))
            )
            print("[Start]: Calendar page\n")
        except:
            print(">> Can't load calendar page\n")
            driver.quit()
            return False
        else:
            driver.switch_to_default_content()
            driver.switch_to_frame('main')


        # Try find the availale link and click it
        try:
            timeslot = driver.find_element_by_xpath(
                '//td[@class="inner-table-cell"]/a')
        except:
            print(">> Couldn't find available timeslot..\n")
        else:
            timeslot.click()

        # If no available link if find,
        # try find the next month's link and click it
        if timeslot is None:
            try:
                nextMonth = driver.find_element_by_xpath(
                    '//td[@class="calendar-table-header"][3]/a')
            except:
                print(">> Next Month is not available as well..\n")
            else:
                nextMonth.click()

                # Try find the availale link and click it
                try:
                    timeslot = driver.find_element_by_xpath(
                        '//td[@class="inner-table-cell"]/a')
                except:
                    print(">> Couldn't find available timeslot in next month too..\n")
                else:
                    timeslot.click()


        if timeslot is not None:
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "/html"))
                )
                print("Almost there!!! Agree to print the booking\n")
            except:
                print(">> Can't load printing page\n")
                # driver.quit()
                return False
            else:
                # task 1: check agree radio
                radioChoice = driver.find_element_by_xpath('//input[@name="agree"]')
                radioChoice.click()
                driver.find_element_by_xpath('//a[@class="redbutton"]').click()




        print(">> I have done my job!\n")
        print("< Input 'q' to quit the program >")

        return True
