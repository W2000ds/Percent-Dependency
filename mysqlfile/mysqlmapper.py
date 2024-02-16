import pandas as pd
params1 = []
params2 = []

def split_params(params):
    """将参数名按照'_'分割成单词列表"""
    return [param.split('_') for param in params]

def compare_params(params1, params2):
    """比较两个参数列表，记录相同单词的数量"""
    matches = []
    for p1 in params1:
        for p2 in params2:
            common_words = set(p1) & set(p2)
            if common_words:
                matches.append((' '.join(p1), ' '.join(p2), len(common_words)))
    return matches

def sort_and_format(matches):
    """根据匹配数量排序并格式化输出"""
    sorted_matches = sorted(matches, key=lambda x: x[2], reverse=True)
    for match in sorted_matches:
        print(f"{match[0]}-{match[1]}-{match[2]}")

def readfile(filepath):
      # 将此路径替换为您的文件路径
    with open(filepath,'r')as f:
        lines = f.readlines()
        for line in lines:
            params1.append(line.split(' ')[0])
            params2.append(line.split(' ')[1].replace('\n',''))#删除换行符



if __name__ == '__main__':
    # 执行比较
    readfile('/home/lhy/manualParser/Mysql/mysqlmapper.txt')
    params1_split = split_params(params1)
    params2_split = split_params(params2)
    matches = compare_params(params1_split, params2_split)

    # 输出结果
    sort_and_format(matches)
