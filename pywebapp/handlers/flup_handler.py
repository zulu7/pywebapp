import sys
import os
import traceback

from pywebapp.web_handler import WebHandler, ErrorWebApp
from pywebapp.errors import PyWebAppHandlerNotSupportedError
from pywebapp import http_helper

class FlupHandler(WebHandler):
  def __init__(self, **kwargs):
    WebHandler.__init__(self, **kwargs)
    self.server_implementation = None

  def start_response(self, start_response_fn, status_code, headers):
    status_string = '%s %s' % (status_code, 'OK' if status_code == http_helper.status['OK'] else 'Error')
    start_response_fn(status_string, headers)

  def get_instance(self, start_class, *args, **kwargs):
    try:
      from flup.server.fcgi import WSGIServer
    except ImportError as e:
      raise PyWebAppHandlerNotSupportedError(FlupHandler, e)
    self.server_implementation = WSGIServer
    instance = WebHandler.get_instance(self, start_class, *args, **kwargs)
    return instance

  def start(self, start_class, *args, **kwargs):
    instance = WebHandler.start(self, start_class, *args, **kwargs)
    self.logger.info('Started a new %s process: %s' % (sys.argv[0], os.getpid()))
    s = self.server_implementation(instance.get_fcgi_handler())
    s.run()

