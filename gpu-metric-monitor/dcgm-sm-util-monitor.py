import argparse
import subprocess
import re
import time

WRITE_TO_FILE = True
MILLI_SECONDS_LEVEL = True

def parse_output(output):
    for line in output.splitlines():
        match = re.match(r'GPU \d+\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)', line)
        if match:
            gpu_id = int(match.group(0).split()[1])
            sm_active = float(match.group(1))
            sm_occupancy = float(match.group(2))
            dram_access = float(match.group(3))
            power_watt = float(match.group(4))
            return gpu_id, sm_active, sm_occupancy, dram_access, power_watt
        else:
            return None, None, None, None, None

def main():
    parser = argparse.ArgumentParser(description='Monitor GPU SM Utilization.')
    parser.add_argument('-g', '--gpus', type=str, required=True, help='Comma-separated list of GPU IDs to monitor, e.g., 0,1,2')
    parser.add_argument('-d', '--delay', type=int, default=1000, help='Delay in milliseconds between samples (default: 1000)')
    args = parser.parse_args()

    gpus = args.gpus
    delay = args.delay

    command = f'dcgmi dmon -i {gpus} -e "1002,1003,1005,155" -d {delay}'
    print('Running command:', command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)

    gpu_list = [int(gpu) for gpu in gpus.split(',')]
    print('Monitoring GPU(s):', gpu_list)

    if WRITE_TO_FILE:
        with open('gpu_sm_metrics.csv', 'w') as f:
            f.write('timestamp,avg_sm_active,avg_sm_occupancy,avg_dram_access,power\n')

    try:
        gpu_data = {i: {'sm_active': 0, 'sm_occupancy': 0, 'dram_access': 0, 'power':0, 'count': 0} for i in gpu_list}

        while True:
            output = process.stdout.readline()
            if MILLI_SECONDS_LEVEL:
                # get timestamp in format of milliseconds since epoch
                timestamp = int(time.time() * 1000)
            else:
                # get timestamp in format of 'YYYY-MM-DD HH:MM:SS' in UTC
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            if output:
                gpu_id, sm_active, sm_occupancy, dram_access, power_watt = parse_output(output)
                if sm_active is not None and sm_occupancy is not None:
                    sm_active_percent = round(sm_active * 100, 3)
                    sm_occupancy_percent = round(sm_occupancy * 100, 3)
                    dram_access_percent = round(dram_access * 100, 3)
                    power_watt = round(power_watt, 3)
                    print(f'GPU:{gpu_id} - SM_ACTIVE: {sm_active_percent}%, SM_OCCUPANCY: {sm_occupancy_percent}%, DRAM_ACCESS: {dram_access_percent}%, Power: {power_watt}W')

                    gpu_data[gpu_id]['sm_active'] += sm_active_percent
                    gpu_data[gpu_id]['sm_occupancy'] += sm_occupancy_percent
                    gpu_data[gpu_id]['dram_access'] += dram_access_percent
                    gpu_data[gpu_id]['power'] += power_watt
                    gpu_data[gpu_id]['count'] += 1

                    if all(gpu_data[i]['count'] > 0 for i in gpu_list):
                        avg_sm_active = sum(gpu_data[i]['sm_active'] for i in gpu_list) / sum(gpu_data[i]['count'] for i in gpu_list)
                        avg_sm_occupancy = sum(gpu_data[i]['sm_occupancy'] for i in gpu_list) / sum(gpu_data[i]['count'] for i in gpu_list)
                        avg_dram_access = sum(gpu_data[i]['dram_access'] for i in gpu_list) / sum(gpu_data[i]['count'] for i in gpu_list)
                        total_power = sum(gpu_data[i]['power'] for i in gpu_list)
                        print(timestamp)
                        print(f'>> Average SM_ACTIVE: {avg_sm_active:.3f}%, Average SM_OCCUPANCY: {avg_sm_occupancy:.3f}%, Average PROF_DRAM_ACTIVE: {avg_dram_access:.3f}, Total Power: {total_power:.3f}\n')

                        # reset the data for the next round
                        gpu_data = {i: {'sm_active': 0, 'sm_occupancy': 0, 'dram_access': 0, 'power': 0, 'count': 0} for i in gpu_list}

                        # write to a local csv file if WRITE_TO_FILE is True (CSV file columns are timestamp, avg_sm_active, avg_sm_occupancy)
                        if WRITE_TO_FILE:
                            with open('gpu_sm_metrics.csv', 'a') as f:
                                f.write(f'{timestamp},{round(avg_sm_active, 3)},{round(avg_sm_occupancy, 3)},{round(avg_dram_access,3)},{round(total_power, 3)}\n')
            else:
                break
    except KeyboardInterrupt:
        process.terminate()

if __name__ == '__main__':
    main()