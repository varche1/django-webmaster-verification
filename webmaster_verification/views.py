import logging

from django.conf import settings
from django.http import Http404
from django.views.generic import TemplateView

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

    def get_context_data(self, code, **kwargs):
        context = super(VerificationView, self).get_context_data(**kwargs)
        use_subdomains = getattr(settings, 'WEBMASTER_VERIFICATION_USE_SUBDOMAINS', False)
        try:
            if use_subdomains:
                verification = Verification.objects.get(
                    provider=self.provider,
                    code=code,
                    subdomain=getattr(self.request, 'subdomain', '')
                )
            else:
                verification = Verification.objects.get(
                    provider=self.provider,
                    code=code
                )
        except Verification.DoesNotExist:
            raise Http404
        provider_name = verification.get_provider_display().lower()
        context['%s_verification' % provider_name] = verification.code
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
