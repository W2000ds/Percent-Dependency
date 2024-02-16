import re

def extract_content(line):
    # 正则表达式匹配第一个引号内的内容和 SESSION_VAR()/GLOBAL_VAR() 内的内容
    quote_pattern = r'\"([^\"]*)\"'
    session_var_pattern = r'SESSION_VAR\(([^)]*)\)'
    global_var_pattern = r'GLOBAL_VAR\(([^)]*)\)'
    sessiononly_pattern = r'SESSION_ONLY\(([^)]*)\)'

    # 寻找匹配
    quote_match = re.search(quote_pattern, line)
    session_var_match = re.search(session_var_pattern, line)
    global_var_match = re.search(global_var_pattern, line)
    session_only_match = re.search(sessiononly_pattern,line)

    # 提取匹配结果
    results = []
    if quote_match:
        results.append(quote_match.group(1))
    if session_var_match:
        results.append(session_var_match.group(1))
    if global_var_match:
        results.append(global_var_match.group(1))
    if session_only_match:
        results.append(session_only_match.group(1))

    return results

def process_lines(line):
    extracted_content = extract_content(line)
    if len(extracted_content)>1 :
        print(f"{extracted_content}")


def read_and_combine_functions(filename):
    functions = []
    current_function = ""
    inside_function = False

    with open(filename, 'r') as file:
        for line in file:
            # 检测函数定义的开始
            if "static Sys_var_" in line:
                inside_function = True
                current_function = line.strip()  # 开始新的函数
            elif inside_function:
                # 添加到当前函数
                current_function += " " + line.strip()
                # 检测函数定义的结束（例如，以分号或特定括号结束）
                if line.strip().endswith(');'):
                    inside_function = False
                    functions.append(current_function)  # 添加完整的函数到列表

    return functions

# 使用函数
functions = read_and_combine_functions('sys_var.txt')
# 接下来你可以对这些函数进行处理

for function in functions:
    process_lines(function)


