from functools import reduce
from pyspark.sql import functions as Fun
from pyspark.sql import DataFrame
def multiple_equal(df,column,val):
    if type(val)==list and len(val)<=10:
        if len(val)==2:
            df=df.filter((df[column]==val[0])|(df[column]==val[1]))
        elif len(val)==3:
            df=df.filter((df[column]==val[0])|(df[column]==val[1])|(df[column]==val[2]))
        elif len(val)==4:
            df=df.filter((df[column]==val[0])|(df[column]==val[1])|(df[column]==val[2])|(df[column]==val[3]))
        elif len(val)==5:
            df=df.filter((df[column]==val[0])|(df[column]==val[1])|(df[column]==val[2])|(df[column]==val[3])|
            (df[column]==val[4]))
        elif len(val)==6:
            df=df.filter((df[column]==val[0])|(df[column]==val[1])|(df[column]==val[2])|(df[column]==val[3])|
            (df[column]==val[4])|(df[column]==val[5]))
        elif len(val)==7:
            df=df.filter((df[column]==val[0])|(df[column]==val[1])|(df[column]==val[2])|(df[column]==val[3])|
            (df[column]==val[4])|(df[column]==val[5])|(df[column]==val[6]))
        elif len(val)==8:
            df=df.filter((df[column]==val[0])|(df[column]==val[1])|(df[column]==val[2])|(df[column]==val[3])|
            (df[column]==val[4])|(df[column]==val[5])|(df[column]==val[6])|(df[column]==val[7]))
        elif len(val)==9:
            df=df.filter((df[column]==val[0])|(df[column]==val[1])|(df[column]==val[2])|(df[column]==val[3])|
            (df[column]==val[4])|(df[column]==val[5])|(df[column]==val[6])|
            (df[column]==val[7])|(df[column]==val[8]))
        elif len(val)==10:
            df=df.filter((df[column]==val[0])|(df[column]==val[1])|(df[column]==val[2])|(df[column]==val[3])|
            (df[column]==val[4])|(df[column]==val[5])|(df[column]==val[6])|
            (df[column]==val[7])|(df[column]==val[8])|(df[column]==val[9]))
    return df



####equal #####

def equal(df,column,val):
    df=df.filter(df[column]==val)
    return df

##multiple not equal
def multiple_not_equal(df,column,val):
    if type(val)==list and len(val)<=10:
        if len(val)==2:
            df=df.filter((df[column]!=val[0])|(df[column]!=val[1]))
        elif len(val)==3:
            df=df.filter((df[column]!=val[0])|(df[column]!=val[1])|(df[column]!=val[2]))
        elif len(val)==4:
            df=df.filter((df[column]!=val[0])|(df[column]!=val[1])|(df[column]!=val[2])|(df[column]!=val[3]))
        elif len(val)==5:
            df=df.filter((df[column]!=val[0])|(df[column]!=val[1])|(df[column]!=val[2])|(df[column]!=val[3])|
            (df[column]!=val[4]))
        elif len(val)==6:
            df=df.filter((df[column]!=val[0])|(df[column]!=val[1])|(df[column]!=val[2])|(df[column]!=val[3])|
            (df[column]!=val[4])|(df[column]!=val[5]))
        elif len(val)==7:
            df=df.filter((df[column]!=val[0])|(df[column]!=val[1])|(df[column]!=val[2])|(df[column]!=val[3])|
            (df[column]!=val[4])|(df[column]!=val[5])|(df[column]!=val[6]))
        elif len(val)==8:
            df=df.filter((df[column]!=val[0])|(df[column]!=val[1])|(df[column]!=val[2])|(df[column]!=val[3])|
            (df[column]!=val[4])|(df[column]!=val[5])|(df[column]!=val[6])|(df[column]!=val[7]))
        elif len(val)==9:
            df=df.filter((df[column]!=val[0])|(df[column]!=val[1])|(df[column]!=val[2])|(df[column]!=val[3])|
            (df[column]!=val[4])|(df[column]!=val[5])|(df[column]!=val[6])|
            (df[column]!=val[7])|(df[column]!=val[8]))
        elif len(val)==10:
            df=df.filter((df[column]!=val[0])|(df[column]!=val[1])|(df[column]!=val[2])|(df[column]!=val[3])|
            (df[column]!=val[4])|(df[column]!=val[5])|(df[column]!=val[6])|
            (df[column]!=val[7])|(df[column]!=val[8])|(df[column]!=val[9]))
    return df


#### not equal
def not_equal(df,column,val):
    df=df.filter(df[column]!=val)
    return df

###is  null
def is_null(df,column,val):
    df=df.filter(df[column].isNull())
    return df

###not null
def not_null(df,column,val):
    df=df.filter(df[column].isNotNull())
    return df


#union###
def unionAll(*dfs):
    return reduce(DataFrame.unionAll, dfs)


def union(df1,df2):
    df_final=df1.unionByName(df2,allowMissingColumns=True)
    return df_final


def contains(df,col,lkp_value,replace_value):
    """df
              >Data frame
        col
            >column name
        lkp_value >
                    >Lookup value (contains value ) it can be list or a single value
        replace_value
                    > Value wich one will be replace the lookup value """
    if type(lkp_value)==list and type(replace_value)==list:
        for i in range(len(lkp_value)):
            df_final=df.withColumn(col,Fun.when(df[col].contains(lkp_value[i]),regexp_replace('answer_text', lkp_value[i], replace_value[i])).otherwise(df.col))
    else:
        df_final=df.withColumn(col,Fun.when(df[col].contains(lkp_value),regexp_replace('answer_text', lkp_value, replace_value)).otherwise(df.col))
    return df_final


def read_db(spark,User_id,password,table,url):
     stg_raw_data = spark.read \
              .format("jdbc") \
              .option("url", url) \
              .option("dbtable", table) \
              .option("user", User_id) \
              .option("password", password) \
              .option("driver", "org.postgresql.Driver") \
              .load()
    return stg_raw_data



def dynamic_drop(db_table,df):
    '''db_table  Database table
    df dataframe '''
    db_col,df_col=[],[]
    for i in db_table.columns:
        db_col.append(i)
    for i in df.columns:
        df_col.append(i)
    for i in df_col:
        if i not in db_col:
            df=df.drop(col(i))
    return df





