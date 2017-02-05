import pypyodbc
import pandas as pd
import datetime
import csv
import collections


pd.options.mode.chained_assignment = None # turn off SettingWithCopyWarning
def makehash():
    return collections.defaultdict(makehash)

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
numdays = .1
minute_inc = 5
time1 = datetime.datetime(2017,1,30,0,0)

print time1
timelist = [time1 + datetime.timedelta(minutes=x) for x in range(0, int(numdays*24*60), minute_inc)]

satdict = makehash()
for MEOLUT in MEOLUTlist:
    satlist = []
    #MEOdict = {}
    for time in timelist:
        satlist2 = []
        for ant_i in antlist:
            #antdict = {}
            #satdict[MEOLUT][ant_i] = {}
            sats = find_sat(MEOLUT, ant_i, time)
            
            if ant_i == 1:
                satlist2.append(time)
            if sats:
                satlist2.append(int(sats[0][0]))
                satdict[MEOLUT][ant_i][time] = int(sats[0][0])
            else:
                satlist2.append(None)
                satdict[MEOLUT][ant_i][time] = None
        satlist.append(satlist2)
    #with open(str(MEOLUT) + "output.csv",'wb') as resultFile:
    #    wr = csv.writer(resultFile, dialect='excel')
    #    wr.writerows(satlist)

df1 = pd.DataFrame(satlist2)
df2 = pd.DataFrame.from_dict(satdict)
print 'df1'
print df1.head(5)
print 'df2'
print df2.head(5)
print 'sat dict[1]'
print satdict[3669][1]





