from selenium import webdriver
from util_selenium import *
import os
import time

class AccountLogin:
    def __init__(self, config, driver, username, password):
        self.config = config
        self.driver = driver
        self.wait_time = config.wait_time

        ## window size ##
        self.width = config.width
        self.height = config.height

        self.login(username, password)

        ## timeline
        self.tweets = []

    
    def login(self, username, password):

        mydriverget(self.driver, self.config.login_url, self.wait_time)

        field_username = self.driver.find_element_by_xpath(self.config.xpath_username)
        field_password = self.driver.find_element_by_xpath(self.config.xpath_password)

        field_username.send_keys(username)
        field_password.send_keys(password)

        login_button = self.driver.find_element_by_xpath(self.config.xpath_button)

        mydriverclick(login_button, self.driver, self.wait_time)

        self.driver.set_window_size(self.width, self.height)

    def search_latest(self, query):
        

        url = 'https://twitter.com/search?q=' + query + '&src=typed_query'
        mydriverget(self.driver, url, self.wait_time)
        latest_button = self.driver.find_element_by_xpath(self.config.xpath_latest)
        mydriverclick(latest_button, self.driver, self.wait_time)

    def scroll3(self, skip = None):
        scroll_page3(self.driver, self.wait_time, skip)

    def scroll1(self):
        scroll_page(self.driver, self.wait_time)

    def follow_rec(self):

        n_follow = 0

        mydriverget(self.driver, self.config.base_url, self.wait_time)
        time.sleep(3)
        but_showrec = mytrygetel(self.driver.find_element_by_xpath, self.config.xpath_showrec)

        if but_showrec == None:
            print("error!!")
            return 0
        else:
            but_showrec.click()

            follow_list = mytrygetel(self.driver.find_elements_by_xpath, self.config.xpath_followbut)
            if follow_list == None:
                return 0
            else:
                for but in follow_list:
                    child = mytrygetel(but.find_element_by_xpath, "./div")
                    if child != None:
                        child.click()
                        n_follow += 1
        
        return n_follow