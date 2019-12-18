from rest_framework.response import Response
from rest_framework import status

import ast

class TranslationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        lang = request.headers['Accept-language'][:2]
        if lang not in ['en', 'fa']:
            lang = 'fa'

        if hasaatr(response, 'data'):
            data = ast.literal_eval(response.data)
            response.data = self.translate(data, lang)

        return response

    def translate(self, data, lang):
        if isinstance(data, dict):
            if len(data.keys()) == 2 and 'en' in data.keys() and 'fa' in data.keys():
                return data[lang]
            for key in data:
                data[key] = self.translate(data[key], lang)
        elif isinstance(data, list):
            for i in range(len(data)):
                data[i] = self.translate(data[i], lang)
        return data

