Changelog
=========

Changes in git
--------------

* Prepare for Django 1.11 support (awaits dependencies)
* **NOTE:** As of Django 1.11, make sure ``{% autoescape off %}`` is used in the ``.txt`` templates.
  Previously, this behavior could be controlled from Python code.
  That is no longer possible as of Django 1.11.


Version 1.3.3 (2016-08-19)
--------------------------

* Avoid Django migrations change when changing ``FORM_STYLE_CHOICES``.


Version 1.3.2 (2016-08-07)
--------------------------

* Fixed Python 3 support.


Version 1.3.1 (2016-07-29)
--------------------------

* Added ``type="tel"`` for phone number field.
* Fix shortened placeholder text for phone number field.


Version 1.3 (2016-07-29)
------------------------

* Added a new "compact" form style.
  This form style displays the name/email/phone_number fields in a single (Bootstrap 3) column.


Version 1.2 (2016-07-19)
------------------------

* Support multiple forms at the same page.
* Fix default layout on mobile, avoid horizontal columns for label/inputs.


Version 1.1 (2016-02-03)
------------------------

* Added Django 1.9 support
* Removed ``FLUENTCMS_CONTACTFORM_IP_RESOLVER`` setting.
  Use WsgiUnproxy_ for proper IP resolving when the site exists behind a load balancer or HTTP proxy.


Version 1.0 (2015-10-24)
------------------------

* First release

.. _WsgiUnproxy: https://pypi.python.org/pypi/WsgiUnproxy
