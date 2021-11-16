import datetime
import time
import uuid
import shutil
from CertificateService import CertificateService
from SnapshotService import SnapshotService
from seleniumwire import webdriver
from urllib.parse import urlparse
from CookiesService import CookiesService
import os
from shutil import rmtree

class SeleniumCollector:

    def __init__(self, domainId, urlPath, timeout, delay,
                 generatedSnapshot,
                 verifyCookies, verifyContent, verifyLocalStorage,
                 verifySessionStorage, redirectTest, verifyCertificate,
                 verifyPath, verifySimpleCookies, newVersion):
        self.domainId = domainId
        self.urlPath = urlPath
        self.timeout = timeout
        self.delay = delay
        self.generatedSnapshot = generatedSnapshot
        self.verifyCookies = verifyCookies
        self.verifyContent = verifyContent
        self.verifyLocalStorage = verifyLocalStorage
        self.verifyLocalStorage = verifyLocalStorage
        self.verifySessionStorage = verifySessionStorage
        self.redirectTest = redirectTest
        self.verifyCertificate = verifyCertificate
        self.verifyPath = verifyPath
        self.verifySimpleCookies = verifySimpleCookies
        self.newVersion = newVersion

    def collector(self):
        root = dict()
        navigation = dict()


        if self.verifyCertificate:
            urlDomain = urlparse(self.urlPath).netloc

            certificateService = CertificateService()
            certificate = certificateService.get_certificate(urlDomain, 443)
            navigation['certificate'] = certificate

        else:
            try:
                sessionChrome = str(uuid.uuid4())
                pathProfile = self.createProfileDir(sessionChrome)
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument("--user-data-dir=" + pathProfile)
                chrome_options.add_argument("--profile-directory=Default")
                chrome_options.add_argument("--ignore-certificate-errors")

                chromeDriver = webdriver.Chrome(chrome_options=chrome_options)

                chromeDriver.get(self.urlPath)
                chromeDriver.set_page_load_timeout(self.timeout)
                chromeDriver.implicitly_wait(self.delay)

                time.sleep(self.delay)

                #first_request = chromeDriver.requests[0]
                statusCode = 200
                print('******************************',  statusCode)

                if statusCode == 301:
                    root['httpsRedirect'] = True
                root['url'] = chromeDriver.current_url
                root['statusCode'] = statusCode

                if statusCode == 200 or statusCode == 400 or statusCode == 403 \
                        or statusCode == 302 or statusCode == 301:

                    if self.generatedSnapshot:
                        if self.newVersion:
                            self.createSnapshotNew(chromeDriver, navigation)
                        else:
                            self.createSnapshot(chromeDriver, navigation)
                    if self.verifyContent:
                        navigation['content'] = chromeDriver.page_source
                    if self.verifyCookies:
                        time.sleep(3)
                        cookieService = CookiesService(pathProfile + "/Default/" + "Cookies")
                        cookies = cookieService.getCookiesByDomainId()


                        navigation['cookies'] = cookies
                    if self.verifySimpleCookies:
                        navigation['cookies'] = chromeDriver.get_cookies()
                    if self.verifyPath:
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

                        navigation['paths'] = paths

                    # if self.verifyExternalResources:
                    #     resources = []
                    #
                    #     for request in chromeDriver.requests:
                    #         if request.response:
                    #             externalResources = dict()
                    #             externalResources['url'] = request.path
                    #             externalResources['statusCode'] = request.response.status_code
                    #             externalResources['method'] = request.method
                    #             if 'Content-Type' in request.response.headers:
                    #                 externalResources['contentType'] = request.response.headers['Content-Type']
                    #             resources.append(externalResources)
                    #     navigation['externalResources'] = resources
            except Exception as e:
                e.with_traceback()
                chromeDriver.quit()
            finally:
                chromeDriver.quit()
                print("------------", pathProfile)
                rmtree(pathProfile)

        root['navigation'] = navigation

        return root

    def createSnapshot(self, chromeDriver, navigation):
        domainNumber = round((self.domainId / 100) + 1)
        domainNumberString = format(domainNumber, '08d')
        subPath = str(uuid.uuid4())
        fileName = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        chromeDriver.save_screenshot(fileName + '.png')
        pathBucket = 'domains/' + domainNumberString + '/' + subPath + '/screenshot-desktop/' + fileName + '.png'
        snapshotService = SnapshotService(fileName + '.png', 'cdn-app-privally-io', pathBucket)
        urlSnapshot = snapshotService.upload_file()
        navigation['snapshot'] = urlSnapshot


    def createSnapshotNew(self, chromeDriver, navigation):
        subPath = str(uuid.uuid4())
        fileName = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        chromeDriver.save_screenshot(fileName + '.png')
        pathBucket = 'domains/' + self.domainId + '/' + subPath + '/screenshot-desktop/' + fileName + '.png'
        snapshotService = SnapshotService(fileName + '.png', 'cdn-app-privally-io', pathBucket)
        urlSnapshot = snapshotService.upload_file()
        navigation['snapshot'] = urlSnapshot


    def createProfileDir(self, domainId):
        #parentDir = "/Users/robertselddon/Desktop/"
        parentDir = "/home/ubuntu/Desktop/chrome_profiles/"
        path = os.path.join(parentDir, domainId)
        if not os.path.isdir(path):
            os.mkdir(path)
        return path
