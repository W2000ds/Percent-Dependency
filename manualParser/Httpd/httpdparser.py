# -*- coding: utf-8 -*-
import re
from lxml import etree
from lxml.html import fromstring
# from StringIO import StringIO
import csv
import os
import re
oplist = []
deps = []
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
    xml = f.read()
    f.close()
    doc = fromstring(xml)
    html = etree.HTML(xml)
    for div in doc.find_class('directive-section'):
        for h2 in div.iter('h2'):
            for a in h2.iter('a'):
                print(a.text)
                oplist.append(a.text)
                break
        dep = ""
        for code in div.find_class('directive'):
            for a in code.iter('a'):
                if a.text.strip().find(':')==-1:
                    print(a.text.strip()+'!!!!!')
                    dep = dep + a.text.strip().replace(':', '') + ' '
        deps.append(dep)
        desc = ""
        for p in div.iter('p'):
            if p.text is not None:
                desc = desc + ' '+ trim(p.text.replace('\n',''))
        descs.append(desc)



def getdep():
    dependency = {}

    for i in range(len(oplist)):
        dep = deps[i].split(' ')

        for cell in dep:
            p = oplist[i]
            if (cell in oplist and cell != p):
                if p in dependency:
                    if dependency[p].find(cell) == -1:
                        dependency[p] = dependency[p] + ' ' + cell
                else:
                    dependency[p] = cell
    csvfile = open('dependency.csv', 'w+')
    writer = csv.writer(csvfile)
    for op in dependency:
        param = [op]
        depen = dependency[op].split(' ')
        param.extend(depen)
        writer.writerow(param)
    csvfile.close()

    csvfile = open('httpdconfig.csv', 'w+')
    writer = csv.writer(csvfile)
    for i in range(len(oplist)):
        param = [oplist[i],descs[i]]
        writer.writerow(param)
    csvfile.close()

def trim(text):
    return re.sub(r'^\s+|\s+$', '', text)


if __name__ == "__main__":
    get_all_parameter_desc('./manuals/')
    getdep()