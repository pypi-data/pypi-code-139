from lxml import html
import requests
import weblogin

class UGlogin(weblogin.AutologinHandler):
  """
  Login handler (weblogin.AutologinHandler) for UG logins, i.e. through 
  login.ug.kth.se.
  """
  LOGIN_URL = "https://login.ug.kth.se"
  
  def __init__(self, username, password, login_trigger_url=None):
    """
    Creates a login handler that automatically logs into KTH.
    - Requires username and password.
    - Optional `login_trigger_url` is a page that redirects to the login page,
      for instance, the API URLs don't redirect, but the UI URLs do.
    """
    super().__init__()
    self.__username = username
    self.__password = password
    self.__login_trigger_url = login_trigger_url
    self.__logging_in = False

  def need_login(self, response):
    """
    Checks a response to determine if logging in is needed,
    returns True if needed
    """
    if self.__logging_in:
      return False

    return (response.status_code == requests.codes.unauthorized and \
              "kth.se" in response.url) or \
           response.url.find(self.LOGIN_URL) == 0

  def login(self, session, response, args=None, kwargs=None):
    """
    Performs a login based on the response `response` from a request to session 
    `session`.
    `args` and `kwargs` are the options from the request triggering the login 
    procedure, this is so that we can redo that request after logging in.

    Raises an AuthenticationError exception if authentication fails.
    """
    self.__logging_in = True
    if response.status_code == requests.codes.unauthorized:
      new_response = session.get(self.__login_trigger_url)
      login_response = self.login(session, new_response)
      request_response = session.request(*args, **kwargs)

      if request_response.status_code == requests.codes.unauthorized:
        raise AuthenticationError(f"authentication apparently failed: "
                                  f"{login_response.text}")

      return request_response
    else:
      doc_tree = html.fromstring(response.text)
      form = doc_tree.xpath("//form[@id='loginForm']")[0]

      data = {}

      for variable in form.xpath("//input"):
        if variable.value:
          data[variable.name] = variable.value

      data["UserName"] = self.__username if "@ug.kth.se" in self.__username \
                                         else self.__username + "@ug.kth.se"
      data["Password"] = self.__password
      data["Kmsi"] = True

      new_response = session.request(
        form.method, f"{self.LOGIN_URL}/{form.action}",
        data=data)

      if new_response.status_code != requests.codes.ok:
        raise AuthenticationError(
          f"authentication as {self.__username} to {new_response.url} failed: "
          f"{new_response.text}")

      return new_response
    self.__logging_in = False
