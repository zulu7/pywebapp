import re

from pywebapp.root_webapp import RootWebApp

def route(route=None):
  def decorator(target):
    if not hasattr(target, 'routes'):
      target.routes = []
    target.routes.append(route)
    return target
  return decorator

def isbound(method):
  attr = None
  if hasattr(method, '__self__'):
    attr = method.__self__
  elif hasattr(method, 'im_self'):
    attr = method.im_self
  return attr is not None

DEFAULT_ROUTE_IDENTIFIER = ''

class RouteWebApp(RootWebApp):
  def __init__(self, *args, **kwargs):
    RootWebApp.__init__(self, *args, **kwargs)
    self.discover_routes()

  def add_route(self, regex, fn):
    self.routes[re.compile(regex) if len(regex) > 0 else ''] = fn

  def discover_routes(self):
    self.routes = {}
    for attr_str in dir(self):
      attr = getattr(self, attr_str)
      if not callable(attr) or\
         not hasattr(attr, 'routes'):
        continue
      routes = getattr(attr, 'routes')
      if not isinstance(routes, list):
        continue
      for regex in routes:
        self.add_route(regex, attr)

  def default_route(self, request):
    """called when no routes match the request
    """
    if DEFAULT_ROUTE_IDENTIFIER in self.routes:
      for result in self.route_call(request, DEFAULT_ROUTE_IDENTIFIER):
        yield result
    else:
      for result in RootWebApp.handle_request(self, request):
        yield result

  def route_call(self, request, route, route_dict=None):
    if route_dict == None:
      route_dict = {}
    method = self.routes[route]
    if isbound(method):
      call = method(request, **route_dict)
    else:
      call = method(self, request, **route_dict)
    return call

  def handle_request(self, request):
    match = False
    for route in self.routes:
      if route == DEFAULT_ROUTE_IDENTIFIER:
        continue
      m = re.match(route, request.path)
      if m:
        match = True
        for result in self.route_call(request, route, m.groupdict()):
          yield result
        break
    if not match:
      for result in self.default_route(request):
        yield result

