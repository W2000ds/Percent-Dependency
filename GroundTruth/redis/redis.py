import csv
import subprocess
import numpy as np
import time
def run_redis_benchmark():
    # 运行 Redis 性能测试命令
    command = "redis-benchmark -t set,get -n 100000 -c 50"
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return result.stdout

def extract_data_from_output(output):
    lines = output.split('\n')
    time_taken = []
    avg_latency = []

    for i, line in enumerate(lines):
        if 'requests completed in' in line:
            # 提取完成请求的时间
            parts = line.split()
            time_taken.append(parts[4])

        if 'latency summary (msec)' in line:
            # 查找平均延迟
            for j in range(i + 1, len(lines)):
                if 'avg' in lines[j]:
                    avg_latency.append(lines[j+1].split()[0])
                    break

    return time_taken, avg_latency




def clear_redis_conf(file_path):
    with open(file_path, "w") as file:
        file.truncate()

def add_config_to_redis_conf(file_path, configname ,configvalue):
    command = f"echo '{configname} {configvalue}' > /home/lhy/sourececodeReading/redis-6.2.12/testconf/redis.conf"

    command1 = "redis-cli shutdown"

    with open("/dev/null", "w") as devnull:
        subprocess.run(command1, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        subprocess.Popen(["redis-server", "/home/lhy/sourececodeReading/redis-6.2.12/testconf/redis.conf"],stdout=devnull, stderr=devnull)
    time.sleep(2) # give redis 2 sec to start

    return True

# 运行测试并捕获输出
# output = run_redis_benchmark()
#
# # 从输出中提取数据
# time_taken, avg_latency = extract_data_from_output(output)
#
# print("Time taken:", time_taken)
# print("Average Latency:", avg_latency)
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
    filepath = "/home/lhy/sourececodeReading/redis-6.2.12/testconf/redis.conf"
    confdata = read_csv_to_dict("/home/lhy/GroundTruth/redis/testbool.csv")
    results = []
    tps_stand = 0.375789474
    latency_stand = 0.097052632
    # start redis
    with open("/dev/null", "w") as devnull:
        subprocess.Popen(["redis-server","/home/lhy/sourececodeReading/redis-6.2.12/testconf/redis.conf"],stdout=devnull, stderr=devnull)

    for conf in confdata:
        # clear conf file
        clear_redis_conf(filepath)
        print(f"{conf['name']} {conf['valuename']} {conf['value']}")
        try:
            tpssum = 0.0
            latencysum = 0.0

            tps_list = []
            latency_list = []

            if (add_config_to_redis_conf(filepath,conf['name'],conf['value']) == False):
                continue
            # run for 5 timees

            for i in range(1, 6):
                bench_output = run_redis_benchmark()
                tpss,latencys = extract_data_from_output(bench_output)
                tps = (float(tpss[0])+float(tpss[1]))/2
                latency = (float(latencys[0]) + float(latencys[1])) / 2
                print(f"{i}th TPS: {tps}, Average Latency: {latency} ms")

                tps_list.append(tps)
                latency_list.append(latency)

            tps_list = np.array(tps_list)
            latency_list = np.array(latency_list)


            tps_avg = np.mean(tps_list) if len(tps_list) else None
            latency_avg = np.mean(latency_list) if len(latency_list) else None

            print(f"Average TPS: {tps_avg}, Average Latency: {latency_avg} ms")

            tpschange = calculate_change(tps_avg, tps_stand)
            latencychange = calculate_change(latency_avg, latency_stand)

            print(
                f"Average TPS change: {tpschange}, Average Latency change: {latencychange}")
            # add to result
            results.append([conf['name'],conf['valuename'],conf['value'],tps_avg,latency_avg,tpschange,latencychange])


        except Exception as e:
            print(f"---error---: {e}")
            continue

    with open('redisGTbool.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(results)