import string

from pywebapp import http_helper
from pywebapp.errors import PyWebAppResponseHeadersAlreadySentError

class WebResponse(object):
  def __init__(self, start_fn, request=None):
    self._start_fn = start_fn
    self.request = request
    self.status_code = http_helper.status['OK']
    self.headers = {'Content-Type': 'text/html'}
    self.sent = False
    self.logger = self.request.parent.logger

  def send(self, status_code=None, headers=None, **kwargs):
    """can also pass headers as kwargs:
    request.response.send(content_type='application/json')
    """

    if self.sent:
      raise PyWebAppResponseHeadersAlreadySentError

    if status_code != None:
      if isinstance(status_code, http_helper.str):
        self.status_code = http_helper.status.get(status_code.upper())
      else:
        self.status_code = status_code

    if headers:
      for k in headers:
        self.headers[k] = headers[k]

    for k in kwargs:
      k_str = k.replace('_', '-')
      k_str = string.capwords(k_str, '-')
      self.headers[k_str] = kwargs[k]

    self.logger.info('%s' % self.headers)

    self._start_fn(self.status_code, [
      (k, self.headers[k]) for k in self.headers
      ])
    self.sent = True

