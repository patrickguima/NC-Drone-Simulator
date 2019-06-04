import xlsxwriter
def write_xlsm(metrics):


    workbook = xlsxwriter.Workbook('resultadosNCDrone.xlsx')
    worksheet = workbook.add_worksheet()

# Some data we want to write to the worksheet.
    expenses = (
        ['num', 'qmi', 'sdf', 'ncc','ntm'],

    )

# Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

# Iterate over the data and write it out row by row.
    for num, qmi,sdf,ncc,ntm in (expenses):
        worksheet.write(row, col,     num)
        worksheet.write(row, col + 1, qmi)
        worksheet.write(row, col + 2, sdf)
        worksheet.write(row, col + 3, ncc)
        worksheet.write(row, col + 4, ntm)
        row += 1

    for num, qmi,sdf,ncc,ntm in metrics:
        worksheet.write(row, col,     num)
        worksheet.write(row, col + 1, qmi)
        worksheet.write(row, col + 2, sdf)
        worksheet.write(row, col + 3, ncc)
        worksheet.write(row, col + 4, ntm)
        row += 1




    workbook.close()

