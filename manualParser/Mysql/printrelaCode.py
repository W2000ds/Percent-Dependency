import os
import re
import subprocess

filepaths = []
vars = []
def getvarlocation(file,var):
    pattern = r"(\d+):"
    var_info =[]
    cmd = f'grep -nR \'{var}\' {file}'
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
    except subprocess.CalledProcessError as e:
        output = e.output.decode('utf-8')
    matches = re.findall(pattern, output)
    # 将提取的信息保存到数据结构中
    for match in matches:
        varline = int(match)
        var_info.append({'varname': var, 'varline': varline, 'file': file})
    return var_info

def readvar(varpath):
    with open(varpath, 'r') as f:
        for line in f:
            var = line.strip()
            vars.append(var)
def readfile(foldname):
    filepaths.clear()
    # 指定文件夹路径
    # 遍历文件夹
    for root, dirs, files in os.walk(foldname):
        # 遍历所有文件
        for file in files:
            # 获取文件绝对路径
            file_path = os.path.join(root, file)
            # 检查文件是否以.c结尾
            if file_path.endswith('.cc'):
                # 输出.c文件的路径
                filepaths.append(file_path)
def PrintRelativeLine(varinfos):
    try:
        for varinfo in varinfos:
            with open(varinfo['file'], 'r') as cpp_file:
                lines = cpp_file.readlines()
                print("["+varinfo['varname']+"]")
                for line_number in range(varinfo['varline'] - 5, varinfo['varline'] + 6):
                    if 1 <= line_number <= len(lines):
                        print(f"{lines[line_number - 1].strip()}")
    except FileNotFoundError:
        print(f"File '{varinfo['file']}' not found.")

if __name__ == '__main__':
    readvar('./mysqlvar')#文件中包含要搜索的变量名
    readfile('/home/lhy/sourececodeReading/mysql-8.0.33')#源码文件夹
    for var in vars:
        for file in filepaths:
            varinfos = getvarlocation(file,var)
            if varinfos :
                PrintRelativeLine(varinfos)