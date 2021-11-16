from flask import Flask, request
from flask_restful import Resource, Api

from SeleniumCollectorNew import SeleniumCollectorNew
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
        if request.json['paths'] is not None:
            paths = request.json['paths']

        if 'post' in json:
            body = request.json['post']
            response = requests.post(urlPath, data=body)
            result = response
            return result

        print("Entrou")
        seleniumService = SeleniumCollectorNew(domainId, urlPath, timeout, delay, paths)
        result = seleniumService.collector()
        return result


api.add_resource(SeleniumController, '/collector/new')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)
