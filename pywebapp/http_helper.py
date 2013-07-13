python3 = True

try:
  import http.client
  import urllib.parse as urlparse
except ImportError:
  import httplib
  import urlparse
  python3 = False

def get_status_codes():
  g = globals()
  client = http.client if python3 else httplib
  g['status'] = {}
  for attr in dir(client):
    if attr in ('HTTP_PORT', 'HTTPS_PORT', '_MAXLINE'):
      continue
    value = getattr(client, attr)
    if isinstance(value, int):
      g['status'][attr] = value

get_status_codes()

globals()['str'] = (str if python3 else basestring)
globals()['urlparse'] = urlparse

