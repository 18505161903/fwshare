# -*- coding:utf-8 -*-

import time
import os

DBUSER='myadmin'        #用户
DBPASS='redhat'           #密码
IP='192.168.122.11'        #主机
DATA_DIR='/data'           #目录
PATH_DUMP='/usr/local/mongodb/bin/mongodump'    #命令路径
BACKITEMS=[     "%s -h %s:27017 -u %s -p %s -o %s" % (PATH,IP,DBUSER,DBPASS,DATA_DIR) ]

def backData():
    try:
        for item in BACKITEMS:
            print(item)
            print(os.system(item))
    except RuntimeError,e:
        print(str(e))

if __name__=="__main__":
    backData()