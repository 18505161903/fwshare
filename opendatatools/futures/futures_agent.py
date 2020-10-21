# encoding: utf-8

from opendatatools.common import RestAgent, split_date, date_convert, remove_chinese
import pandas as pd
import numpy as np
import json
import zipfile
import io
import re
from xml.etree import ElementTree
import string


def transform(df):
    df = df.copy()
    try:
        # 丢掉合计
        df = df[df.名次 != "合计"]
    except:
        pass
    for index in [2, 3, 4, 5, 6, 8, 9]:
        # 千分位处理
        if df[df.columns[index]].dtypes.__str__() == 'object':
            df[df.columns[index]] = df[df.columns[index]].map(lambda x: x.replace(",", "") if isinstance(x, str) else x)
        else:
            df[df.columns[index]] = df[df.columns[index]].map(lambda x: '%.2f' % x if isinstance(x, (int, float)) else x)
    return df


def format_field(x):
    if type(x) == str:
        return x.replace('\n', '').strip()
    else:
        return x


def _merge_df(df_list):
    df_result = None
    for df in df_list:
        if df_result is None:
            df_result = df
        else:
            df_result = pd.merge(df_result, df, left_index=True, right_index=True)
    return df_result


def _concat_df(df_list):
    return pd.concat(df_list)


def _rename_df(df):
    name_map = {
        "会员简称": "期货公司",
        "（手）": "",
    }
    for col in df.columns:
        for name, value in name_map.items():
            if name in col:
                col_new = col.replace(name, value)
                df.rename(columns={col: col_new}, inplace=True)


class SHFAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    # date : %Y%m%d
    def get_trade_rank(self, date):
        url = 'http://www.shfe.com.cn/data/dailydata/kx/pm%s.dat' % date_convert(date, '%Y-%m-%d', '%Y%m%d')
        response = self.do_request(url, None)
        rsp = json.loads(response.encode('utf-8'))

        code = rsp['o_code']
        msg = rsp['o_msg']
        date_int = int(date_convert(date, '%Y-%m-%d', "%Y%m%d"))
        if code != 0:
            return None, msg

        if 'report_date' in rsp.keys():
            date = rsp['report_date']
        else:
            date = str(date_int)
        records = rsp['o_cursor']
        # print(records)
        # input()
        df = pd.DataFrame(records)
        df['date'] = date[:4] + '-' + date[4:6] + '-' + date[6:]

        for col in df.columns:
            df[col] = df[col].apply(lambda x: format_field(x))

        df['RANK'] = df['RANK'].apply(lambda x: int(x))
        df = df[(df['RANK'] > 0) & (df['RANK'] <= 20)]
        df.rename(columns={"CJ1": "成交量"}, inplace=True)
        df.rename(columns={"CJ1_CHG": "成交量增减"}, inplace=True)
        df.rename(columns={"PARTICIPANTABBR1": "成交量期货公司"}, inplace=True)
        df.rename(columns={"CJ2": "持买仓量"}, inplace=True)
        df.rename(columns={"CJ2_CHG": "持买仓量增减"}, inplace=True)
        df.rename(columns={"PARTICIPANTABBR2": "持买仓量期货公司"}, inplace=True)
        df.rename(columns={"CJ3": "持卖仓量"}, inplace=True)
        df.rename(columns={"CJ3_CHG": "持卖仓量增减"}, inplace=True)
        df.rename(columns={"PARTICIPANTABBR3": "持卖仓量期货公司"}, inplace=True)
        df.rename(columns={"RANK": "名次"}, inplace=True)
        df.rename(columns={"INSTRUMENTID": "symbol"}, inplace=True)
        try:
            df.drop(['PARTICIPANTID1', 'PARTICIPANTID2', 'PARTICIPANTID3', 'PRODUCTNAME', 'PRODUCTSORTNO'], axis=1,
                    inplace=True)
        except:
            try:
                df.drop(['PRODUCTSORTNO', 'PRODUCTNAME'], axis=1, inplace=True)
            except:
                df.drop(['PRODUCTSORTNO'], axis=1, inplace=True)
        # df['variety'] = df['symbol'].apply(lambda x: re.search(r'([\s\S]*?)\d', x).group(1))
        df['variety'] = df['symbol'].apply(lambda x: x.replace(' ', '').rstrip(string.digits))
        data2 = pd.DataFrame()
        for name, data in df.groupby('symbol'):
            data = data.copy()
            # 丢掉合计列
            # data.loc['合计'] = \
            data.iloc[:, :6].apply(lambda x: x.replace('', np.nan)).apply(lambda x: x.sum(skipna=True))
            # print(data)
            data2 = pd.concat([data2, data])
        cols = list(data2)
        cols.insert(0, cols.pop(cols.index('名次')))
        cols.insert(-1, cols.pop(cols.index('symbol')))
        cols.append(cols.pop(cols.index('date')))
        cols.insert(1, cols.pop(cols.index('成交量期货公司')))
        cols.insert(4, cols.pop(cols.index('持买仓量期货公司')))
        cols.insert(7, cols.pop(cols.index('持卖仓量期货公司')))
        df = data2.loc[:, cols]

        # input()
        # print(df)
        return transform(df), ""


class DCEAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    '''
    名次		会员简称	成交量		增减		
    1		海通期货	24,326		9,991		
    2		中信期货	12,926		5,960		
    3		兴证期货	12,835		4,405		
    4		西南期货	11,054		6,614		
    '''

    def _parse_trade_file(self, file, old=False):
        filename = file.name.encode('cp437').decode('gbk')

        name_items = filename.split("_")
        symbol = name_items[1]

        lines = file.readlines()
        df_list = []
        if old == False:
            for i in range(len(lines)):
                items = lines[i].decode('utf8').split()
                if len(items) == 4 and items[0] == '名次':
                    head = items

                    head[1] = head[2] + head[1]
                    head[3] = head[2] + head[3]

                    data = []
                    for j in range(20):
                        i = i + 1
                        items = lines[i].decode('utf8').split()

                        if items[0] == '总计':
                            break
                        data.append(items)
                    if data == []:
                        data.append(['', '', '', ''])
                    df = pd.DataFrame(data)
                    df.columns = head
                    df.set_index('名次', inplace=True)
                    df_list.append(df)

            df_result = _merge_df(df_list)
            df_result['symbol'] = symbol
            df_result['variety'] = re.search(r'([\s\S]*?)\d', symbol).group(1)

        else:
            for i in range(len(lines)):
                items = lines[i].decode('gbk').split()
                if len(items) == 4 and items[0] == '名次':
                    head = items

                    head[1] = head[2] + head[1]
                    head[3] = head[2] + head[3]

                    data = []
                    for j in range(20):
                        i = i + 1
                        items = lines[i].decode('gbk').split()

                        if items[0] == '总计':
                            break
                        data.append(items)
                    if data == []:
                        data.append(['', '', '', ''])
                    df = pd.DataFrame(data)
                    df.columns = head
                    df.set_index('名次', inplace=True)
                    df_list.append(df)

            df_result = _merge_df(df_list)
            df_result['symbol'] = symbol
            df_result['variety'] = re.search(r'([\s\S]*?)\d', symbol).group(1)
        return df_result

    def get_trade_rank(self, date):
        date_int = int(date_convert(date, '%Y-%m-%d', "%Y%m%d"))
        url = 'http://www.dce.com.cn/publicweb/quotesdata/exportMemberDealPosiQuotesBatchData.html'
        # url = 'http://www.dce.com.cn/publicweb/quotesdata/exportMemberDealPosiQuotesData.html'
        year, month, day = split_date(date, '%Y-%m-%d')
        data = {
            "year": year,
            "month": month - 1,  # 脑残程序员的设计
            "day": day,
            "batchExportFlag": 'batch',
        }

        response = self.do_request(url, data, "POST", type='binary')
        zip_ref = zipfile.ZipFile(io.BytesIO(response))
        df_list = []
        for finfo in zip_ref.infolist():
            file = zip_ref.open(finfo, 'r')
            if date_int > 20151231:
                df = self._parse_trade_file(file)
            else:
                df = self._parse_trade_file(file, old=True)
            df_list.append(df)

        df_result = _concat_df(df_list)
        df_result['date'] = date
        df_result.reset_index(level=['名次'], inplace=True)

        _rename_df(df_result)
        return transform(df_result), ""


class CZCAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    '''
    品种：苹果AP              日期： 2018-05-30
    名次  |会员简称      |成交量（手）|增减量    |会员简称      |持买仓量  |增减量    |会员简称      |持卖仓量  |增减量
    1     |海通期货      |157,955     |-2,663    |海通期货      |42,771    |3,342     |海通期货      |43,889    |1,843     
    2     |招商期货      |67,527      |-12,527   |华泰期货      |21,091    |-1,093    |华泰期货      |20,927    |-1,991    
    3     |徽商期货      |66,887      |-29,680   |招商期货      |17,302    |-3,063    |招商期货      |20,519    |-2,788    
    4     |光大期货      |66,322      |-10,134   |永安期货      |17,193    |784       |中信期货      |15,779    |716       
    '''

    def _get_code(self, text):
        items = re.split("：| |\t|\r\n|", text)
        return items[1]

    def _get_head(self, text, old=False):
        items = ['', '', '', '', '', '', '', '']
        if old == False:
            items = self._split_field(text)
            items[1] = '成交量' + items[1]
            items[3] = '成交量增减'
            items[4] = '持买仓量' + items[4]
            items[6] = '持买仓量增减'
            items[7] = '持卖仓量' + items[7]
            items[9] = '持卖仓量增减'
        else:
            items = ['名次', '成交量期货公司', '成交量', '成交量增减', '持买仓量期货公司', '持买仓量', '持买仓量增减', '持卖仓量期货公司', '持卖仓量', '持卖仓量增减']
        return items

    def _get_data(self, lines, old=False):
        data = []
        if old == False:
            for line in lines:
                items = self._split_field(line)
                data.append(items)
        else:
            for line in lines:
                items = self._split_field(line, ',')
                data.append(items)
        return data

    def _split_field(self, text, splitter="|"):
        items = text.split(splitter)
        result = [str(x).strip().replace('\r\n', '') for x in items]
        return result

    def _parse_trade_file(self, file, old=False):
        lines = file.readlines()
        df_list = []
        if old == False:
            for i in range(len(lines)):
                items = self._split_field(lines[i])
                if len(items) == 10 and items[0] == '名次':
                    code = self._get_code(lines[i - 1])
                    heads = self._get_head(lines[i])
                    a = i
                    while True:
                        a += 1
                        items = self._split_field(lines[a])
                        # print(items)
                        if items[0] == '合计':
                            data = self._get_data(lines[i + 1:a + 1])
                            break
                    # print(data)
                    # print(code)

                    df = pd.DataFrame(data)
                    df.columns = heads
                    df['symbol'] = remove_chinese(code)
                    # print(df['symbol'])
                    # input()
                    df['variety'] = df['symbol'].apply(lambda x: re.search(r'([a-zA-Z]*)', x).group(1))
                    # print(df)
                    # input()
                    df_list.append(df)
        else:
            for i in range(len(lines)):
                items = self._split_field(lines[i], splitter=',')
                if items[0][0:2] == '合约':
                    code = self._get_code(lines[i])
                    heads = self._get_head(lines[i], old=True)
                    a = i
                    while True:
                        a += 1
                        items = self._split_field(lines[a], splitter=',')
                        # print(items)
                        if items[0] == '合计':
                            data = self._get_data(lines[i + 1:a + 1], old=True)
                            break
                    # print(code)
                    data[-1].insert(1, '')
                    df = pd.DataFrame(data)
                    df.columns = heads
                    df['symbol'] = remove_chinese(code)
                    # print(df['symbol'])
                    # input()
                    df['variety'] = df['symbol'].apply(lambda x: re.search(r'([a-zA-Z]*)', x).group(1))
                    # print(df)
                    # input()
                    df_list.append(df)
        df_result = _concat_df(df_list)

        return df_result

    def get_trade_rank(self, date):

        url = 'http://old.czce.com.cn/portal/DFSStaticFiles/Future/%d/%d/FutureDataHolding.txt'
        url_old = 'http://old.czce.com.cn/portal/exchange/%d/datatradeholding/%d.txt'

        year, month, day = split_date(date, '%Y-%m-%d')
        date_int = int(date_convert(date, '%Y-%m-%d', "%Y%m%d"))
        if date_int < 20151001:
            url_old = url_old % (year, date_int)
            response = self.do_request(url_old, None, "GET", type='binary')
            df = self._parse_trade_file(io.StringIO(response.decode('gbk')), old=True)
            df['date'] = date
            _rename_df(df)
        else:
            url = url % (year, date_int)
            response = self.do_request(url, None, "GET", type='binary')
            df = self._parse_trade_file(io.StringIO(response.decode('gbk')))
            df['date'] = date
            _rename_df(df)
        df = df[df.variety == df.symbol]
        return transform(df), ""


class CFEAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)

    def get_trade_rank(self, date):
        products = ['T', 'IF', 'IC', 'IH', 'TF']
        df_list = []
        for product in products:
            df = self._get_trade_rank_by_product(date, product)
            df_list.append(df)

        df = _concat_df(df_list)
        df['date'] = date
        df.reset_index(level=[0, 1], inplace=True)
        df['variety'] = df['symbol'].apply(lambda x: re.search(r'([a-zA-Z]*)', x).group(1))

        cols = list(df)
        cols.insert(-1, cols.pop(cols.index('symbol')))
        cols.append(cols.pop(cols.index('date')))

        cols.insert(2, cols.pop(cols.index('成交量')))
        cols.insert(5, cols.pop(cols.index('持买单量')))
        cols.insert(8, cols.pop(cols.index('持卖单量')))

        df = df.loc[:, cols]
        return transform(df), ""

    def _get_trade_rank_by_product(self, date, product):
        url = 'http://www.cffex.com.cn/sj/ccpm/%04d%02d/%02d/%s.xml'
        year, month, day = split_date(date, '%Y-%m-%d')
        url = url % (year, month, day, product)

        response = self.do_request(url, None, "GET")
        root = ElementTree.fromstring(response)
        data_list = []
        for dataElements in root:
            if dataElements.tag != 'data':
                continue

            data = {}
            for subElement in dataElements:
                key = subElement.tag
                value = subElement.text
                if key in ['instrumentid', 'datatypeid', 'rank', 'shortname', 'volume', 'varvolume']:
                    data[key] = value
                    # print(data[key])
                    # print(data)
            data_list.append(data)

        df = pd.DataFrame(data_list)

        datatype_map = {
            "0": "成交量",
            "1": "持买单量",
            "2": "持卖单量",
        }

        df_list = []
        for type, name in datatype_map.items():
            # warnning
            df_tmp = df[df['datatypeid'] == type].copy()
            df_tmp['rank'] = df_tmp['rank'].apply(lambda x: int(x))
            df_tmp.rename(columns={"instrumentid": "symbol"}, inplace=True)
            df_tmp.rename(columns={"rank": "名次"}, inplace=True)
            df_tmp.rename(columns={"shortname": name + "期货公司"}, inplace=True)
            df_tmp.rename(columns={"volume": name}, inplace=True)
            df_tmp.rename(columns={"varvolume": name + "增减"}, inplace=True)
            # print(df_tmp)
            df_tmp.drop(['datatypeid'], axis=1, inplace=True)
            df_tmp.set_index(['symbol', '名次'], inplace=True)
            df_list.append(df_tmp)

        return _merge_df(df_list)