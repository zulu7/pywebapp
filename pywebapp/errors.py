class PyWebAppError(Exception):
  pass

class PyWebAppHandlerNotSupportedError(PyWebAppError):
  def __init__(self, type, inner_exception):
    self.type = type
    self.inner_exception = inner_exception

class PyWebAppResponseHeadersAlreadySentError(PyWebAppError):
  pass

class PyWebAppStartupError(PyWebAppError):
  def __init__(self, inner_exception):
    self.inner_exception = inner_exception

class PyWebAppClassLoadError(PyWebAppError):
  pass

