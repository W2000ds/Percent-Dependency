from bs4 import BeautifulSoup
from lxml import etree
from lxml.html import fromstring
# from StringIO import StringIO
import csv
import os
import re
# HTML content provided by the user

from bs4 import BeautifulSoup

# Define the path to the target file
file_path = "./manuals/Module ngx_http_core_module.html"

# Open and read the content of the file
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Create a BeautifulSoup object to parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Find all <div class="directive"> elements
directives = soup.find_all('div', class_='directive')

# Initialize a list to hold the extracted contents
extracted_contents = []

# Iterate through each directive and extract the first <tr> content
for directive in directives:
    first_tr_content = directive.table.tr
    th_text = first_tr_content.th.text.strip()  # Extract text from <th>
    td_text = first_tr_content.td.text.strip()  # Extract text from <td>
    combined_text = f"{th_text}: {td_text}".replace("\n",'')
    extracted_contents.append(combined_text)

# Display the extracted contents
for content in extracted_contents:
    print(content)
