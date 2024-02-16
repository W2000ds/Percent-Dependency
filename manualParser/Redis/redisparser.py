# -*- coding: utf-8 -*-
import re
from lxml import etree
from lxml.html import fromstring
# from StringIO import StringIO
import csv
import os
import re

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
    xml = f.read()
    f.close()
    doc = fromstring(xml)
    oplist = []
    html = etree.HTML(xml)
    for a in doc.find_class('wiki wiki-page'):
        for table in a.iter('table'):
            for tbody in table.iter('tbody'):
                for tr in tbody.iter('tr'):
                    print()
                    for td in tr.iter('td'):
                        print(trim(td.text)+'#',end='')

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
    getdep()
