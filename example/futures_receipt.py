#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import re
import json
import requests
import datetime

HEADER = [u'日期', u'品种', u'期货仓单', u'仓单变化']
OUTPUT_CSV_PATH = "./receipt.csv"
URL_TEMPL = "http://www.shfe.com.cn/data/dailydata/{}dailystock.dat"


def write_to_csv(datas, header):
    if os.path.exists(OUTPUT_CSV_PATH):
        os.remove(OUTPUT_CSV_PATH)

    with open(OUTPUT_CSV_PATH, 'w+') as f:
        f.write(",".join(header))
        f.write("\n")
        for line in datas:
            f.write(",".join(map(lambda x: str(x), line)))
            f.write("\n")


def check_proc_params(start_date_str, end_date_str):
    def check_date_format(date_str):
        if re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
            return True
        else:
            return False

    date_list = []
    if check_date_format(start_date_str) and \
        check_date_format(end_date_str):
        year_start, month_start, day_start = start_date_str.split("-")
        year_end, month_end, day_end = end_date_str.split("-")
        start_date = datetime.date(int(year_start),
                                   int(month_start),
                                   int(day_start))
        end_date = datetime.date(int(year_end),
                                 int(month_end),
                                 int(day_end))
        delta_days = (end_date-start_date).days
        if delta_days>=0:
            for i in range(0, delta_days+1):
                date = start_date+datetime.timedelta(days=i)
                date_list.append(date.strftime('%Y%m%d'))
            return date_list
        else:
            print("input params end_date is earlier than start_date")
            raise Exception
    else:
        return None


def get_inventory_data(start_date, end_date):
    print("start_date is {}, end_date is {}".format(start_date, end_date))
    date_list = check_proc_params(start_date, end_date)
    datas = []
    for date_str in date_list:
        url = URL_TEMPL.format(date_str)
        resp = requests.get(url)
        if resp.status_code == 404:
            continue
        elif resp.status_code != 200:
            print("the resp status code of date({}) is {}".format(date_str, resp.status_code))
        jsonObj = json.loads(resp.content.decode('utf-8'))
        tradingday = jsonObj['o_tradingday']
        for idx, l in enumerate(jsonObj['o_cursor']):
            if not re.match(r'\S+?\$\$Total$', l['WHABBRNAME']):
                continue
            datas.append([tradingday, l['VARNAME'].split('$$')[0],
                          l['WRTWGHTS'], l['WRTCHANGE']])

    write_to_csv(datas, HEADER)


if __name__ == '__main__':

    get_inventory_data('2018-11-07', '2018-11-07')