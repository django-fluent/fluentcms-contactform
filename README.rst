.. image:: https://img.shields.io/travis/edoburu/fluentcms-contactform/master.svg?branch=master
    :target: http://travis-ci.org/edoburu/fluentcms-contactform
.. image:: https://img.shields.io/pypi/v/fluentcms-contactform.svg
    :target: https://pypi.python.org/pypi/fluentcms-contactform/
.. image:: https://img.shields.io/pypi/l/fluentcms-contactform.svg
    :target: https://pypi.python.org/pypi/fluentcms-contactform/
.. image:: https://img.shields.io/codecov/c/github/edoburu/fluentcms-contactform/master.svg
    :target: https://codecov.io/github/edoburu/fluentcms-contactform?branch=master

fluentcms-contactform
=====================

A plugin for django-fluent-contents_ to show a simple contact form.

Features:

* Configurable fields.
* Configurable layouts.
* Phone number validation.
* IP-Address detection.
* Admin panel with submitted messages.
* Email notification to staff members for new messages.
* Optional capcha / reCAPTCHA support.

Installation
============

First install the module, preferably in a virtual environment. It can be installed from PyPI::

    pip install fluentcms-contactform


Backend Configuration
---------------------

First make sure the project is configured for django-fluent-contents_.

Then add the following settings:

.. code-block:: python

    INSTALLED_APPS += (
        'fluentcms_contactform',
        'crispy_forms',    # for default template
    )

The database tables can be created afterwards::

    ./manage.py migrate

Now, the ``ContactFormPlugin`` can be added to your ``PlaceholderField``
and ``PlaceholderEditorAdmin`` admin screens.

Make sure the following settings are configured:

.. code-block:: python

    DEFAULT_FROM_EMAIL = '"Your Name" <you@example.org>'

    FLUENTCMS_CONTACTFORM_VIA = "Sitename"    # Will send a From: "Username via Sitename" email.

To have bootstrap 3 layouts, add:

.. code-block:: python

    CRISPY_TEMPLATE_PACK = 'bootstrap3'


IP address detection
~~~~~~~~~~~~~~~~~~~~

This package stores the remote IP of the visitor in the model.
The IP Address is read from the ``REMOTE_ADDR`` meta field.
In case your site is behind a HTTP proxy (e.g. using Gunicorn or a load balancer),
this would make all contact form submissions appear to be sent from the load balancer IP.

The best and most secure way to fix this, is using WsgiUnproxy_ middleware in your ``wsgi.py``:

.. code-block:: python

    from django.core.wsgi import get_wsgi_application
    from django.conf import settings
    from wsgiunproxy import unproxy

    application = get_wsgi_application()
    application = unproxy(trusted_proxies=settings.TRUSTED_X_FORWARDED_FOR_IPS)(application)

In your ``settings.py``, you can define which hosts may pass the ``X-Forwarded-For``
header in the HTTP request. For example:

.. code-block:: python

    TRUSTED_X_FORWARDED_FOR_IPS = (
        '11.22.33.44',
        '192.168.0.1',
    )


Updating the form layout
~~~~~~~~~~~~~~~~~~~~~~~~

The default form fields can be changed using:

.. code-block:: python

    FLUENTCMS_CONTACTFORM_DEFAULT_FIELDS = ('name', 'email', 'phone_number', 'subject', 'message')

    # default CSS styles
    CRISPY_TEMPLATE_PACK = 'bootstrap3'
    FLUENTCMS_CONTACTFORM_FORM_CSS_CLASS = 'form-horizontal'
    FLUENTCMS_CONTACTFORM_LABEL_CSS_CLASS = 'col-xs-3'
    FLUENTCMS_CONTACTFORM_FIELD_CSS_CLASS = 'col-xs-9'

For example, the subject can be removed using:

.. code-block:: python

    FLUENTCMS_CONTACTFORM_DEFAULT_FIELDS = ('name', 'email', 'phone_number', 'message')


Adding form fields
~~~~~~~~~~~~~~~~~~

The form layout is fully configurable, as you can select your own form classes.
The default settings are:

.. code-block:: python

    FLUENTCMS_CONTACTFORM_STYLES = (
        ('default', {
            'title': _("Default"),
            'form_class': 'fluentcms_contactform.forms.default.DefaultContactForm',
            'required_apps': (),
        }),
        ('captcha', {
            'title': _("Default with captcha"),
            'form_class': 'fluentcms_contactform.forms.captcha.CaptchaContactForm',
            'required_apps': ('captcha',),
        }),
        ('recaptcha', {
            'title': _("Default with reCAPTCHA"),
            'form_class': 'fluentcms_contactform.forms.recaptcha.ReCaptchaContactForm',
            'required_apps': ('captcha',),
        }),
    )

You can provide any form class, as long as it inherits from ``fluentcms_contactform.forms.AbstractContactForm``.
The current implementation expects the form to be a model form,
so any submitted data is safely stored in the database too.

By providing a ``helper`` function, the form fields received default styling from django-crispy-forms_.
See the provided form code in ``fluentcms_contactform.forms`` for examples.

The form is rendered with the ``fluentcms_contactform/forms/*name*.html`` template.

Displaying phone numbers
~~~~~~~~~~~~~~~~~~~~~~~~

The phone number field uses django-phonenumber-field_ to validate the phone number.
By default, it requires an international notation starting with ``+``.
The ``PhoneNumberField`` can support national phone numbers too, 
which is useful when most visitors come from a single country.
Update the ``PHONENUMBER_DEFAULT_REGION`` setting to reflect this.

For example, to auto insert a ``+31`` prefix for Dutch phone numbers, use:

.. code-block:: python

    PHONENUMBER_DEFAULT_REGION = 'NL'   # Your country code, eg. .NL to 

The phone numbers can be displayed in various formats, the most human readable is:

.. code-block:: python

    PHONENUMBER_DEFAULT_FORMAT = 'NATIONAL'

The supported formats are:

* ``NATIONAL`` - nicely space separated, remove the country prefix.
* ``INTERNATIONAL`` - nicely space separated
* ``E164`` - all numbers, suitable for data transmission.
* ``RFC3966`` - the ``tel:`` URL, suitable for URL display.


Displaying captcha's
~~~~~~~~~~~~~~~~~~~~

The ``fluentcms_contactform.forms.captcha`` provides an example to create a captcha form.
This requires a properly installed django-simple-captcha_ form::

    pip install django-simple-captcha

In ``settings.py``:

.. code-block:: python

    INSTALLED_APPS += (
        'captcha',
    )

In ``urls.py``:

.. code-block:: python

    urlpatterns = [
        # ...

        url(r'^api/captcha/', include('captcha.urls')),

    ]

Add the database tables::

    python manage.py migrate

And optional settings to simplify the captcha:

.. code-block:: python

    CAPTCHA_NOISE_FUNCTIONS = ()
    CAPTCHA_FONT_SIZE = 30
    CAPTCHA_LETTER_ROTATION = (-10,10)

This can be made more complicated when needed:

.. code-block:: python

    CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
    CAPTCHA_NOISE_FUNCTIONS = (
        'captcha.helpers.noise_arcs',
        'captcha.helpers.noise_dots',
    )

See the documentation of django-simple-captcha_ for more examples.

Using reCAPTCHA
~~~~~~~~~~~~~~~

In a similar way, you can use recapcha. Select the form option,
and make sure everything is installed::

    pip install django-recaptcha

In ``settings.py``:

.. code-block:: python

    INSTALLED_APPS += (
        'captcha',
    )

    RECAPTCHA_PUBLIC_KEY = '...'
    RECAPTCHA_PRIVATE_KEY = '...'
    RECAPTCHA_USE_SSL = True
    NOCAPTCHA = True  # Use the new nocapcha

See the documentation of django-recaptcha_ for more details.

.. warning::
    Don't install both django-simple-captcha_ and django-recaptcha_ as they both install
    a ``captcha`` package in the same location.


Frontend Configuration
----------------------

If needed, the HTML code can be overwritten by redefining ``fluentcms_contactform/forms/*.html``.

The template filename corresponds with the form style defined in ``FLUENTCMS_CONTACTFORM_STYLES``.
When no custom template is defined, ``fluentcms_contactform/forms/default.html`` will be used.

The staff email message can be updated by redefining ``fluentcms_contactform/staff_email/*.txt``,
which works similar to the form templates.


Contributing
------------

If you like this module, forked it, or would like to improve it, please let us know!
Pull requests are welcome too. :-)

.. _django-fluent-contents: https://github.com/edoburu/django-fluent-contents
.. _django-phonenumber-field: https://github.com/stefanfoulis/django-phonenumber-field
.. _django-simple-captcha: https://github.com/mbi/django-simple-captcha
.. _django-recaptcha: https://github.com/praekelt/django-recaptcha
.. _django-crispy-forms: https://github.com/maraujop/django-crispy-forms
.. _WsgiUnproxy: https://pypi.python.org/pypi/WsgiUnproxy
