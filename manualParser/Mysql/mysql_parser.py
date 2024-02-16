# -*- coding: utf-8 -*-

from lxml import etree
from lxml.html import fromstring
# from StringIO import StringIO
import csv
import os
import re

def get_all_parameter_desc(page_dir):
    option_list = []
    option_desc = {}
    """
    Step 1. Collect all the paraemters
    This is used for filter out incorrect parsing results
    """
    flist = os.listdir(page_dir)
    for fp in flist:
        #print path + fp
        opl =   get_parameter_list(page_dir + fp)
        for o in opl:
            if o not in option_list:
                option_list.append(o)
    print ('Number of options', len(option_list))
    """
    Step 2. Get all the description 
    """
    for fp in flist:
        opdesc = get_parameter_desc(page_dir + fp, option_list)
        for opd in opdesc:
            if opd not in option_desc:
                option_desc[opd] = opdesc[opd]
            else:
                if option_desc[opd].find(opdesc[opd]) == -1:
                    option_desc[opd] = opdesc[opd] + ' ' + option_desc[opd]
            option_desc[opd] = option_desc[opd].replace('\n', ' ').replace('-', '').replace('      ',' ')
    print ('Number of option desc:', len(option_desc))
    """
    Step 3. print to file
    """
    csvfile = open('mysqlparam2.csv','w')
    writer = csv.writer(csvfile)

    for op in option_desc:
        desc = re.sub(' +', ' ', option_desc[op]).replace('\n',' ').encode(encoding='utf-8')
        param = [op, desc]
        writer.writerow(param)

    csvfile.close()


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
    for i in range(1,343):
        print(i)
        if i == 110 or i == 203 or i== 334:
            continue
        a = html.xpath(f'//*[@id="docs-body"]/div/div[5]/ul/li[{i}]/p[1]/a[2]/code')[0]
        opname = a.text;
        if opname.find(':') != -1:
           opname = opname[opname.find(':')+1:]
           opname = opname.strip()
        if opname not in oplist:
           oplist.append(opname)

    return oplist
def get_parameter_desc(path, oplist):
    """
    Extract the parameters' desc from the given html page (path),
    oplist is used to filter irrelevant results
    """
    f = open(path,encoding='utf-8')
    xml = f.read()
    f.close()
    doc = fromstring(xml)
    opdesc = {}
    for item in doc.find_class('listitem'):
        #get the option name
        opname = None
        #sometimes its option sometimes its literal
        for pb in item.iter('p'):
            for option in pb.find_class('option'):
                opname = norm(option.text_content())
                break
            if opname == None:
                for option in pb.find_class('literal'):
                    opname = norm(option.text_content())
                    break
                break
        if opname in oplist:
            #we want to skip the informaltable
            itxt = ''
            for p in item.iter('p'):
                itxt = p.text_content().strip() + ' '
                if itxt.strip() == opname:
                    continue
                if opname in opdesc:
                    if opdesc[opname].find(itxt) == -1:
                         opdesc[opname] = opdesc[opname] + ' ' + itxt
                else:
                    opdesc[opname] = itxt
    return opdesc 

def norm(pstr):
    """
    pstr is a parameter string
    """
    par = pstr
    if par.startswith('--'):
        par = par[2:]
    par = par.replace('-', '_')
    if par.find('=') != -1:
        par = par[:par.find('=')]
    if par.find('[') != -1:
        par = par[:par.find('[')]
    return  par.strip()

if __name__ == "__main__":
    #manpage = '/home/tixu/software/mysql-doc-online/5.6/innodb-parameters.html'
    #plist = get_parameter_list(manpage)
    #pdesc = get_parameter_desc(manpage, plist)
    #print len(pdesc)
    get_all_parameter_desc('./newnewmanuals/')
