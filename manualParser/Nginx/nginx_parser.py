# -*- coding: utf-8 -*-

from lxml import etree
from lxml.html import fromstring
# from StringIO import StringIO
import csv
import os
import re

def get_all_parameter_desc(page_dir):
    option_list = []
    option_desc = []
    """
    Step 1. Collect all the paraemters
    This is used for filter out incorrect parsing results
    """
    flist = os.listdir(page_dir)
    for fp in flist:
        #print path + fp
        opl = get_parameter_list(page_dir + fp)
        for o in opl:
            if o not in option_list:
                option_list.append(o)
    print ('Number of options', len(option_list))
    """
    Step 2. Get all the description 
    """
    for fp in flist:
        opdesc = get_parameter_desc(page_dir + fp, option_list)



    """
    Step 3. print to file
    """
    csvfile = open('nginxconfigs.csv','w')
    writer = csv.writer(csvfile)

    for op in opdesc:
        opname = re.sub(' +', ' ', op['name']).encode(encoding='utf-8')
        desc = re.sub(' +', ' ', op['desc']).encode(encoding='utf-8')
        param = [opname, desc]
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
    for i in range(1,80):
        print(i)
        a = html.xpath(f'//*[@id="content"]/div[{i}]/table/tbody/tr[1]/td/code/strong')[0]
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
    div_element = doc.xpath('//*[@id="content"]')[0]
    opdesc = []

    i = -1
    for child in div_element.iterchildren():
        if child.tag == 'div':
            #print(child.xpath(f'/table/tbody/tr[1]/td/code/strong'))
            opdesc.append({'name': '', 'desc': ''})
            i = i + 1
            opdesc[i]['name'] = oplist[i]
        if child.tag == 'p' and child.text:

            if(opdesc[i]['desc']==''):
                opdesc[i]['desc'] = child.text_content().strip().replace('\n','')
            else:
                opdesc[i]['desc']+= child.text_content().strip().replace('\n', '')

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


def getdep(path,oplist):
    f = open(path, encoding='utf-8')
    xml = f.read()
    f.close()
    doc = fromstring(xml)
    div_element = doc.xpath('//*[@id="content"]')[0]
    i = 1
    for child in div_element.iterchildren():
        if child.tag == 'div':
            print('')
            print(oplist[i] + ' ', end='')
            i = i + 1
        if child.tag == 'p' and child.text:
            # des = des+child.text.replace('\n','')
            for grandchild in child.iterchildren():
                if grandchild.tag == 'a' and grandchild.text:
                    if grandchild.text in oplist:
                        print(grandchild.text + ' ', end='')

if __name__ == "__main__":
    #manpage = '/home/tixu/software/mysql-doc-online/5.6/innodb-parameters.html'
    #plist = get_parameter_list(manpage)
    #pdesc = get_parameter_desc(manpage, plist)
    #print len(pdesc)
    get_all_parameter_desc('./manuals/')
