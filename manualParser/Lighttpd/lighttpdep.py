import re
import csv

# with open("lighttpdmanual.csv", "rt") as csvfile:
#     reader = csv.reader(csvfile)
#     desc = [row[1] for row in reader]
opname= []
desc = []

with open("lighttpdmanual.csv", "rt") as csvfile1:
    reader1 = csv.reader(csvfile1)
    for row in reader1:
        opname.append(row[0].split('\t')[0])
        if(row[0].split('\t')[0]=="usertrack.cookie-max-age"):
            break
        print(row[0].split('\t')[0])
        if(not row[0].split('\t')[1]):
            desc.append(' ')
            continue
        desc.append(row[0].split('\t')[1])


desc.append('deprecated; subsumed by usertrack.cookie-attrs since lighttpd 1.4.46')
#search for dependency
count = {}
dependency={}
for i in range(len(opname)):
   descp = desc[i].split(' ')

   for cell in descp:
       p = opname[i]
       if (cell in opname and cell!=p):
           if p in dependency:
               if dependency[p].find(cell) == -1:
                   dependency[p] = dependency[p] + ' ' + cell
           else:
               dependency[p] = cell


# print to file

csvfile = open('dependency.csv', 'w+')
writer = csv.writer(csvfile)
for op in dependency:
        param = [op]
        depen = dependency[op].split(' ')
        param.extend(depen)
        writer.writerow(param)
csvfile.close()


