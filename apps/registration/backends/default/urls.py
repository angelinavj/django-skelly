"""
URLconf for registration and activation, using django-registration's
default backend.

If the default behavior of these views is acceptable to you, simply
use a line like this in your root URLconf to set up the default URLs
for registration::

    (r'^accounts/', include('registration.backends.default.urls')),

This will also automatically set up the views in
``django.contrib.auth`` at sensible default locations.

If you'd like to customize the behavior (e.g., by passing extra
arguments to the various views) or split up the URLs, feel free to set
up your own URL patterns for these views instead.

"""
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from registration.views import activate
from registration.views import register

_backend = {'backend': 'registration.backends.default.DefaultBackend'}
template = lambda temp: {'template': 'registration/%s.html' % temp}

urlpatterns = patterns('',
  url(r'^activate/complete/$', direct_to_template, template("activation_complete"),
     name='registration_activation_complete'),
  # Activation keys get matched by \w+ instead of the more specific
  # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
  # that way it can return a sensible "invalid key" message instead of a
  # confusing 404.
  url(r'^activate/(?P<activation_key>\w+)/$', activate, _backend,
     name='registration_activate'),
  url(r'^register/$', register, _backend, name='registration_register'),
  url(r'^register/complete/$', direct_to_template, template("registration_complete"),
     name='registration_complete'),
  url(r'^register/closed/$', direct_to_template, template("registration_closed"),
     name='registration_disallowed'),
  (r'', include('registration.auth_urls')),
)
