# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.test.utils import override_settings
from django.utils import timezone

from .models import Verification
from .views import YandexVerificationView, GoogleVerificationView


class WebmasterVerificationTest(TestCase):
    def setUp(self):
        self.client = Client()

    def _get_google_url(self, code):
        return '/google%s.html' % code

    def test_google(self):
        code = '0123456789abcdef'
        Verification.objects.create(
            code=code,
            provider=Verification.PROVIDER_GOOGLE
        )
        url = self._get_google_url(code)
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            200,
            "Couldn't access %s, got %d" % (url, response.status_code)
        )
        self.assertRegexpMatches(
            str(response.content),
            '.*google%s\.html.*' % code,
            'Verification code not found in response body',
        )

        bad_codes = (
            '',
            '012345678',
        )
        for code in bad_codes:
            url = self._get_google_url(code)
            response = self.client.get(url)
            self.assertEqual(
                response.status_code,
                404,
                "Could access %s for inexistent code, got %d" % (url, response.status_code)
            )

    def test_bing(self):
        code = 'FFFFFFFFFFFFFFFF'
        Verification.objects.create(
            code=code,
            provider=Verification.PROVIDER_BING
        )
        url = '/BingSiteAuth.xml'
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            200,
            "Couldn't access %s, got %d" % (url, response.status_code)
        )
        self.assertEqual(
            response['Content-Type'],
            'text/xml',
            'Got %s content type for xml file' % response['Content-Type']
        )
        self.assertRegexpMatches(
            str(response.content),
            '.*%s.*' % code,
            'Verification code not found in response body',
        )

    def _get_yandex_url(self, code):
        return '/yandex_%s.html' % code

    def test_yandex(self):
        code = '0123456789abcdef'
        Verification.objects.create(
            code=code,
            provider=Verification.PROVIDER_YANDEX
        )
        url = self._get_yandex_url(code)
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            200,
            "Couldn't access %s, got %d" % (url, response.status_code)
        )
        self.assertEqual(
            response['Content-Type'],
            'text/html; charset=utf-8',
            'Got %s content type for text file' % response['Content-Type']
        )

        bad_codes = (
            '',
            '012345678',
            '0123456789ABCDEF0123456789ABCDEF',
        )
        for code in bad_codes:
            url = self._get_yandex_url(code)
            response = self.client.get(url)
            self.assertEqual(
                response.status_code,
                404,
                'Could access %s for inexistent code, got %d' % (url, response.status_code)
            )

    def _get_webmaster_mailru(self, code):
        return '/wmail_%s.html' % code

    def test_webmaster_mailru(self):
        code = '0123456789abcdef0123456789abcdef'
        Verification.objects.create(
            code=code,
            provider=Verification.PROVIDER_WEBMASTER_MAILRU
        )
        url = self._get_webmaster_mailru(code)
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            200,
            "Couldn't access %s, got %d" % (url, response.status_code)
        )
        self.assertEqual(
            response['Content-Type'],
            'text/html; charset=utf-8',
            'Got %s content type for text file' % response['Content-Type']
        )
        self.assertRegexpMatches(
            str(response.content),
            '.*%s.*' % code,
            'Verification code not found in response body',
        )

        bad_codes = (
            '',
            '012345678',
            '0123456789abcdef',
        )
        for code in bad_codes:
            url = self._get_webmaster_mailru(code)
            response = self.client.get(url)
            self.assertEqual(
                response.status_code,
                404,
                'Could access %s for inexistent code, got %d' % (url, response.status_code)
            )

    def _get_seosan_mailru(self, code):
        return '/mailru-verification%s.html' % code

    def test_seosan_mailru(self):
        code = '0123456789abcdef'
        Verification.objects.create(
            code=code,
            provider=Verification.PROVIDER_SEOSAN_MAILRU
        )
        url = self._get_seosan_mailru(code)
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            200,
            "Couldn't access %s, got %d" % (url, response.status_code)
        )
        self.assertEqual(
            response['Content-Type'],
            'text/html; charset=utf-8',
            'Got %s content type for text file' % response['Content-Type']
        )
        self.assertRegexpMatches(
            str(response.content),
            '.*%s.*' % code,
            'Verification code not found in response body',
        )

        bad_codes = (
            '',
            '012345678',
            'abcdef0123456789',
            '0123456789abcdef9876543210fedcba',
        )
        for code in bad_codes:
            url = self._get_seosan_mailru(code)
            response = self.client.get(url)
            self.assertEqual(
                response.status_code,
                404,
                'Could access %s for inexistent code, got %d' % (url, response.status_code)
            )

    def _get_mj_url(self, code):
        return '/MJ12_%s.txt' % code

    def test_majestic(self):
        code = 'AFAFAFAFAFAFAFAFAFAFAFAFAFAFAFAF'
        Verification.objects.create(
            code=code,
            provider=Verification.PROVIDER_MAJESTIC
        )
        url = self._get_mj_url(code)
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            200,
            "Couldn't access %s, got %d" % (url, response.status_code)
        )
        self.assertEqual(
            response['Content-Type'],
            'text/plain',
            'Got %s content type for text file' % response['Content-Type']
        )

        bad_codes = (
            '',
            '012345678',
            '0123456789ABCDEF0123456789ABCDEF',
        )
        for code in bad_codes:
            url = self._get_mj_url(code)
            r = self.client.get(url)
            self.assertEqual(
                r.status_code,
                404,
                'Could access %s for inexistent code, got %d' % (url, r.status_code)
            )

    def _get_alexa_url(self, code):
        return '/%s.html' % code

    def test_alexa(self):
        code = '1234567890abcdefABCDEF12345'
        Verification.objects.create(
            code=code,
            provider=Verification.PROVIDER_ALEXA
        )
        url = self._get_alexa_url(code)
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            200,
            "Couldn't access %s, got %d" % (url, response.status_code)
        )

        bad_codes = (
            '',
            '012345678',
            '0123456789ABCDEF0123456789ABCDEF',
        )
        for code in bad_codes:
            url = self._get_alexa_url(code)
            r = self.client.get(url)
            self.assertEqual(
                r.status_code,
                404,
                'Could access %s for inexistent code, got %d' % (url, r.status_code)
            )

    @override_settings(WEBMASTER_VERIFICATION_USE_SUBDOMAINS=True)
    def test_subdomains(self):
        code = '0123456789abcdef'
        Verification.objects.create(
            code=code,
            provider=Verification.PROVIDER_YANDEX,
            subdomain='msk'
        )
        url = self._get_yandex_url(code)
        request_factory = RequestFactory()
        request = request_factory.get(url)

        def do_request():
            return YandexVerificationView.as_view()(request, code=code)

        self.assertRaises(Http404, do_request)

        request.subdomain = 'msk'
        setattr(request, 'subdomain', 'msk')
        response = do_request()
        self.assertEqual(
            response.status_code,
            200,
            "Couldn't access %s, got %d" % (url, response.status_code)
        )

    @override_settings(WEBMASTER_VERIFICATION_USE_CACHE=True)
    def test_cache(self):
        code = '0123456789abcdef'
        verification = Verification.objects.create(
            code=code,
            provider=Verification.PROVIDER_GOOGLE
        )
        url = self._get_google_url(code)
        request_factory = RequestFactory()
        request = request_factory.get(url)
        view_instance = GoogleVerificationView()
        view = GoogleVerificationView.as_view()

        # getting from database, cache value
        response = view(request, code=code)
        self.assertEqual(
            response.status_code,
            200,
            "Couldn't access %s, got %d" % (url, response.status_code)
        )
        response = response.render()
        self.assertIn(code, response.content.decode('utf-8'))
        cache_key = 'google_%s' % code
        self.assertIn(cache_key, view_instance._cache)
        self.assertIn('code', view_instance._cache[cache_key])
        self.assertIn('expire', view_instance._cache[cache_key])
        self.assertEqual(view_instance._cache[cache_key]['code'], code)

        # getting from cache
        changed_code = 'abcdef0123456789'
        verification.code = changed_code
        verification.save()
        response = view(request, code=code)
        response = response.render()
        self.assertIn(code, response.content.decode('utf-8'))

        # cache was expired
        view_instance._cache[cache_key]['expire'] = timezone.datetime.now() - timezone.timedelta(minutes=7)
        self.assertRaises(Http404, view, request, code=code)
        response = view(request, code=changed_code)
        self.assertEqual(
            response.status_code,
            200,
            "Couldn't access %s, got %d" % (url, response.status_code)
        )
