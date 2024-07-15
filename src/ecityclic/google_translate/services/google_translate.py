# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from zExceptions import BadRequest

import html
import json
import urllib


class GoogleTranslatePost(Service):
    """ GoogleTranslatePost
    """

    URL = 'https://www.googleapis.com/language/translate/v2'

    def reply(self):
        self.error = False
        data = json_body(self.request)
        translate_text = data.get('translate_text', None)
        source_lang = data.get('source_lang', None)
        target_lang = data.get('target_lang', None)
        if not all([translate_text, source_lang, target_lang]):
            raise BadRequest("Missing required params: translated_text, source_lang, target_lang")

        API_KEY = api.portal.get_registry_record('plone.google_translation_key')
        translated = self.translate(API_KEY, source_lang, target_lang, translate_text)
        if self.error:
            return {'translated_text': {'error': 'no_more_quota'}}

        return {'translated_text': translated}

    def translate(self, API_KEY, source_lang, target_lang, translate_text):
        if isinstance(translate_text, list):
            return self.translate_list(API_KEY, source_lang, target_lang, translate_text)

        translate_text = translate_text.replace('\xa0', ' ')
        data = {
            'key': API_KEY,
            'source': source_lang,
            'target': target_lang,
            'q': translate_text
        }

        data = urllib.parse.urlencode(data).encode()
        req = urllib.request.Request(self.URL, data=data)
        try:
            r = urllib.request.urlopen(req, timeout=10)
        except Exception as e:  # noqa
            self.error = True
            return {'error': 'no_more_quota'}

        translated = json.loads(r.read())['data']['translations'][0]['translatedText']
        translated = html.unescape(translated)
        return translated

    def translate_list(self, API_KEY, source_lang, target_lang, translate_text):
        for child in translate_text:
            self.translate_dict(API_KEY, source_lang, target_lang, child)
        return translate_text

    def translate_dict(self, API_KEY, source_lang, target_lang, translate_text):
        for key in translate_text:
            if key == 'children':
                self.translate_list(API_KEY, source_lang, target_lang, translate_text[key])
            if key == 'text':
                translate_text[key] = self.translate(API_KEY, source_lang, target_lang, translate_text[key])
