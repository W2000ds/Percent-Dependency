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


if __name__ == "__main__":
    get_all_parameter_desc('./manual/')
