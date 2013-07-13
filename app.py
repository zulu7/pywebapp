#!/usr/bin/env python

#from pywebapp.handlers.flup_handler import FlupHandler
from pywebapp.handlers.python_fastcgi_handler import PythonFastCGIHandler
from pywebapp.root_webapp import RootWebApp
import logging

handler_cls = PythonFastCGIHandler

if __name__ == '__main__':
  logger = logging.getLogger('app')
  log_handler = logging.FileHandler('./log')
  formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
  log_handler.setFormatter(formatter)
  logger.addHandler(log_handler)
  logger.setLevel(logging.DEBUG)

  handler = handler_cls(logger=logger)
  handler.start('test_app.TestApp')


