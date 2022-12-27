import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome


'''
Tools made for indianfoodforever.com
'''


class WebScrapper(Chrome):
    def __init__(self, get_url: str, executable_path: str, options: Options):
        self.chrome = Chrome(executable_path=executable_path, options=options)
        self.get_url = get_url

    def func_request(self, func_name, args):
        try:
            func = getattr(self, func_name)
            return True, func(**args)
        except Exception as e:
            print(format(str(e)))
            return False, str(e)

    def startDriver(self) -> None:
        self.chrome.get(self.get_url)

    def createNewTab(self):
        self.chrome.execute_script("window.open('');")
        self.chrome.switch_to.window(self.chrome.window_handles[-1])

    def closeTab(self):
        self.chrome.close()
        if self.chrome.window_handles[-1]:
            self.chrome.switch_to.window(self.chrome.window_handles[-1])

    def createChildScrapperInNewTab(self, get_url: str, steps: dict) -> dict:
        driver = self.chrome
        self.createNewTab()
        driver.get(get_url)
        res = {}
        for (step, args) in steps.items():
            status, data = self.func_request(step, args)
            res[get_url] = data
        self.closeTab()
        return res

    def createChildScrapper(self, get_url: str, executable_path: str, options: Options, steps: dict):
        _scrapper = WebScrapper(get_url, executable_path, options)
        for (step, args) in steps.items():
            status, data = _scrapper.func_request(step, args)
            print(data)
        _scrapper.close()

    def getSimilarObjects(self, xpath_string: str, getOptions: list = None) -> list:
        webObjects = self.chrome.find_elements(By.XPATH, xpath_string)
        if getOptions:
            res = {}
            for attribute in getOptions:
                res[attribute] = [elem.get_attribute(
                    attribute) for elem in webObjects]
            return res

        return webObjects

    def recurringAttributeScrapper(self, parent_item_options: dict, child_item_options: dict):
        categoryLinks = self.getSimilarObjects(
            xpath_string=parent_item_options['xpath'], getOptions=parent_item_options['attributes'])

        res = {}
        for categorylink in categoryLinks['href']:
            temp = self.createChildScrapperInNewTab(categorylink, steps={
                "getSimilarObjects": {'xpath_string': child_item_options['xpath'], 'getOptions': child_item_options['attributes']}
            })
            for attribute in child_item_options['attributes']:
                if attribute not in res:
                    res[attribute] = temp[categorylink][attribute]
                else:
                    res[attribute] += temp[categorylink][attribute]

        return res
