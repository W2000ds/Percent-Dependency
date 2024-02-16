import re
import csv

with open("HBase.csv", "rt") as csvfile:
    reader = csv.reader(csvfile)
    desc = [row[1] for row in reader]

with open("HBase.csv", "rt") as csvfile1:
    reader1 = csv.reader(csvfile1)
    opname = [row[0] for row in reader1]

#search for dependency
count = {}
dependency={}
for i in range(len(opname)):
   # descp = desc[i].split(' ')
   descp = re.split(' |,',desc[i])
   for cell in descp:
       p = opname[i]
       if (cell in opname and cell!=p):
           if p in dependency:
               if dependency[p].find(cell) == -1:
                   dependency[p] = dependency[p] + ' ' + cell
           else:
               dependency[p] = cell



# print to file

csvfile = open('HbaseManualDep.csv', 'wb+')
writer = csv.writer(csvfile)
for op in dependency:
        depen = dependency[op].encode()
        param = [op.encode(),dependency[op].encode()]
        print(op+' '+dependency[op])
csvfile.close()


