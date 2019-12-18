from rest_framework.response import Response
from rest_framework import status

import re


class TranslationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        lang = request.headers['Accept-language'][:2]
        if lang not in ['en', 'fa']:
            lang = 'fa'

        if hasattr(response, 'data'):
            print('AAAAAAAAA')
            print(response.data)
            self.translate(response.data, lang)
            response.data['x'] = 'y'

        return response

    def translate(self, data, lang):
        print(data)
        if isinstance(data, dict):
            new_data = {}
            for field in data:
                if isinstance(data[field], str):
                    if re.match('(.*)_en', field) or re.match('(.*)_fa', field):
                        name = field[:-3]
                        data[name + '_en'] = data[name + '_fa'] = data[name + '_' + lang]
                else:
                    self.translate(data[field], lang)
        elif isinstance(data, list):
            for i in range(len(data)):
                self.translate(data[i], lang)

