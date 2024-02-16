import csv
import subprocess
import numpy as np
import time
import re
password = 777777

def run_nginx_benchmark():
    # 运行 nginx 性能测试命令
    command = "ab -n 10000 -c 100 http://127.0.0.1:70/test.html"
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return result.stdout

def extract_data_from_output(output):
    lines = output.split('\n')

    # 正则表达式用于匹配关键性能指标
    requests_per_second_pattern = r"Requests per second:\s+(\d+\.\d+)"
    time_per_request_pattern = r"Time per request:\s+(\d+\.\d+)"

    # 提取指标
    requests_per_second = re.search(requests_per_second_pattern, output).group(1)

    time_per_request = re.search(time_per_request_pattern, output).group(1)

    return requests_per_second,time_per_request


def clear_nginx_conf(file_path):
    with open(file_path, "w") as file:
        file.truncate()

def startsys():
    subprocess.run(f"echo {password} | sudo -S /home/lhy/nginx-server/sbin/nginx",shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    time.sleep(2) # give nginx 2 sec to start

def stopsys():
    commandstop = f"echo {password} | sudo -S killall nginx"

    try:
        subprocess.run(commandstop, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        print(e)

def add_config_to_nginx_conf(file_path, configname ,configvalue):
    commandwrite2file = f"echo '{configname} {configvalue};' > {filepath}"

    stopsys()

    subprocess.run(commandwrite2file, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    startsys()

    return True

# 运行测试并捕获输出
# output = run_nginx_benchmark()
#
# # 从输出中提取数据
# time_taken, avg_TPR = extract_data_from_output(output)
#
# print("Time taken:", time_taken)
# print("Average TPR:", avg_TPR)
def read_csv_to_dict(filename):
    data = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # 将每行转换为字典（列标题作为键）
            data.append(row)
    return data

def is_outlier(points, thresh=2.0):
    """判断是否为异常值"""
    if len(points) == 1:
        return False
    median = np.median(points)
    diff = np.abs(points - median)
    mdev = np.median(diff)
    modified_z_score = 0.6745 * diff / mdev
    return modified_z_score > thresh

def calculate_change(current, standard):
    """计算变化率。"""
    return ((current - standard) / standard) * 100 if standard != 0 else 0

if __name__ == '__main__':
    filepath = "/home/lhy/GroundTruth/Nginx/nginx.conf"
    confdata = read_csv_to_dict("/home/lhy/GroundTruth/Nginx/test.csv")
    results = []
    RPS_stand = 68500
    TPR_stand = 1.48

    #stopnginx
    stopsys
    # clear conffile
    clear_nginx_conf(filepath)
    # start nginx
    startsys

    for conf in confdata:
        # clear conf file
        clear_nginx_conf(filepath)
        print(f"{conf['name']} {conf['valuename']} {conf['value']}")

        RPS_list = []
        TPR_list = []

        if (add_config_to_nginx_conf(filepath,conf['name'],conf['value']) == False):
            continue
        # run for 5 timees

        for i in range(1, 6):
            bench_output = run_nginx_benchmark()
            RPS,TPR = extract_data_from_output(bench_output)
            print(f"{i}th : Requests per second:{RPS}, Time per request: {TPR} ms")

            
            RPS_list.append(float(RPS))
            TPR_list.append(float(TPR))

        RPS_list = np.array(RPS_list)
        TPR_list = np.array(TPR_list)


        RPS_avg = np.mean(RPS_list) if len(RPS_list) else None
        TPR_avg = np.mean(TPR_list) if len(TPR_list) else None

        print(f"Average RPS: {RPS_avg}, Average TPR: {TPR_avg} ms")

        RPSchange = calculate_change(RPS_avg, RPS_stand)
        TPRchange = calculate_change(TPR_avg, TPR_stand)

        print(f"Average RPS change: {RPSchange}, Average TPR change: {TPRchange}")
        # add to result
        results.append([conf['name'],conf['valuename'],conf['value'],RPS_avg,TPR_avg,RPSchange,TPRchange])




    with open('nginxGTbool.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(results)

