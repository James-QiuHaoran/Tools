import json
import time

import nvidia_smi

WRITE_TO_FILE = False
PER_GPU_METRICS = False

while True:
    # get timestamp in format of 'YYYY-MM-DD HH:MM:SS' in UTC
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    gpus = nvidia_smi.get_gpus()
    total_power = 0
    gpu_util_list = []
    mem_util_list = []
    for gpu in gpus:
        info = json.loads(gpu.to_json())
        gpu_util = round(info['gpu_util'], 3)
        mem_util = round(info['mem_util'], 3)
        power_watts = round(info['power'], 3)
        freq_mhz = int(info['freq'])
        max_freq_mhz = int(info['max_freq'])

        if PER_GPU_METRICS:
            print('ID:', info['id'], info['uuid'])
            print('GPU Util:', str(gpu_util) + '%', 'Mem Util:', str(mem_util) + '% (' + str(info['mem_used']), 'MB in use)')
            print('Power:', power_watts, 'Watts')
            print('Frequency:', freq_mhz, 'MHz (max =', max_freq_mhz, 'MHz)')

        total_power += power_watts
        gpu_util_list.append(gpu_util)
        mem_util_list.append(mem_util)

    print(timestamp)
    total_power = round(total_power, 3)
    avg_gpu_util = round(sum(gpu_util_list) / len(gpu_util_list), 3)
    avg_mem_util = round(sum(mem_util_list) / len(mem_util_list), 3)
    print('>> Total Power:', total_power, 'Watts')
    print('>> Average GPU Util:', avg_gpu_util, '%')
    print('>> Average Mem Util:', avg_mem_util, '%')
    print()

    # write to a local csv file if WRITE_TO_FILE is True (CSV file columns are timestamp, total_power, avg_gpu_util, avg_mem_util)
    if WRITE_TO_FILE:
        with open('gpu_metrics.csv', 'a') as f:
            f.write(f'{timestamp},{total_power},{avg_gpu_util},{avg_mem_util}\n')

    time.sleep(1)