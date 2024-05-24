# -*- coding: utf-8 -*-
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from zExceptions import BadRequest


class GoogleTranslatePost(Service):
    """ GoogleTranslatePost
    """

    def reply(self):
        data = json_body(self.request)
        translate_text = data.get('translate_text', None)
        if not translate_text:
            raise BadRequest("'translate_text' param is required")

        print('Text translated ---')
        print(f'Input: "{translate_text}"')
        print(f'Output: "{translate_text}"')
        return {'translated_text': translate_text}
