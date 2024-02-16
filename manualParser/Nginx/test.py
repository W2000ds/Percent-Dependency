from lxml import html

# 输入HTML段落
html_text = """
<p>
On Linux,
<a href="#directio">directio</a>
can only be used for reading blocks that are aligned on 512-byte
boundaries (or 4K for XFS).
File’s unaligned end is read in blocking mode.
The same holds true for byte range requests and for FLV requests
not from the beginning of a file: reading of unaligned data at the
beginning and end of a file will be blocking.
</p>
"""

# 解析HTML文本
parsed_html = html.fromstring(html_text)

# 提取<p>标签中的文本信息
p_text = parsed_html.xpath('//*[@id="content"]/p[2]')
//*[@id="content"]/p[262]
# 打印提取的文本
print(''.join(p_text).replace('\n',''))