import sys
import os
import traceback

from pywebapp.web_handler import WebHandler, ErrorWebApp
from pywebapp.errors import PyWebAppHandlerNotSupportedError

class PythonFastCGIHandler(WebHandler):
  def __init__(self, **kwargs):
    WebHandler.__init__(self, **kwargs)
    self.server_implementation = None

  def get_instance(self, start_class, *args, **kwargs):
    try:
      from fastcgi import ThreadedWSGIServer
    except ImportError as e:
      raise PyWebAppHandlerNotSupportedError(PythonFastCGIHandler, e)
    self.server_implementation = ThreadedWSGIServer
    instance = WebHandler.get_instance(self, start_class, *args, **kwargs)
    return instance

  def start(self, start_class, *args, **kwargs):
    instance = WebHandler.start(self, start_class, *args, **kwargs)
    self.logger.info('Started a new %s process: %s' % (sys.argv[0], os.getpid()))
    s = self.server_implementation(instance.get_fcgi_handler(), workers=self.num_threads)
    s.serve_forever()

