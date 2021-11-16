from flask import Flask, request
from flask_restful import Resource, Api

from SeleniumCollector import SeleniumCollector
import requests

app = Flask(__name__)
api = Api(app)


class SeleniumController(Resource):

    def post(self):
        
        json = request.json
        if request.json['domainId'] is not None:
            domainId = request.json['domainId']
        urlPath = request.json['urlPath']
        if request.json['timeout'] is not None:
            timeout = request.json['timeout']
        else:
            timeout = 10
        if request.json['delay'] is not None:
            delay = request.json['delay']
        else:
            delay = 1
        print(urlPath)
        generatedSnapshot = request.json['generatedSnapshot']
        # verifyExternalResources = request.json['verifyExternalResources']
        verifyCookies = request.json['verifyCookies']
        verifyContent = request.json['verifyContent']
        verifyLocalStorage = request.json['verifyLocalStorage']
        verifySessionStorage = request.json['verifySessionStorage']
        redirectTest = request.json['redirectTest']
        verifyCertificate = request.json['verifyCertificate']

        if 'verifyPath' not in json:
            verifyPaths = False
        else:
            verifyPaths = request.json['verifyPath']
        if 'verifySimpleCookies' not in json:
            verifySimpleCookies = False
        else:
            verifySimpleCookies = request.json['verifySimpleCookies']
        if 'newVersion' not in json:
            newVersion = False
        else:
            newVersion = request.json['newVersion']
        if 'post' in json:
            body = request.json['post']
            response = requests.post(urlPath, data=body)
            result = response
            return result


        seleniumService = SeleniumCollector(domainId, urlPath, timeout, delay, generatedSnapshot,
                                            verifyCookies, verifyContent,
                                            verifyLocalStorage, verifySessionStorage, redirectTest,
                                            verifyCertificate, verifyPaths, verifySimpleCookies, newVersion)
        result = seleniumService.collector()
        return result


api.add_resource(SeleniumController, '/collector')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
