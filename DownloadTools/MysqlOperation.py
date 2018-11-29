#coding:utf-8
import pymysql

def insert_into_mysql(db_config, tablename, params={}, mode='single'):
    conn = pymysql.connect(
        host=db_config['host'],
        db=db_config['db'],
        user=db_config['user'],
        passwd=db_config['passwd'],
        charset=db_config['charset']
    )
    sql = "insert into %s " % tablename
    keys = params.keys()
    sql += "(`" + "`,`".join(keys) + "`)"               #字段组合
    values = list(params.values())                        #值组合，由元组转换为数组
    sql += " values (%s)" % ','.join(['%s']*len(values))  #配置相应的占位符
    cur = conn.cursor()
    if mode == 'single':
        cur.execute(sql, values)
        conn.commit()
        cur.close()
        conn.close()
    elif mode == 'multiple':
        insert_items = []
        flag = 0
        index = 0
        while True:
            temp = []
            for key in keys:
                if index == len(params[key]):
                    flag = 1
                    break
                temp.append(params[key][index])
            if flag == 1:
                break
            insert_items.append(temp)
            index += 1

        cnt = 0
        for item in insert_items:
            cur.execute(sql, item)
            cnt += 1
            if cnt % 30 == 0:
                conn.commit()
        conn.commit()
        cur.close()
        conn.close()
    else:
        raise Exception

def delete_from_mysql(db_config, tablename, field='uuid', value=''):
    conn = pymysql.connect(
        host=db_config['host'],
        db=db_config['db'],
        user=db_config['user'],
        passwd=db_config['passwd'],
        charset=db_config['charset']
    )
    sql = "delete from %s " % tablename
    sql += " where %s = '%s' " % (field, value)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def update_mysql(db_config, tablename, params={}):
    conn = pymysql.connect(
        host=db_config['host'],
        db=db_config['db'],
        user=db_config['user'],
        passwd=db_config['passwd'],
        charset=db_config['charset']
    )
    cur = conn.cursor()
    sql = "update %s set " % tablename
    keys = params.keys()
    for al in keys:                                  #字段与占位符拼接
        if al != 'uuid':
            sql += "`" + al + "` = %(" + al + ")s,"
    sql = sql[:-1]                                   #去掉最后一个逗号
    sql += " where uuid = %(uuid)s "                 #只支持按主键进行修改
    cur.execute(sql, params)
    conn.commit()
    cur.close()
    conn.close()

def get_data_from_mysql(db_config, tablename, params={}, where=None, fields=[], order_field=None, order_by = 'desc', start=None, num=None):

    order = ''
    limit = ''

    if order_field is not None:
        order = ' order by ' + order_field + ' ' + order_by

    if start is not None and num is not None:
        limit = ' limit ' + str(start) + ',' + str(num)

    conn = pymysql.connect(
        host=db_config['host'],
        db=db_config['db'],
        user=db_config['user'],
        passwd=db_config['passwd'],
        charset=db_config['charset']
    )
    sql = "select %s from %s " % ('*' if len(fields) == 0 else ','.join(fields), tablename)

    if where is None:
        keys = params.keys()
        ps = []
        values = []
        where = ""
        if len(keys) > 0:                    #存在查询条件时，以与方式组合
            for key in keys:
                ps.append(key + " =%s ")
                values.append(params[key])
            where += ' where ' + ' and '.join(ps)
        cur = conn.cursor()
        cur.execute(sql + where + order + limit, values)

    else:
        cur = conn.cursor()
        cur.execute(sql + ' where ' + where + order + limit)
    ret = cur.fetchall()
    cur.close()
    conn.close()
    return ret