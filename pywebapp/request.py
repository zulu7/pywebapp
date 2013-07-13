from pywebapp.response import WebResponse
from pywebapp import http_helper

class WebRequest(object):
  def __init__(self, env=None, start_fn=None, path='/', parent=None):
    if not env:
      env = { 'REQUEST_METHOD': 'GET', 'PATH_INFO': path }
    self._env = env
    self.parent = parent
    self.response = WebResponse(start_fn, request=self)
    self.method = self._env.get('REQUEST_METHOD')
    self.path = self._env.get('PATH_INFO')
    self.env = {}
    for k in self._env:
      v = self._env[k]
      if not isinstance(v, (int, float, http_helper.str, tuple, dict, list)):
        continue
      self.env[k] = v

    self.logger = self.parent.logger

  def parse_qs(self):
    return http_helper.urlparse.parse_qs(self.env.get('QUERY_STRING', ''))

  def __repr__(self):
    return "WebRequest: %s" % str(self.env)
  def __str__(self):
    return repr(self)
