==========================
Welcome to django-allauth!
==========================

Integrated set of Django applications addressing authentication,
registration, account management as well as 3rd party (social) account
authentication.

Rationale
=========

Most existing Django apps that address the problem of social
authentication focus on just that. You typically need to integrate
another app in order to support authentication via a local
account.

This approach separates the worlds of local and social
authentication. However, there are common scenarios to be dealt with
in both worlds. For example, an e-mail address passed along by an
OpenID provider is not guaranteed to be verified. So, before hooking
an OpenID account up to a local account the e-mail address must be
verified. So, e-mail verification needs to be present in both worlds.

Integrating both worlds is quite a tedious process. It is definitely
not a matter of simply adding one social authentication app, and one
local account registration app to your ``INSTALLED_APPS`` list.

This is the reason this project got started -- to offer a fully
integrated authentication app that allows for both local and social
authentication, with flows that just work.

Commercial Support
==================

This project is sponsored by If you require assistance on
your project(s), please contact us: info@intenct.nl.
