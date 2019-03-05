======
README
======

This application allows various webmaster tools to verify that a Django site is
managed by you.

The only supported method of verification is by accessing a file on your
server.

Supported services:

- `Google Webmaster Tools <https://www.google.com/webmasters/tools/home>`_
- `Bing Webmaster Tools <https://ssl.bing.com/webmaster/Home/>`_
- `Yandex Webmaster Tools <http://webmaster.yandex.com/>`_
- `Mail.ru Webmaster Tools <http://webmaster.mail.ru/>`_
- `Mail.ru Seosan Tools <https://seosan.mail.ru/>`_
- `Majestic SEO <https://www.majesticseo.com>`_
- `Alexa <http://www.alexa.com>`_

.. image:: https://travis-ci.org/whyflyru/django-webmaster-verification.svg?branch=master
    :target: https://travis-ci.org/whyflyru/django-webmaster-verification

Usage
=====

Get ``django-webmaster-verification`` into your python path::

    pip install django-webmaster-verification

Add ``webmaster_verification`` to your INSTALLED_APPS in settings.py::

    INSTALLED_APPS = (
        ...,
        'webmaster_verification',
        ...,
    )

Add ``webmaster_verification`` to your root urlconf (urls.py)::

    urlpatterns = [
        ...,
        url(r'', include('webmaster_verification.urls')),
        ...,
    ]

Add optional settings::

    WEBMASTER_VERIFICATION_USE_SUBDOMAINS = True  # enable subdomains support (disabled by default)
    WEBMASTER_VERIFICATION_USE_CACHE = True  # enable cache (disabled by default)
    WEBMASTER_VERIFICATION_CACHE_LIFETIME = 360  # cache life time in seconds (default - 5 minutes)

Add verification data in your admin interface.

Notes
-----

As **Bing** always accesses the same verification file I'm not sure if it's
possible to support more than one code for it. Please let me know if yes, and
how, as I don't really use their tools.

The **Alexa** codes I saw all had a length of 27 characters, so that's what this
app assumes is used. Please let me know if your codes differ and I need to
modify the app.

Changelog
=========

0.4.1+whyfly.2 (2019-03-05)
---------------------------
- Better package version
- Add support of Mail.Ru services
- Correct verification template for Yandex
- Store verification codes in database
- Add support of subdomains

0.4.0 (2019-01-26)
------------------
- Use docker-based travis testing
- Test against Django >=1.11
- Removed tests for Python 3.4, add 3.6
- I only ran the tests, I don't think I use it on any prod site right now

0.3.0 (2016-02-20)
------------------
- Python 2.7 and Django 1.8 are required

0.2.4 (2015-02-26)
------------------
- Add Django 1.8 (beta1) support and drop 1.5 tests

0.2.3 (2014-04-13)
------------------
- Django 1.7 (beta1) support

0.2.2 (2014-01-12)
------------------
- Django 1.6 support
- Removed Python 2.5 testing

0.2.1 (2013-03-25)
------------------
- Add alexa support
- Refactor the test project to use a different structure

0.2 (2013-02-16)
----------------
- Python 3.2 support
- Integrate testing with travis

0.1.10 (2012-12-21)
-------------------
- Fix test errors when running from a real project

0.1.9 (2012-12-19)
------------------
- Pypi updates

0.1.8 (2012-12-19)
------------------
- Yandex Webmaster Tools support added.

0.1.7 (2012-05-07)
------------------
- Bugfix for multiple verification codes for one provider.
