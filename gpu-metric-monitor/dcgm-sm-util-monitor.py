import argparse
import subprocess
import re
import time

WRITE_TO_FILE = False

def parse_output(output):
    for line in output.splitlines():
        match = re.match(r'GPU \d+\s+(\d+\.\d+)\s+(\d+\.\d+)', line)
        if match:
            gpu_id = int(match.group(0).split()[1])
            sm_active = float(match.group(1))
            sm_occupancy = float(match.group(2))
            return gpu_id, sm_active, sm_occupancy
        else:
            return None, None, None

def main():
    parser = argparse.ArgumentParser(description='Monitor GPU SM Utilization.')
    parser.add_argument('-g', '--gpus', type=str, required=True, help='Comma-separated list of GPU IDs to monitor, e.g., 0,1,2')
    parser.add_argument('-d', '--delay', type=int, default=1000, help='Delay in milliseconds between samples (default: 1000)')
    args = parser.parse_args()

    gpus = args.gpus
    delay = args.delay

    command = f'dcgmi dmon -i {gpus} -e "1002,1003" -d {delay}'
    print('Running command:', command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)

    gpu_list = [int(gpu) for gpu in gpus.split(',')]
    print('Monitoring GPU(s):', gpu_list)

    try:
        gpu_data = {i: {'sm_active': 0, 'sm_occupancy': 0, 'count': 0} for i in gpu_list}

        while True:
            output = process.stdout.readline()
            # get timestamp in format of 'YYYY-MM-DD HH:MM:SS' in UTC
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            if output:
                gpu_id, sm_active, sm_occupancy = parse_output(output)
                if sm_active is not None and sm_occupancy is not None:
                    sm_active_percent = round(sm_active * 100, 3)
                    sm_occupancy_percent = round(sm_occupancy * 100, 3)
                    print(f'GPU:{gpu_id} - SM_ACTIVE: {sm_active_percent}%, SM_OCCUPANCY: {sm_occupancy_percent}%')

                    gpu_data[gpu_id]['sm_active'] += sm_active_percent
                    gpu_data[gpu_id]['sm_occupancy'] += sm_occupancy_percent
                    gpu_data[gpu_id]['count'] += 1

                    if all(gpu_data[i]['count'] > 0 for i in gpu_list):
                        avg_sm_active = sum(gpu_data[i]['sm_active'] for i in gpu_list) / sum(gpu_data[i]['count'] for i in gpu_list)
                        avg_sm_occupancy = sum(gpu_data[i]['sm_occupancy'] for i in gpu_list) / sum(gpu_data[i]['count'] for i in gpu_list)
                        print(timestamp)
                        print(f'>> Average SM_ACTIVE: {avg_sm_active:.3f}%, Average SM_OCCUPANCY: {avg_sm_occupancy:.3f}%\n')

                        # reset the data for the next round
                        gpu_data = {i: {'sm_active': 0, 'sm_occupancy': 0, 'count': 0} for i in gpu_list}

                        # write to a local csv file if WRITE_TO_FILE is True (CSV file columns are timestamp, avg_sm_active, avg_sm_occupancy)
                        if WRITE_TO_FILE:
                            with open('gpu_sm_metrics.csv', 'a') as f:
                                f.write(f'{timestamp},{avg_sm_active},{avg_sm_occupancy}\n')
            else:
                break
    except KeyboardInterrupt:
        process.terminate()

if __name__ == '__main__':
    main()