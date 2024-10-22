import sys
from nsys_recipe.data_service import DataService
import matplotlib.pyplot as plt


# To run this script, be sure to add the Nsight Systems package directory to your PYTHONPATH, similar to this: 
# export PYTHONPATH=/opt/nvidia/nsight-systems/2023.4.1/target-linux-x64/python/packages

"""
Example usage:
sudo nsys profile --gpu-metrics-devices=0 /home/azrsadmin/.conda/envs/lmm/bin/python test-stable-diffusion.py
nsys stats ./report1.nsys-rep  # this gives you some profile summary as well
python nsys-reader.py report1.nsys-rep
"""

def compute_utilization(filename, freq=10000):
    service=DataService(filename)
    table_column_dict = {
        "GPU_METRICS": ["typeId", "metricId", "value"],
        "TARGET_INFO_GPU_METRICS": ["metricName", "metricId"],
        "META_DATA_CAPTURE": ["name", "value"]
    }
    hints={"format":"sqlite"}
    df_dict = service.read_tables(table_column_dict, hints=hints)
    df = df_dict.get("GPU_METRICS", None)
    if df is None:
        print(f"{filename} does not contain GPU metric data.")
        return
    tgtinfo_df = df_dict.get("TARGET_INFO_GPU_METRICS", None)
    if tgtinfo_df is None:
        print(f"{filename} does not contain TARGET_INFO_GPU_METRICS table.")
        return
    metadata_df = df_dict.get("META_DATA_CAPTURE", None)
    if metadata_df is not None:
        if "GPU_METRICS_OPTIONS:SAMPLING_FREQUENCY" in metadata_df['name'].values:
            report_freq = metadata_df.loc[ metadata_df['name']=='GPU_METRICS_OPTIONS:SAMPLING_FREQUENCY']['value'].iat[0]
            if isinstance(report_freq, (int,float)):
                freq = report_freq
                print("Setting GPU Metric sample frequency to value in report file. new frequency=",freq)

    possible_smactive=['SMs Active', 'SM Active', 'SM Active [Throughput %]', 'SMs Active [Throughput %]']
    smactive_name_mask = tgtinfo_df['metricName'].isin(possible_smactive)
    smactive_row = tgtinfo_df[smactive_name_mask]
    smactive_name = smactive_row['metricName'].iat[0]
    smactive_id = tgtinfo_df.loc[tgtinfo_df['metricName']==smactive_name,'metricId'].iat[0]
    smactive_df = df.loc[ df['metricId'] == smactive_id ]

    usage = smactive_df['value'].sum()
    print('usage', usage)
    print('smactive_df', smactive_df)
    print('smactive_df[\'value\']', smactive_df['value'])
    # plot the smactive_df['value'] to see the utilization over time
    plt.scatter(range(len(smactive_df['value'])), smactive_df['value'], s=1)
    plt.savefig('smactive_df.png')

    count = len(smactive_df['value'])
    count_nonzero = len(smactive_df.loc[smactive_df['value']!=0])
    avg_gross_util = usage/count
    avg_net_util = usage/count_nonzero
    effective_util = usage/freq/100

    print(f"Avg gross GPU utilization:\t%lf %%" % avg_gross_util)
    print(f"Avg net GPU utilization:\t%lf %%" % avg_net_util)
    print(f"Effective GPU utilization time:\t%lf s" % effective_util)
    return metadata_df


if __name__ == '__main__': 
    if len(sys.argv)==2:
        compute_utilization(sys.argv[1])
    elif len(sys.argv)==3:
        compute_utilization(sys.argv[1], freq=float(sys.argv[2]))
