import numpy as np

def single_formu(x,y):
  """
  find the distance between two points
  Arguments:
      a: an integer
      b: an integer
  Returns:
      The distance between two points
  """
  forward = np.sqrt(np.square(y - x))
  backword = np.sqrt(np.square(((360 - (abs(max(x,y)))) + min(x,y))))
  lowest_distance=min(backword,forward)
  return lowest_distance

def list_formu(x,y):
  """
  find the distance between two list of points
  Arguments:
      a: an list
      b: an list
  Returns:
      The distance between two list of points
  """
  forward = (np.square(y - x))
  backword = (np.square(((360 - (abs(max(x,y)))) + min(x,y))))
  lowest_distance=min(backword,forward)
  return lowest_distance

def distance(ed1,ed2):
  """
  calculate the distance between given two integer or list
  Arguments:
      a: an integer or an list
      b: an integer or an list
  Returns:
      The distance between two points or list of points
  """
  if isinstance(ed1, list) and isinstance(ed2, list):
    if (max(ed1) < 361) and (max(ed2) < 361) and (len(ed1) == len(ed2)):
      result = np.sqrt(sum([(list_formu(ed1[i],ed2[i])) for i in range(len(ed1))]))
    else:
      result="entered number exceed the limit 360 degree or given list is of different length"
  else:
    if (ed1 < 361) and (ed2 < 361):
      result = int(single_formu(ed1,ed2))
    else:
      result = "entered number exceed the limit 360 degree"
  return result
