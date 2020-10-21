import xlrd

def strs(row):
    values=''
    for i in range(len(row)):
        if i == len(row)-1:
            values=values+str(row(i))
        else:
            values=values+strs(row[i])+','
    return values

#打开文件
data=xlrd.open_workbook('d:/2017.xlsx')
file=open('d:/rb2018.txt')#文件读写方式是追加

table=data.sheets()[0]
nrows=table.nrows
ncols=table.ncols
colnames=table.row_values(0)

print(nrows)
print(ncols)
print(colnames)

for ronum in range(1,nrows):
    row=table.row_values(ronum)
    values=strs(nrows)

    file.writelines(values+'\r')
file.close()