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

    def reply(self):
        data = json_body(self.request)
        translate_text = data.get('translate_text', None)
        source_lang = data.get('source_lang', None)
        target_lang = data.get('target_lang', None)
        if not all([translate_text, source_lang, target_lang]):
            raise BadRequest("Missing required params: translated_text, source_lang, target_lang")

        URL = 'https://www.googleapis.com/language/translate/v2'
        key = api.portal.get_registry_record('plone.google_translation_key')
        data = {
            'key': key,
            'source': source_lang,
            'target': target_lang,
            'q': json.dumps(translate_text) if isinstance(translate_text, list) else translate_text
        }

        data = urllib.parse.urlencode(data).encode()
        req = urllib.request.Request(URL, data=data)
        try:
            r = urllib.request.urlopen(req, timeout=10)
        except Exception as e:  # noqa
            return {'error': 'no_more_quota'}

        translated = json.loads(r.read())['data']['translations'][0]['translatedText']
        if isinstance(translate_text, list):
            translated = html.unescape(translated)
            translated = translated.replace('" text"', '"text"').replace('"text "', '"text"')
            translated = translated.replace('" children"', '"children"').replace('"children "', '"children"')
            translated = json.loads(translated)
        else:
            translated = html.unescape(translated)

        return {'translated_text': translated}
