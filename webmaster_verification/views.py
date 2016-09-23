import logging

from django.conf import settings
from django.http import Http404
from django.views.generic import TemplateView
from django.utils import timezone

from .models import Verification


logger = logging.getLogger(__name__)


class MimeTextMixin(object):
    """
    Return text content type
    """
    def render_to_response(self, context, **kwargs):
        return super(MimeTextMixin, self).render_to_response(
            context,
            content_type='text/plain',
            **kwargs
        )


class MimeXMLMixin(object):
    """
    Return xml content type
    """
    def render_to_response(self, context, **kwargs):
        return super(MimeXMLMixin, self).render_to_response(
            context,
            content_type='text/xml',
            **kwargs
        )


class VerificationView(TemplateView):
    """
    This adds the verification key to the template context and makes sure we
    return a 404 if no key was set for the provider.
    """
    provider = None

    # cache data structure:
    # '{provider}_{code}': {
    #     'code': 'code_value',
    #     'expire': 'expire_date'
    # }
    _cache = {}

    @staticmethod
    def get_provider_name(provider):
        providers = dict(Verification.PROVIDERS)
        return providers[provider].lower()

    def get_cache_key(self, provider, code):
        provider_name = self.get_provider_name(provider)
        if provider == Verification.PROVIDER_BING:
            return provider_name
        else:
            return '%s_%s' % (provider_name, code)

    def set_cache_value(self, key, value):
        cache_life_time = getattr(settings, 'WEBMASTER_VERIFICATION_CACHE_LIFETIME', 300)
        self._cache[key] = {
            'code': value,
            'expire': timezone.datetime.now() + timezone.timedelta(seconds=cache_life_time)
        }

    def get_cache_value(self, key):
        try:
            value = self._cache[key]
        except KeyError:
            return None
        if value['expire'] > timezone.datetime.now():
            return value['code']
        else:
            del self._cache[key]
            return None

    def get_verification_code(self, **kwargs):
        """
        Get verification code from cache or from database depending on the settings
        :param kwargs: parameters for get method of query manager
        :return: verification code
        """
        use_cache = getattr(settings, 'WEBMASTER_VERIFICATION_USE_CACHE', False)
        code = kwargs.get('code')
        cache_key = self.get_cache_key(self.provider, code)
        if use_cache:
            code_value = self.get_cache_value(cache_key)
            if code_value:
                return code_value
        verification = Verification.objects.filter(**kwargs).first()
        if not verification:
            raise Http404
        code_value = verification.code
        self.set_cache_value(cache_key, code_value)
        return code_value

    def get_context_data(self, **kwargs):
        context = super(VerificationView, self).get_context_data(**kwargs)
        use_subdomains = getattr(settings, 'WEBMASTER_VERIFICATION_USE_SUBDOMAINS', False)
        provider_name = self.get_provider_name(self.provider)
        code = kwargs.get('code')
        params = {
            'provider': self.provider
        }
        if not self.provider == Verification.PROVIDER_BING:
            params['code'] = code
        if use_subdomains:
            params['subdomain'] = getattr(self.request, 'subdomain', '')
        verification_code = self.get_verification_code(**params)
        context['%s_verification' % provider_name] = verification_code
        return context


class GoogleVerificationView(VerificationView):
    template_name = 'webmaster_verification/google_verify_template.html'
    provider = Verification.PROVIDER_GOOGLE


class BingVerificationView(MimeXMLMixin, VerificationView):
    template_name = 'webmaster_verification/bing_verify_template.xml'
    provider = Verification.PROVIDER_BING


class MajesticVerificationView(MimeTextMixin, VerificationView):
    template_name = 'webmaster_verification/majestic_verify_template.txt'
    provider = Verification.PROVIDER_MAJESTIC


class YandexVerificationView(MimeTextMixin, VerificationView):
    template_name = 'webmaster_verification/yandex_verify_template.txt'
    provider = Verification.PROVIDER_YANDEX


class AlexaVerificationView(VerificationView):
    template_name = 'webmaster_verification/alexa_verify_template.html'
    provider = Verification.PROVIDER_ALEXA
