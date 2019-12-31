Overview
========

This is a complete python implementation of the Fitbark API.

It uses OAuth2 for authentication.

Quickstart
==========

Here is an example of authorizing with OAuth 2.0::

  # You'll have to gather the tokens on your own, or use
  # ./gather_keys_oauth2.py
  authd_client = pyfitbark.FitbarkApi('<consumer_key>', '<consumer_secret>',
                                 access_token='<access_token>', refresh_token='<refresh_token>')
  authd_client.sleep()

FitbarkApi
===========

Some assumptions you should note. Anywhere it says date=None, it should accept
either ``None`` or a ``date`` or ``datetime`` object
(anything with proper strftime will do), or a string formatted
as ``%Y-%m-%d``.

.. autoclass:: pyfitbark.FitbarkApi
    :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
