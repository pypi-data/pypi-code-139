import kthutils.ug
import os

ug = kthutils.ug.UGsession(os.environ["KTH_LOGIN"], os.environ["KTH_PASSWD"])

def test_list_editable_groups():
  groups = ug.list_editable_groups()
  assert groups
def test_find_user_by_username():
  data = ug.find_user_by_username("dbosk")
  assert data[0]["username"] == "dbosk"
