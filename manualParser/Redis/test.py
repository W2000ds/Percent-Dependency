import re
from lxml import etree
from lxml.html import fromstring
# from StringIO import StringIO
import csv
import os
import re
oplist = []
descs = []
def get_all_parameter_desc(page_dir):

    """    Step 1. Collect all the paraemters
    This is used for filter out incorrect parsing results
    """
    flist = os.listdir(page_dir)
    for fp in flist:
        #print path + fp
        get_parameter_list(page_dir + fp)

def get_parameter_list(path):
    """
    Extract all the parameters from the given html file (path)
    """

    f = open(path,encoding='utf-8')
    lines = f.readlines()
    f.close()
    lastindex = 0
    for index, line in enumerate(lines):
        line = trim(line)
        if len(line.split(' '))==2:
            if line.split(' ')[0].find(':')==-1 and line.split(' ')[0].find(')')==-1 and line.split(' ')[1].find(':')==-1 and line.split(' ')[1].find(')')==-1 and not line.split(' ')[1].endswith('.'):
                opname = line.split(' ')[0]
                print(line)
                desc = ''
                for i in range(lastindex,index):
                    desc = trim(desc + lines[i].replace('\n',''))
                lastindex = index + 1
                oplist.append(opname)
                descs.append(desc)
    csvfile = open('redisconfig.csv', 'w+')
    writer = csv.writer(csvfile)
    for i in range(len(oplist)):
        param = [oplist[i],descs[i]]
        writer.writerow(param)
    csvfile.close()

def trim(text):
    return re.sub(r'^\s+|\s+$', '', text)

def getdep(oplist,descs):
    count = {}
    dependency = {}
    for i in range(len(oplist)):
        descp = descs[i].split(' ')

        for cell in descp:
            p = oplist[i]
            if (cell in oplist and cell != p):
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

if __name__ == "__main__":
    get_all_parameter_desc('./manuals/')
    getdep(oplist,descs)