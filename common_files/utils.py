import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome


'''
Tools made for indianfoodforever.com
'''


class WebScrapper(Chrome):
    def __init__(self, executable_path: str, options: Options):
        self.chrome = Chrome(executable_path=executable_path, options=options)

    def getSimilarObjects(self, xpath_string: str):
        HTMLObjects = self.chrome.find_elements(By.XPATH, xpath_string)
        for elem in HTMLObjects:
            print(elem)
