from skyway import cfg, debug
import pymysql

class DBConnector:
    
    _h = None
    
    def __init__(self):
        if DBConnector._h is None:
            c = cfg['db']
            DBConnector._h = pymysql.connect(host=c['host'], user=c['username'], password=c['password'], database=c['database'], port=c['port'])
        
        self.c = DBConnector._h.cursor()
        
    def ex(self, sql):
        if debug:
            print(sql)
        
        try:
            self.c.execute(sql)
        except Exception as e:
            raise Exception("MySQL Error: " + sql + "\nException Details: " + str(e.args))
        
        DBConnector._h.commit()
        
    def update_one(self, tbl, key, ident, values):
        sets = ','.join([("%s='%s'" % (k, str(v))) for k,v in values.items()])
        self.ex("update %s set %s where %s='%s' limit 1" % (tbl, sets, key, str(ident)))
    
    def remove_one(self, tbl, key, ident):
        self.ex("delete from %s where %s='%s' limit 1" % (tbl, key, str(ident)))
        
    
    def insert_one(self, tbl, **values):
        self.ex("insert into %s (%s) values (%s)" % (tbl, ','.join(values.keys()), ','.join([("'%s'" % (str(v))) for v in values.values()])))
        
    def select(self, tbl, fields, **kwargs):
        sql = "select %s from %s" % (fields, tbl)
        
        if 'where' in kwargs:
            sql += ' where ' + kwargs['where']
        
        if 'group' in kwargs:
            sql += ' group by ' + kwargs['group']
        
        if 'order' in kwargs:
            sql += ' order by ' + kwargs['order']
        
        if 'limit' in kwargs:
            sql += ' limit ' + kwargs['limit']
        
        self.ex(sql)
        return self.c.fetchall()
