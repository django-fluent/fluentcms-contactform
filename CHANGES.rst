Changelog
=========

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
