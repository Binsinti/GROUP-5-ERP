LOGIN_REDIRECT_URL = '/email/compose/' # Redirects users to the home page after login
LOGOUT_REDIRECT_URL = '/login/' # Redirects users to the home page after logout
LOGIN_URL = '/login/' # This is the default, but it's good practice to be explicit

# Mail Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'wlite0990@gmail.com'
EMAIL_HOST_PASSWORD = 'fvlwllnqfemtadap' #'zunoruiagwgfzaps'

# New IMAP Settings for Inbox
IMAP_HOST = 'imap.gmail.com'
IMAP_PORT = 993
# IMAP_USE_SSL = True
# IMAP_HOST_USER = 'wlite0990@gmail.com'
IMAP_USER = 'wlite0990@gmail.com'
# IMAP_HOST_PASSWORD = 'fvlwllnqfemtadap' #'zunoruiagwgfzaps'
IMAP_PASSWORD = 'fvlwllnqfemtadap'