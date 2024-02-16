import configparser
import subprocess
import re
import subprocess

import numpy as np

def modify_mysql_config(config_file, section, parameter, value, sys_password):
    try:
        # 创建RawConfigParser对象
        config = configparser.RawConfigParser()

        # 赋予修改权限
        chmod_777(config_file, sys_password)

        # 读取MySQL配置文件
        config.read(config_file)

        # # 读取原本的配置值
        # original_value = config.get(section, parameter)

        # 修改参数值
        config.set(section, parameter, value)

        # 保存修改后的配置文件
        with open(config_file, 'w') as f:
            config.write(f)

        print(f"成功将参数 {parameter} 修改为 {value}")

        # 回收修改权限
        chmod_644(config_file, sys_password)

        # 重启服务
        restart_mysql_service(sys_password)
        return True
    except Exception as error:
        print(f"修改失败：{error}")
        return False


def restart_mysql_service(sys_password):
    # 使用subprocess模块执行系统命令来重启MySQL服务
    command = f"echo {sys_password} | sudo -S systemctl restart mysql.service"
    # subprocess.run(['service', 'mysql', 'restart'])
    subprocess.run(command, shell=True, check=True, executable="/bin/bash")


def chmod_777(file_path, sudo_password):
    # 构建chmod命令
    command = f"echo {sudo_password} | c"

    # 执行命令
    subprocess.run(command, shell=True, check=True, executable="/bin/bash")


def chmod_644(file_path, sudo_password):
    # 构建chmod命令
    command = f"echo {sudo_password} | sudo -S chmod 644 {file_path}"

    # 执行命令
    subprocess.run(command, shell=True, check=True, executable="/bin/bash")



def run_sysbench(mysql_host, mysql_port, mysql_user, mysql_password, mysql_db, threads=16, time=20, report_interval=1, tables=4, table_size=100000):
    base_command = f"echo 777777 | sudo -S sysbench --threads={threads} --time={time} --report-interval={report_interval} --mysql-host={mysql_host} --mysql-port={mysql_port} --mysql-user={mysql_user} --mysql-password={mysql_password} --mysql-db={mysql_db} --tables={tables} --table-size={table_size}"

    commands = {
        "cd": f"cd /usr/share/sysbench",
        "prepare": f"{base_command} oltp_common.lua prepare",
        "run": f"{base_command} oltp_read_write run",
        "cleanup": f"{base_command} oltp_common.lua cleanup"
    }

    for stage, command in commands.items():
        print(f"开始执行 Sysbench {stage}...")
        if stage == "run":
            try:
                result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                return result.stdout
            except subprocess.CalledProcessError as e:
                print(f"errorlog：{e.output}")



def extract_metrics(sysbench_output):
    # 定义正则表达式模式
    tps_pattern = r"transactions:\s*\d+\s*\((\d+\.\d+) per sec.\)"
    qps_pattern = r"queries:\s*\d+\s*\((\d+\.\d+) per sec.\)"
    avg_latency_pattern = r"avg:\s+(\d+\.\d+)"

    # 提取 TPS
    tps_matches = re.search(tps_pattern, sysbench_output)
    tps = tps_matches.group(1) if tps_matches else "未找到"

    # 提取 QPS
    qps_matches = re.search(qps_pattern, sysbench_output)
    qps = qps_matches.group(1) if qps_matches else "未找到"

    # 提取平均延迟
    avg_latency_matches = re.search(avg_latency_pattern, sysbench_output)
    avg_latency = avg_latency_matches.group(1) if avg_latency_matches else "未找到"

    return tps, qps, avg_latency


import csv

def read_csv_to_dict(filename):
    data = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # 将每行转换为字典（列标题作为键）
            data.append(row)
    return data

def clearconf(config_file):
    command = f"echo 777777 | sudo -S sh -c 'echo '[mysqld]' > {config_file}'"
    chmod_777(config_file, sys_password)
    subprocess.run(command, shell=True, check=True, executable="/bin/bash")
    chmod_644(config_file, sys_password)


def calculate_change(current, standard):
    """计算变化率。"""
    return ((current - standard) / standard) * 100 if standard != 0 else 0


def is_outlier(points, thresh=2.0):
    """判断是否为异常值"""
    if len(points) == 1:
        return False
    median = np.median(points)
    diff = np.abs(points - median)
    mdev = np.median(diff)
    modified_z_score = 0.6745 * diff / mdev
    return modified_z_score > thresh


if __name__ == '__main__':

        config_file = '/etc/mysql/conf.d/mysql.cnf'
        section = 'mysqld'
        sys_password = "777777"
        confdata = read_csv_to_dict("/home/lhy/GroundTruth/test.csv")
        tps_stand = 616.22
        qps_stand = 12324.39
        latency_stand = 26
        results = []

        for conf in confdata:
            #clear conf file
            clearconf(config_file)

            try:
                tpssum = 0.0
                qpssum = 0.0
                latencysum = 0.0

                tps_list = []
                qps_list = []
                latency_list = []

                if(modify_mysql_config(config_file, section, conf['optionname'], conf['value'], sys_password)==False):
                    continue
                # run for 5 timees
                for i in range(1, 6):
                    sysbench_output = run_sysbench(
                        mysql_host="localhost",
                        mysql_port=3306,
                        mysql_user="root",
                        mysql_password="123456",
                        mysql_db="sbtest"
                    )
                    tps, qps, latency = extract_metrics(sysbench_output)
                    tps = float(tps)
                    qps = float(qps)
                    latency = float(latency)
                    tps_list.append(tps)
                    qps_list.append(qps)
                    latency_list.append(latency)
                    print(f"{i}th TPS: {tps}, QPS: {qps}, avg latency: {latency} ms")

                # calculate avg
                tps_list = np.array(tps_list)
                qps_list = np.array(qps_list)
                latency_list = np.array(latency_list)

                tps_list = tps_list[~is_outlier(tps_list)]
                qps_list = qps_list[~is_outlier(qps_list)]
                latency_list = latency_list[~is_outlier(latency_list)]


                tps_avg = np.mean(tps_list) if len(tps_list) else None
                qps_avg = np.mean(qps_list) if len(qps_list) else None
                latency_avg = np.mean(latency_list) if len(latency_list) else None

                print(f"Average TPS: {tps_avg}, Average QPS: {qps_avg}, Average Latency: {latency_avg} ms")

                tpschange = calculate_change(tps_avg, tps_stand)
                qpschange = calculate_change(qps_avg, qps_stand)
                avg_latencychange = calculate_change(latency_avg, latency_stand)

                print(f"Average TPS change: {tpschange}, Average QPS change : {qpschange}, Average Latency change: {avg_latencychange} ms")
                # add to result
                results.append([conf['optionname'], conf['valuename'], conf['value'], tps_avg,qps_avg,latency_avg,tpschange, qpschange, avg_latencychange])


            except Exception as e:
                print(f"---error---: {e}")
                continue

        #write to file
        with open('mysqlGT2.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(results)



