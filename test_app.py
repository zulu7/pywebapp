import json

from pywebapp.route_webapp import RouteWebApp, route
from pywebapp.root_webapp import RootWebApp
from pywebapp import http_helper

class TestApp(RouteWebApp):
  def __init__(self, *args, **kwargs):
    RouteWebApp.__init__(self, *args, **kwargs)
    #self.add_route('', RootWebApp.info)

  @route('')
  def not_found(self, request):
    request.response.send(status_code=http_helper.status['NOT_FOUND'], content_type='application/json')
    yield json.dumps({
      'status_code': http_helper.status['NOT_FOUND']
      })

  @route(r'^/test/(?P<id>[0-9]+)$')
  @route(r'^/foo/(?P<id>[a-z]+)$')
  def test(self, request, id):
    request.response.send(content_type='application/json')
    yield json.dumps({
      'id': id
      })

