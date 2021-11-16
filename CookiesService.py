from CookiesRepository import CookiesRepository


class CookiesService:

    def __init__(self, dbDirFile):
        self.dbDirFile = dbDirFile

    def getCookiesByDomainId(self):
        cookiesRepository = CookiesRepository(self.dbDirFile)
        cookies = cookiesRepository.getCookiesByDomainId()

        cookiesList = []

        for cookie in cookies:
            dicCookies = dict()
            dicCookies['domain'] = cookie[1]
            dicCookies['expiry'] = cookie[5]
            dicCookies['httpOnly'] = cookie[7]
            dicCookies['name'] = cookie[2]
            dicCookies['path'] = cookie[4]
            dicCookies['secure'] = cookie[6]
            dicCookies['value'] = cookie[3]
            cookiesList.append(dicCookies)
        return cookiesList
