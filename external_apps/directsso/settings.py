import os

# The login URL
DIRECT_SSO_LOGIN_URL = 'http://typo3.org/login/translation'

# Technical contact email, this should be an admin on the local server
DIRECT_SSO_CONTACT_EMAIL = 'dfeyer@reelpeek.net'

# Path to the file or ASCII content of the key.
DIRECT_SSO_PUBLIC_KEY = """
-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAu+x5xKoCGxc/I4jB5soN
IqklkDH/jvLER0enJd1jIeOJ8jOjo7kMkMnt/5qfpIb4tnCYVLXR7OrhQ16TQfty
wuaeeVothdthc3SWFCB9j3k7983RJOgHsQzFNLpGzokMbI0PIs4xZVEimegS3ItR
1xWINdRkK/R6Y4oCx/SgR1hO5uqnYJNOytHRAe4JxKwNN2LSuvkNob15dHqTKU9M
CwztPTtoHK2KwkgGHq6lLFpGLeKBa7r98Mm1TXV+VsD2M1sT1vgJ6ocXEdf153xY
1zQmUecexTlS/oQnHGdtSWvNdPQBnfD6qADiC9YZwA15WHG2fEqsLuxiVVfIURNo
IXqKpVuS96a3vkAqi/AECd+FzlIgeTOFLf+SZmRhsxECXesdoc2ZL8exBKK05Wqt
YcnIuXhTsiqwDmsr9hhpaXHDFI/7aZFaV0C+Is3z67m/vfK8IRAVv9J5tAyIwqKz
JV75+Wj/Uww0AqulHXm8Ayf+yS7MHwePDA/Sh2cE7Yv6unta4o3D/vhZg0QQlDKJ
IZtldY+0HbgHJqEKxfipcA7gO1GpRlj6HVnwjHwJfcFfRwKdnDy+tWziUJQL50TV
pJvAzTUnrt7k1xomc87kW7CFk58I6f1GH5PhDJnxhPM0i0nSRaLfsDsHv7k310co
5Vpe3Ym6JZF7Nm/cLr/OAfsCAwEAAQ==
-----END PUBLIC KEY-----
"""

# Configured on the Typo3 server
DIRECT_SSO_TPA_ID = "Pootle Server"

# Must be True on production: prevents the same URL to be reused to re-authenticate a user
DIRECT_SSO_ENFORCE_NO_REPEAT_ATTACK = True

# Redirect to this URL after a successfull login
DIRECT_SSO_SUCCESS_REDIRECT_URL = '/accounts/personal/edit/'
