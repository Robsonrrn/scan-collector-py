import time
import os
import time
import uuid
from shutil import rmtree
from urllib.parse import urlparse

from seleniumwire import webdriver

from CookiesService import CookiesService


class SeleniumCollectorNew:

    def __init__(self, domainId, urlPath, timeout, delay, paths):
        self.domainId = domainId
        self.urlPath = urlPath
        self.timeout = timeout
        self.delay = delay
        self.paths = paths

    def collector(self):
        try:
            root = dict()
            navigation = dict()
            sessionChrome = str(uuid.uuid4())
            pathProfile = self.createProfileDir(sessionChrome)
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--user-data-dir=" + pathProfile)
            chrome_options.add_argument("--profile-directory=Default")
            chrome_options.add_argument("--ignore-certificate-errors")

            chromeDriver = webdriver.Chrome(chrome_options=chrome_options)
            chromeDriver.set_page_load_timeout(self.timeout)

            chromeDriver.get(self.urlPath)

            for path in self.paths:
                urlPathScan = self.urlPath + path
                script = "window.open('{}', '_blank');".format(urlPathScan)
                print(script)
                chromeDriver.execute_script(script)

                cookieService = CookiesService(pathProfile + "/Default/" + "Cookies")
                cookies = cookieService.getCookiesByDomainId()

                navigation['cookies'] = cookies
                navigation['cookies'] = chromeDriver.get_cookies()
                time.sleep(2)

                paths = []
                elems = chromeDriver.find_elements_by_xpath("//a[@href]")
                for elem in elems:
                    url = elem.get_attribute("href")
                    path = urlparse(url).path
                    if "#" in path:
                        path = path[:path.index("#")]
                    if path not in paths:
                        if path.startswith("/"):
                            paths.append(path)
                time.sleep(1)

                navigation['paths'] = paths
            chromeDriver.implicitly_wait(self.delay)
            time.sleep(self.delay)
        except Exception as e:
            e.with_traceback()
            print("------", e)
            chromeDriver.quit()
        finally:
            chromeDriver.quit()
            print("------------", pathProfile)
            rmtree(pathProfile)

        root['navigation'] = navigation

        return root

    def createProfileDir(self, domainId):
        #parentDir = "/Users/robertselddon/Desktop/"
        parentDir = "/home/ubuntu/Desktop/chrome_profiles/"
        path = os.path.join(parentDir, domainId)
        if not os.path.isdir(path):
            os.mkdir(path)
        return path
