from M2Crypto import BIO, RSA, EVP
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
import os, datetime, base64, hashlib


def handle_auth(request):
    """
    Main entry point of the Direct SSO agent.
    """
    
    def verify_sig(payload, signature):
        "Verify the signature digest using the configured public key"
        
        # Load the public key
        if os.path.exists(settings.DIRECT_SSO_PUBLIC_KEY):
            ascii_pub_key = open(settings.DIRECT_SSO_PUBLIC_KEY,'r').read()
        else:
            ascii_pub_key = settings.DIRECT_SSO_PUBLIC_KEY
            
        bio = BIO.MemoryBuffer(ascii_pub_key)
        rsa = RSA.load_pub_key_bio(bio)
        pubkey = EVP.PKey()
        pubkey.assign_rsa(rsa)
        pubkey.reset_context(md='sha1')
        pubkey.verify_init()
        pubkey.verify_update(payload)
        return pubkey.verify_final(signature) == 1
        
    # Calculate the hash of the querystring, check if it was 
    # used before
    sso_link_hash = hashlib.new('sha1', request.META.get('QUERY_STRING')).hexdigest()
    cache_key = 'sso_hash_%s' %sso_link_hash
    if cache.get(cache_key) is None:
        cache.set(cache_key,True, 3600)
    else:
        if settings.DIRECT_SSO_ENFORCE_NO_REPEAT_ATTACK:
            raise Exception(_('This single-signon query string was used before. Please try the login process again. If the problem persists, please contact %s.') %settings.DIRECT_SSO_CONTACT_EMAIL)
    
    
    # Sanitize all passed data
    version, user, tpa_id, expires, action, flags, userdata, signature = \
        request.GET.get('version',''), \
        request.GET.get('user',''), \
        request.GET.get('tpa_id',''), \
        request.GET.get('expires',''), \
        request.GET.get('action',''), \
        request.GET.get('flags',''), \
        request.GET.get('userdata',''), \
        request.GET.get('signature','').decode('hex')
    
    # TPA ID must match the configured one, just in case.
    if tpa_id != settings.DIRECT_SSO_TPA_ID:
        raise Exception(_('An invalid Application ID key was used. Please report this problem to %s.') %settings.DIRECT_SSO_CONTACT_EMAIL)

    # Verify the signature digest
    payload = 'version=%s&user=%s&tpa_id=%s&expires=%s&action=%s&flags=%s&userdata=%s' %(
        version, user, tpa_id, expires, action, flags, userdata
    )
    payload = str(payload)    
    if not verify_sig(payload, signature):
        raise Exception(_('Could not validate the SSO signature. Please report this problem to %s.') %settings.DIRECT_SSO_CONTACT_EMAIL)
    
    # Make sure the URL is still valid
    if datetime.datetime.fromtimestamp(float(expires)) < datetime.datetime.now():
        raise Exception(_('The given single-signon URL has expired. Please try the login process again, if the problem persists, please contact %s.') %settings.DIRECT_SSO_CONTACT_EMAIL)
    
    # All good, extract the userdata, stash it away in a dict
    try:
        udata = dict()
        for pair in base64.b64decode(userdata).split('|'):
            try:
                k,v = pair.split('=')
                udata[k] = v
            except:
                pass
            
        userdata = udata
    except:
        raise Exception(_('The given userdata is invalid. Please try the login process again, if the problem persists, please contact %s.') %settings.DIRECT_SSO_CONTACT_EMAIL)

    # Check whether the user exists, if not, create him
    try:
        user = User.objects.get(username=userdata.get('username'))
    except User.DoesNotExist:
        user = User.objects.create_user(
            userdata.get('username'),
            userdata.get('email', None)
        )
        user.is_active = True
        user.set_unusable_password()
    
    # Update the user data    
    if ' ' in userdata.get('name'):
        user.first_name, user.last_name = userdata.get('name').rsplit(' ',1)
    else:
        user.first_name = userdata.get('name')
    user.email = userdata.get('email', '')
    user.save()
    
    
    # Log 'em in
    user = authenticate(direct_sso_username=userdata.get('username'))
    if user is not None and user.is_active:
        login(request, user)
    else:
        raise Exception(_('Could not authenticate you, sorry. Please contact %s') %settings.DIRECT_SSO_CONTACT_EMAIL)
        
    
    # Success, redirect to the configured URL
    return HttpResponseRedirect(settings.DIRECT_SSO_SUCCESS_REDIRECT_URL)
    
