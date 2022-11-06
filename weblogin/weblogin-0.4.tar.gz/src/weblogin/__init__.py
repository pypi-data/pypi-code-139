import requests

class AuthenticationError(Exception):
  pass

class AutologinSession(requests.Session):
  """
  Maintains an authenticated session to a web system. This class intercepts any 
  requests made in a requests.Session and ensures that we log in when 
  redirected to the login page.

  This is an abstract class.
  """

  def __init__(self):
    super().__init__()
    self.__logging_in = False

  def login(self, response, args=None, kwargs=None):
    """
    Performs a login based on the response from a request.
    args and kwargs are the options from the request triggering the login 
    procedure, this is so that we can redo that request after loggin in.

    Raises an AuthenticationError exception if authentication fails.
    """
    raise NotImplementedError()

  def need_login(self, response):
    """
    Checks a response to determine if logging in is needed,
    returns True if needed
    """
    raise NotImplementedError()

  def request(self, *args, **kwargs):
    """
    Wrapper around requests.Session.request(...) to check if logging in
    is needed.
    """
    response = super().request(*args, **kwargs)
    
    if not self.__logging_in and self.need_login(response):
      self.__logging_in = True
      response = self.login(response, args, kwargs)
      self.__logging_in = False

    return response
