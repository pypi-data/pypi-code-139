import cachetools as ct
import functools as ft
import json
import operator
import re
import requests
import weblogin
import weblogin.kth

class UGsession:
  """
  Maintains a session to the UG Editor APIs.
  """
  BASE_URL = "https://app.kth.se/ug-gruppeditor"

  def __init__(self, username, password):
    """Never used directly, instantiated through childclasses."""
    self.__session = weblogin.AutologinSession([
          weblogin.kth.UGlogin(username, password,
                               self.BASE_URL)
      ])
    self.cache = {}

  @ct.cachedmethod(operator.attrgetter("cache"),
    key=ft.partial(ct.keys.hashkey, "list_editable_groups"))
  def list_editable_groups(self):
    """
    Lists all groups that are editable by the logged in user.
    Returns list of JSON objects.
    """
    response = self.__session.get(
        f"{self.BASE_URL}/api/ug/groups?editableBySelf=true")
    return response.json()
  def find_group_by_name(self, name_regex):
    """
    Searches for a group from `list_editable_groups()` whose name matches the 
    regex `name_regex`.
    Returns a list of matching groups.
    """
    return filter(lambda group: re.search(name_regex, group["name"]),
                  self.list_editable_groups())
  def list_group_members(self, group_kthid):
    """
    Returns a list of the members of a group.
    The list contains JSON objects.
    """
    response = self.__session.get(
      f"{self.BASE_URL}/api/ug/users?$filter=memberOf eq '{group_kthid}'")
    return response.json()
  def set_group_members(self, members, group_kthid):
    """
    Sets the group members of group identified by `group_kthid` to be the list of 
    users (strings of kthid for users) `members`.

    Returns the updated group data, JSON format.
    """
    headers = self.__session.headers
    headers["content-type"] = "application/merge-patch+json"
    data = {
      "kthid": group_kthid,
      "members": members if isinstance(members, list) \
                         else list(members)
    }

    response = self.__session.patch(
      f"{self.BASE_URL}/api/ug/groups/{group_kthid}",
      data=json.dumps(data), headers=headers)

    if response.status_code != requests.codes.ok:
      raise Exception(f"failed to set members: {response.status_code}: "
                      f"{response.text}")

    return response.json()
  def add_group_members(self, new_members, group_kthid):
    """
    Adds list of members in `new_members` (kthids of users) to group with kthid 
    `group_kthid`.

    Returns the updated group data, JSON format.
    """
    current_members = [x["kthid"] for x in self.list_group_members(group_kthid)]
    return self.set_group_members(
              set(current_members + new_members),
              group_kthid)
  def remove_group_members(self, members, group_kthid):
    """
    Removes the users in `members` (list of kthids) from the group identified by 
    kthid `group_kthid`.

    Returns the updated group data, JSON format.
    """
    current_members = [x["kthid"] for x in self.list_group_members(group_kthid)]
    return self.set_group_members(
              set(current_members) - set(members),
              group_kthid)
  def find_user_by_username(self, username):
    """
    Finds a user by username.
    Returns a list of matching user objects.
    """
    response = self.__session.get(f"{self.BASE_URL}/api/ug/users"
      f"?$filter=username eq '{username}' or emailAliases eq '{username}'")
    return response.json()
