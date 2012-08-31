from django.contrib.auth.models import User

class DirectSSOAuthBackend:
    def authenticate(self, direct_sso_username=None):
        if not direct_sso_username:
            return None
        try:
            user = User.objects.get(username=direct_sso_username)
            # we only want to authenticate SSO users, 
            # not local, valid users (i.e. admins)
            if user.has_usable_password():
                return None
            
            return user
        except:
            return None
        
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    
    