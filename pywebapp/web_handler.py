import cgi
import logging
import sys
import traceback

from pywebapp import http_helper
from pywebapp.errors import PyWebAppStartupError, PyWebAppClassLoadError
from pywebapp.root_webapp import RootWebApp

DEFAULT_LOGGER_NAME = 'pywebapp'

class WebHandler(object):
  def __init__(self, num_threads=1, logger=None):
    self.num_threads = num_threads
    if logger == None:
      logger = logging.getLogger(DEFAULT_LOGGER_NAME)
    self.logger = logger

  def start_response(self, start_response_fn, status_code, headers):
    return start_response_fn(status_code, headers)

  def load_cls(self, start_class, args, kwargs):
    error_str = 'Failed to load %s. Check names and permissions.'
    pieces = start_class.split('.')
    cls = __import__(pieces[0])
    if not cls:
      raise PyWebAppClassLoadError(error_str % pieces[0])
    for i, piece in enumerate(pieces):
      if i == 0:
        continue
      if not hasattr(cls, piece):
        raise PyWebAppClassLoadError(error_str % ('%s from module %s' % (pieces[i], '.'.join(pieces[0:i]))))
      cls = getattr(cls, piece)
    return cls

  def get_instance(self, start_class, *args, **kwargs):
    cls = self.load_cls(start_class, args, kwargs)
    kwargs['handler'] = self
    instance = cls(*args, **kwargs)
    return instance

  def start(self, start_class, *args, **kwargs):
    try:
      instance = self.get_instance(start_class, *args, **kwargs)
    except Exception as e:
      error_str = traceback.format_exc()
      instance = ErrorWebApp(exception=e, error_str=error_str, handler=self)
    return instance

class ErrorWebApp(RootWebApp):
  def __init__(self, error_str=None, exception=None, logger=None, handler=None):
    RootWebApp.__init__(self, logger=logger, handler=handler)
    self.error_str = error_str
    self.exception = exception
    self.logger.error('err1: %s' % error_str)

  def handle_request(self, request):
    request.response.status_code = http_helper.status['INTERNAL_SERVER_ERROR']
    request.response.send()
    if not self.error_str:
      self.error_str = str(self.exception)
    title = 'Startup Error' if isinstance(self.exception, PyWebAppClassLoadError) else 'Application Error'
    yield '<h2>%s</h2>' % title
    yield '<pre style="color:red;">%s</pre>' % self.error_str

