Install the DirectSSO authentication back-end
---------------------------------------------

0. Install the requirements::

        pip install m2crypto
    
    or:
        
        easy_install m2crypto
    

1. Place the ``directsso`` folder somewhere in the Python path (e.g. ``external_apps``)
2. Add an URLconf entry in ``pootle/urls.py``::
 
        url('^auth/', include('directsso.urls')),
   
   Note: the ``/auth/`` prefix can be anything you want, but it has to match the path path configured on the SSO server.
   
   Note: the URLconf line should be high in the list, e.g. right after the Django admin lines.

3. Add the ``directsso.auth.DirectSSOAuthBackend`` back-end to ``AUTHENTICATION_BACKENDS`` in ``localsettings.py``, e.g.::

        AUTHENTICATION_BACKENDS = (
            'django.contrib.auth.backends.ModelBackend',
            'directsso.auth.DirectSSOAuthBackend',    
        )

4. At the end of ``localsettings.py`` import the directsso settings::

        from directsso.settings import *

5. Edit ``directsso/settings.py`` to suit your needs.

6. Restart your server to take the changes into account
