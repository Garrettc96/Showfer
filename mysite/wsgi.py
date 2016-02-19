import os
print('hi')
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
print('hi')
from dj_static import Cling
application = Cling(get_wsgi_application())
print('hi')
