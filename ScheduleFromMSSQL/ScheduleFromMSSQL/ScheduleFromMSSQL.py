import pypyodbc
import pandas as pd
import datetime
import csv


pd.options.mode.chained_assignment = None # turn off SettingWithCopyWarning

def find_sat(MEOLUT ,ant_i, time, databasename='MccTestLGM'):
    conn = pypyodbc.connect(r'Driver={SQL Server};Server=.\SQLEXPRESS;Database='+databasename+';Trusted_Connection=yes;')
    c = conn.cursor()
    query_params = [MEOLUT, time, time, ant_i]
    sql_query = ('SELECT "SAT ID", "LUT ID", ANTENNA from schedule '
        'WHERE '
        '"LUT ID" like ? '
        'AND '
        'AOS < ? '
        'AND '
        'LOS > ? '
        'AND '
        'ANTENNA like ? ' )
    c.execute(sql_query, query_params)
    packets = c.fetchall()
    return packets

MEOLUTlist = [3385, 3669]
antlist = range(1,7)
time = '2017-01-29 18:00'
numdays = 1
minute_inc = 5
time1 = datetime.datetime(2017,1,30,0,0)

print time1
timelist = [time1 + datetime.timedelta(minutes=x) for x in range(0, numdays*24*60, minute_inc)]


for MEOLUT in MEOLUTlist:
    satlist = []
    for time in timelist:
        satlist2 = []
        for ant_i in antlist:
            sats = find_sat(MEOLUT, ant_i, time)
            if ant_i == 1:
                satlist2.append(time)
            if sats:
                satlist2.append(int(sats[0][0]))
            else:
                satlist2.append(None)
        satlist.append(satlist2)
    with open(str(MEOLUT) + "output.csv",'wb') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerows(satlist)




