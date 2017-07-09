#coding:utf-8
import classes import DBHelper

if __name__ == '__main__':
    sql = 'select from domain_table where lan like "en:%"'
    d = DBHelper()
    d.oncesql