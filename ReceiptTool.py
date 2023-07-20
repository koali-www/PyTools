import pdfplumber as pf
import re
import pathlib
# import pathlib2
from openpyxl import Workbook


basedir = "xxxxx"
files = pathlib.Path(basedir).glob('**/*.pdf')
data = []
for path in files:
    try:
        with pf.open(path) as pdf:
            p = pdf.pages[0]
            text = p.extract_text().replace(' ', '')
            code = re.sub(r'\D', "", re.search(
                '发票代码[：|:][0-9]{12}', text).group())
            date = re.sub(r'开票日期[：|:]', "", re.search(
                '开票日期[：|:][0-9]{4}年[0-9]{2}月[0-9]{2}日', text).group())
            sum = re.sub(r'[(|（]小写[)|）][￥|¥]', "", re.search(
                '[(|（]小写[)|）][￥|¥][0-9]*\.[0-9]{2}', text).group())
            print(code, date, sum)
            data.append([path.name, code, date, sum])
    except:
        print('error path:', path)
print(data)
wb = Workbook()
ws = wb.create_sheet("发票单统计")
ws.append(['发票文件名', '发票代码', '开票时间', '金额(总计)'])
total = 0
for i in data:
    ws.append(i)
    total += float(i[-1])
# print(total)
ws.append(['', '', '总计', total])

wb.save(basedir+"\\detail.xlsx")
