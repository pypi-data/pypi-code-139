import json
import os.path

import numpy as np
import pandas as pd
# https://blog.csdn.net/Strive_For_Future/article/details/126710810

class pandas:
    def __init__(self, args):
        self.path = args["path"]    # 建议.csv json，读写速度快

        self.file_extension = self.path.split(".")[-1]  # 取文件扩展名

        self.cols = args["cols"]
        # 设置索引，选择值没有重复的一列
        try:
            self.index = args["index"]
        except:
            self.index = False
        if self.file_extension == "csv":
            if not os.path.exists(self.path):
                pass
        elif self.file_extension == "xlsx":
            self.sheet_name = args["sheet_name"]
            if not os.path.exists(self.path):
                self.df = pd.DataFrame(columns=self.cols)
                self.df.to_excel(self.path,sheet_name=self.sheet_name,index=self.index)  #index默认是True，导致第一列是空的,设置为False后可以去掉第一列。

            self.df = pd.DataFrame(pd.read_excel(self.path))
        elif self.file_extension == "json":
            try:
                self.json_orient = args["json_table"]
            except:
                self.json_orient = "split"     # orient 参数看下方注解，这里用split,节省空间
            if not os.path.exists(self.path):
                data = {}
                for col in self.cols:
                    data[col] = []
                self.df = pd.DataFrame(data)
                self.save()
                r'''
                {"col1":{"0":"1","1":"3"},"col2":{"0":"2","1":"4"}}
                json_split =  {"columns":["col1","col2"],"index":[0,1],"data":[["1","2"],["3","4"]]} 
                json_records =  [{"col1":"1","col2":"2"},{"col1":"3","col2":"4"}] 
                json_index =  {"0":{"col1":"1","col2":"2"},"1":{"col1":"3","col2":"4"}} 
                json_columns =  {"col1":{"0":"1","1":"3"},"col2":{"0":"2","1":"4"}} 
                json_values =  [["1","2"],["3","4"]] 
                json_table =  {"schema":{"fields":[{"name":"index","type":"integer"},{"name":"col1","type":"string"},{"name":"col2","type":"string"}],"primaryKey":["index"],"pandas_version":"1.4.0"},"data":[{"index":0,"col1":"1","col2":"2"},{"index":1,"col1":"3","col2":"4"}]} 
                '''
            self.df = pd.read_json(path_or_buf=self.path,orient=self.json_orient,encoding='utf-8',convert_dates=False,keep_default_dates = False)



    # 设置索引，
    def set_index(self,cols=None):
        if not cols:
            self.df.reset_index(drop=True,inplace=True)
        else:
            self.df.set_index(cols,drop=False,inplace=True)

    def add(self,values,index=None):
        if self.index is not None and index is None:
                exit("缺少index值")
        self.index = index if self.index is None else self.index

        cols = self.df.columns.values
        if type(values) == dict:
            cols = list(values.keys())
            values = [list(values.values())]
        index = [index] if type(index) == str else index
        values = [values] if type(values) == str else values
        values = [values] if type(values[0]) == str else values
        df2 = pd.DataFrame(data = values,columns=cols,index=index)
        #df2.loc[len(df2.index)] = data
        ignore_index = True if index is None else False
        print(ignore_index)
        self.df = pd.concat([self.df,df2],ignore_index=ignore_index)

    def save(self):
        fe = self.file_extension
        if fe == "xlsx":
            self.df.to_excel(self.path, sheet_name=self.sheet_name, index=False)  # index默认是True，导致第一列是空的,设置为False后可以去掉第一列。
        elif fe == "csv":
            pass
        elif fe == "json":
            self.df.to_json(path_or_buf=self.path,orient=self.json_orient,date_format="iso")
            '''
            date_format:【None, ‘epoch’, ‘iso’】，日期转换类型。可将日期转为毫秒形式，iso格式为ISO8601时间格式。对于orient='table'，默认值为“iso”。对于所有其他方向，默认值为“epoch”
            double_precision:【int, default 10】,对浮点值进行编码时使用的小数位数。默认为10位。
            force_unit:【boolean, default True】,默认开启，编码位ASCII码。
            date_unit:【string, default ‘ms’ (milliseconds)】,编码到的时间单位，控制时间戳和ISO8601精度。“s”、“ms”、“us”、“ns”中的一个分别表示秒、毫秒、微秒和纳秒.默认为毫秒。
            default_handler :【callable, default None】,如果对象无法转换为适合JSON的格式，则调用处理程序。应接收单个参数，该参数是要转换并返回可序列化对象的对象。
            lines：【boolean, default False】，如果“orient”是“records”，则写出以行分隔的json格式。如果“orient”不正确，则会抛出ValueError，因为其他对象与列表不同。
            compression:【None, ‘gzip’, ‘bz2’, ‘zip’, ‘xz’】，表示要在输出文件中使用的压缩的字符串，仅当第一个参数是文件名时使用。
            index:【boolean, default True】，是否在JSON字符串中包含索引值。仅当orient为“split”或“table”时，才支持不包含索引（index=False）。
            
            '''

    def drop(self,where):
        '''

        :param where: dict {列名：内容}，int index,行号
        :return:
        '''
        if type(where) == dict:
            indexs = self.get_index(where)  # 取索引值
        else:   # where 是索引
            indexs = where if type(where) == list else [where]

        self.df.drop(index=indexs, inplace=True)
        self.df.reset_index(drop=True,inplace=True)     # 重新设置索引

    def get_index(self,where):
        '''

        :param where: dict {列名：内容}，int index,行号
        :return:[n,...]
        '''
        col = list(where.keys())[0]
        key = list(where.values())[0]
        indexs = self.df[self.df[col] == key].index.tolist()
        return indexs
    # 删除重复值
    def drop_duplicates(self,cols:list,keep="last",index=False,sort=True):
        '''

        cols：list 表示要进去重的列名，默认为 None。
        index: True,索引去重
        last：有三个可选参数，分别是 first、last、False，默认为 first，表示只保留第一次出现的重复项，删除其余重复项，last 表示只保留最后一次出现的重复项，False 则表示删除所有重复项。
        inplace：布尔值参数，默认为 False 表示删除重复项后返回一个副本，若为 Ture 则表示直接在原数据上删除重复项。

        :return:
        '''

        if index:
            self.drop_index_duplicates(keep)
        else:
            self.df.drop_duplicates(subset=cols,keep=keep,inplace=True)
        if sort:
            self.sort()

    # 索引去重
    def drop_index_duplicates(self,keep="last"):
        self.df = self.df[~self.df.index.duplicated(keep=keep)]



    def rename(self,cols:dict):
        '''

        :param cols: {原名：新名}
        :return:
        '''
        self.df = self.df.rename(columns=cols)

    # 数据替换
    def replace(self,col,old,new):
        self.df[col].replace(old,new,inplace=True)



    def sort(self,cols=False):
        '''
        如果不指定cols,则按索引重新排序
        :param cols: 可以是列表，也可以是字符串
        :return:
        '''
        if not cols:
            self.df.sort_index(inplace=True)
        else:
            self.df.sort_values(by=cols,inplace=True)

    def get(self,where=False,cols=False):
        '''
        1、使用“与”进行筛选
        df_inner.loc[(df_inner['age'] > 25) & (df_inner['city'] == 'beijing'), ['id','city','age','category','gender']]
        2、使用“或”进行筛选
        df_inner.loc[(df_inner['age'] > 25) | (df_inner['city'] == 'beijing'), ['id','city','age','category','gender']].sort(['age'])
        3、使用“非”条件进行筛选
        df_inner.loc[(df_inner['city'] != 'beijing'), ['id','city','age','category','gender']].sort(['id'])
        4、对筛选后的数据按city列进行计数
        df_inner.loc[(df_inner['city'] != 'beijing'), ['id','city','age','category','gender']].sort(['id']).city.count()
        5、使用query函数进行筛选
        df_inner.query('city == ["beijing", "shanghai"]')
        6、对筛选后的结果按prince进行求和
        df_inner.query('city == ["beijing", "shanghai"]').price.sum()







        :param where: 可以是dict条件，也可以是索引，也可以是False表示全部
        :return: [[所有字段]，[所有值]]
        '''
        if type(where) == int:
            res = self.df.loc[where]
            values = list(res)
            keys = list(self.df.columns.values)
        else:
            if where is False:
                res = self.df
            else:
                res = self.df.loc[where]
            keys = list(res.columns.values)
            values = []

            #print(res.values.itemsize)
            for v in res.values:
                values.append(list(v))

        res = [keys,values]
        return res

    #

    # 1、维度查看：
    # self.df.shape     # 返回（r,c） 几行几列,列头是0行

    # 2、数据表基本信息（维度、列名称、数据格式、所占空间等）：
    # self.df.info()

    # 3、查看所有行的行索引名
    # self.df.index           # 得到一个对象
    # self.df.index.values    # 得到一个列表

    # 4、查看所有列的列索引名
    # 查看所有列的列名
    # self.df.columns  # 得到的是一个series对象
    # self.df.columns.values  # 得到的是一个列表

    # 5、定位表格中的指定元素
    # 要在pandas.DataFrame中的任何位置检索或更改数据，可以使用at，iat，loc，iloc。
    # 更多细节详见 https://blog.csdn.net/qq_18351157/article/details/104838924
    # print(self.df.at['行标签名', '列标签名'])
    # print(self.df.iat['行索引号', '列索引号'])

    # print(self.df.loc['行标签名', '列标签名'])
    # print(self.df.iloc[行索引数字, 列索引数字])

    # print(self.df.loc['行标签名1':'行标签名2', '列标签名1': '列标签名2'])
    # print(self.df.iloc[行索引数字1:行索引数字2, 列索引数字1:列索引数字2])

    # 6、每一列数据的格式：
    # self.df.dtypes

    # 7、某一列格式：
    # self.df['B'].dtype

    # 8、查看某一列的所有值
    # self.df["姓名"].values  # 获取某一列的所有数值
    # 说明:需要先用对应列的列名称“姓名”获取对应列对象，然后用.values将对象转变为列表




if __name__ == '__main__':
    import random
    args = {}
    args["path"] = "c:/item/data.json"
    args["cols"] = np.arange(6)
    #args["sheet_name"] = "a"
    #args["index"] = "aa"

    pds = pandas(args)

    date1 = pd.date_range("20180813", periods=6)
    data = []
    for l in range(6):
        iData = []
        for i in range(6):
            item = "".join(random.sample('zyxwvutsrqponmlkjihgfedcba',3))
            iData.append(item)
        data.append(iData)
    #pds.add(data,date1)

    date1 = pd.date_range("20190813", periods=3)
    date = []
    for i in range(len(date1)):
        item = date1.values[i]
        item = str(item)[:10]
        date.append(item)
    for i in range(len(date)):
        dt = random.choice(date)
        data = []
        for i in range(6):
            item = "".join(random.sample('zyxwvutsrqponmlkjihgfedcba',3))
            data.append(item)

        pds.add(data, dt)

    #df = pds.sort()
    #pds.set_index([1,2])
    #pds.replace( 1, "sun", "abcddddd")
    #pds.set_index()
    print(pds.df)
    pds.save()
    exit()

