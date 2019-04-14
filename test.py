import unittest
import json
import time
from appium import webdriver
from datetime import datetime, timedelta


class TripAdvisorAndroidTest(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '8.0.0'
        desired_caps['deviceName'] = '192.168.57.101:5555'
        desired_caps['noReset'] = 'true'
        desired_caps['appPackage'] = 'com.tripadvisor.tripadvisor'
        desired_caps['appActivity'] = '.TripAdvisorTripAdvisorActivity'
        #desired_caps['automationName'] = 'uiautomator2'

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        self.driver.quit()

    def testHotel(self):

        hotel = "The Grosvenor Hotel"
        dates = ["2019-04-16", "2019-05-23", "2019-04-18", "2019-04-20", "2019-04-25"]
        output = {}

        self.driver.implicitly_wait(30)
        search_hotel = self.driver.find_element_by_id("com.tripadvisor.tripadvisor:id/search_image")
        search_hotel.click()

        hotel_search_box = self.driver.find_element_by_id("com.tripadvisor.tripadvisor:id/what_query_text")
        hotel_search_box.send_keys("The Grosvenor Hotel")

        search_result = self.driver.find_element_by_android_uiautomator('new UiSelector().textContains("101 Buckingham Palace Road, London")')
        search_result.click()

        self.driver.swipe(400, 1000, 400, 545, 1500)

        output[hotel] = {}

        for date in dates:

            date_in = 'new UiSelector().description("' + date + '")'

            try:
                date_f = datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                print("Wrong date: ", date)
                continue

            if date_f < datetime.now():
                print('got it')
                continue

            end_date = date_f + timedelta(days=1)
            date_out = 'new UiSelector().description("' + end_date.date().strftime("%Y-%m-%d") + '")'

            output[hotel][date] = {}

            self.driver.find_element_by_id("com.tripadvisor.tripadvisor:id/set_dates_button").click()

            self.driver.find_element_by_id('com.tripadvisor.tripadvisor:id/action_clear').click()

            self.driver.swipe(400, 400, 400, 1000, 300)
            self.driver.swipe(400, 400, 400, 1000, 300)
            top_calendar = self.driver.find_elements_by_android_uiautomator('new UiSelector().description("' + datetime.now().strftime("%Y-%m-%d") + '")')
            while not len(top_calendar) > 0:
                self.driver.swipe(400, 400, 400, 1000, 300)
                time.sleep(2)
                top_calendar = self.driver.find_elements_by_android_uiautomator('new UiSelector().description("' + datetime.now().strftime("%Y-%m-%d") + '")')

            time.sleep(2)
            check_in_date = self.driver.find_elements_by_android_uiautomator(date_in)
            while not len(check_in_date) > 0:
                self.driver.swipe(400, 1040, 400, 500, 1500)
                time.sleep(2)
                check_in_date = self.driver.find_elements_by_android_uiautomator(date_in)
            check_in_date[0].click()

            time.sleep(2)
            check_out_date = self.driver.find_elements_by_android_uiautomator(date_out)
            while not len(check_in_date) > 0:
                self.driver.swipe(400, 1040, 400, 500, 1500)
                time.sleep(2)
                check_out_date = self.driver.find_element_by_android_uiautomator(date_out)
            check_out_date[0].click()

            time.sleep(2)
            view_all_deals = self.driver.find_elements_by_id('com.tripadvisor.tripadvisor:id/text_links_revealer_button')
            if len(view_all_deals) > 0:
                view_all_deals[0].click()

            prov_price = {}

            providers = self.driver.find_elements_by_id('com.tripadvisor.tripadvisor:id/title_and_price_container')

            for prov in providers:
                title = prov.find_element_by_id('com.tripadvisor.tripadvisor:id/title')
                price = prov.find_element_by_id('com.tripadvisor.tripadvisor:id/price')
                prov_price[title.text] = price.text

            self.driver.save_screenshot('output/' + date + '.png')

            output[hotel][date]["prices"] = prov_price
            output[hotel][date]["screenshot"] = 'output/' + date + '.png'

        with open('output/output.json', 'w+') as outfile:
            json.dump(output, outfile)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TripAdvisorAndroidTest)
    unittest.TextTestRunner(verbosity=1).run(suite)
