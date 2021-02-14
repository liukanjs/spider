# coding:utf-8
import xlwt
import xlrd


class Excel(object):
    def read_to_dict(self, filename):
        book = xlrd.open_workbook(filename)  # 打开要读取的Excel
        sheet = book.sheet_by_name('Sheet1')  # 打开sheet页
        rows = sheet.nrows  # sheet页里面的行数
        columns = sheet.ncols  # sheet页里面的列数
        print(sheet.cell(1, 2).value)  # 通过制定行和列去获取到单元格里的内容

        row_data = sheet.row_values(2)  # 获取第一行的内容
        print(row_data)

        for i in range(rows):
            print(sheet.row_values(i))  # 获取第几行的数据

        # return sheet

    def write(self):
        pass
