from rest_framework.response import Response
import re

Always200MiddlewarePathExceptions = ('/api/accounts/login', '/api/accounts/profile')
Always200MiddlewareStatusCodeExceptions = (401,)


class TranslationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        lang = request.headers['Accept-language'][:2]
        if lang not in ['en', 'fa']:
            lang = 'fa'

        if hasattr(response, 'data'):
            data = self.translate(response.data, lang)
            r = Response(data)
            try:
                r.accepted_renderer = response.accepted_renderer
                r.accepted_media_type = response.accepted_media_type
                r.renderer_context = response.renderer_context
            finally:
                r.render()
            return r
        return response

    def translate(self, data, lang):
        if isinstance(data, dict):
            new_data = {}
            for field in data:
                if re.match('^(.*)_en', field):
                    name = field[:-3]
                    if name + '_fa' in data:
                        new_data[name] = data[name + '_' + lang]
                        new_data[name + '_fa'] = data[name + '_fa']
                        new_data[name + '_en'] = data[name + '_en']
                elif not re.match('^(.*)_fa', field):
                    new_data[field] = self.translate(data[field], lang)
            return new_data
        elif isinstance(data, list):
            for i in range(len(data)):
                self.translate(data[i], lang)
        elif isinstance(data, str):
            return data


class Always200Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if hasattr(response, 'data'):
            if isinstance(response.data, dict):
                if request.path in Always200MiddlewarePathExceptions or \
                        response.status_code in Always200MiddlewareStatusCodeExceptions:
                    pass
                else:
                    data = response.data
                    data['status_code'] = response.status_code
                    try:
                        r = Response(data=data, status=200)
                        r.accepted_renderer = response.accepted_renderer
                        r.accepted_media_type = response.accepted_media_type
                        r.renderer_context = response.renderer_context
                        r.render()
                        return r
                    except Exception:
                        pass
        return response


class WrapSerializerErrorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 400:
            if hasattr(response, 'data'):
                data = {'detail': response.data}
                try:
                    r = Response(data=data, status=400)
                    r.accepted_renderer = response.accepted_renderer
                    r.accepted_media_type = response.accepted_media_type
                    r.renderer_context = response.renderer_context
                    r.render()
                    return r
                except Exception:
                    pass
            return response
        else:
            return response
