import json
import logging
import sys
import traceback

from pywebapp.request import WebRequest
from pywebapp import http_helper

DEFAULT_LOGGER_NAME = 'pywebapp'

class RootWebApp(object):
  def __init__(self, handler=None, logger=None):
    self.handler = handler
    if logger == None and handler:
      logger = handler.logger
    if logger == None:
      logger = logging.getLogger(DEFAULT_LOGGER_NAME)
    self.logger = logger

  def get_fcgi_handler(self):
    def handler_function(env=None, start_response=None, path=None):
      start_response_callback = lambda status_code, headers: self.handler.start_response(start_response, status_code, headers)
      if path:
        request = WebRequest(path=path, parent=self)
      else:
        request = WebRequest(env, start_response_callback, parent=self)
      self.logger.info('request: %s' % request.path)
      try:
        for item in self.handle_request(request):
          yield item
      except Exception as e:
        error_str = '<h2>Error Handling Request</h2><pre style="color:red;">%s</pre>' % traceback.format_exc()
        if not request.response.sent:
          request.response.status_code = http_helper.status['INTERNAL_SERVER_ERROR']
          request.response.send()
          yield error_str
        else:
          yield error_str
    return handler_function

  def handle_request(self, request, *args, **kwargs):
    request.response.send()
    yield '<h2>Your Website Works!</h2>'

  def info(self, request, *args, **kwargs):
    request.response.send(content_type='application/json')
    yield json.dumps({
      'qs': request.parse_qs(),
      'path': request.path,
      'method': request.method,
      'env': request.env
      })

