# -*- coding:utf-8 -*-

import time
import os

DBUSER='myadmin'
DBPASS='redhat'
IP='192.168.122.1'       #将数据导入改主机
DATA_DIR='/data'
PATH_RES='/usr/local/mongodb/bin/mongorestore'
BACKITEMS=[

    "%s -h %s:27017 --dir %s" % (PATH_RES,IP,DATA_DIR)
]

def backData():
    try:
       for item in BACKITEMS:
           print(item )
           print (os.system(item) )
    except RuntimeError,e:
        print( str(e) )

if __name__=="__main__":

    backData()

