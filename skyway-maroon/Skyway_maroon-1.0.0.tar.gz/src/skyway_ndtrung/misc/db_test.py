from ..db import *

db = DBConnector()
db.ex('show tables;')
print(db.c.fetchall())
