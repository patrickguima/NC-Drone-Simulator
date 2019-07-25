
import xlsxwriter
import statistics
def write_xlsm(metrics):


    workbook = xlsxwriter.Workbook('resultadosNCDrone.xlsx')
    worksheet = workbook.add_worksheet()

# Some data we want to write to the worksheet.
    expenses = (
        ['Num', 'Qmi', 'Sdf', 'Ncc','Manobras'],

    )
  #  labels = (['Media Qmi','DP','Media SDF','DP','Media Manobras','DP'])
    QMI = []
    SDF = []
    MANOBRAS = []
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
        QMI.append(qmi)
        SDF.append(sdf)
        MANOBRAS.append(ntm)
        worksheet.write(row, col,     num)
        worksheet.write(row, col + 1, qmi)
        worksheet.write(row, col + 2, sdf)
        worksheet.write(row, col + 3, ncc)
        worksheet.write(row, col + 4, ntm)
        row += 1
    col = 6
    row = 0
   
    worksheet.write(row, col,     "Media Qmi")
    worksheet.write(row, col + 1, "DP")
    worksheet.write(row, col + 2, "Media SDF")
    worksheet.write(row, col + 3, "DP")
    worksheet.write(row, col + 4, "Media Manobras")
    worksheet.write(row, col + 5, "DP")
    row += 1



    worksheet.write(row, col,     statistics.mean(QMI))
    worksheet.write(row, col + 1, statistics.stdev(QMI))
    worksheet.write(row, col + 2, statistics.mean(SDF))
    worksheet.write(row, col + 3, statistics.stdev(SDF))
    worksheet.write(row, col + 4, statistics.mean(MANOBRAS))
    worksheet.write(row, col + 5, statistics.stdev(MANOBRAS))


    workbook.close()

