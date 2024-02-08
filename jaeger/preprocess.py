###################################################
## Description: This script converts the raw Jaeger
## tracing data in JSON format to a list of traces
## withg only info for critical path analysis.
###################################################
## Author: {Haoran Qiu}
## Copyright: Copyright 2020, Project FIRM
## License: GNU GENERAL PUBLIC LICENSE
## Maintainer: Haoran Qiu
## Email: haoranq4[AT]illinois.edu
## Status: Testing, Non-production
###################################################

import json
import sys

# Input:
## raw tracing data => {"data", "errors", "limit", "offset", "total"}
##           "data" => [{"processes", "spans", "traceID", "warnings"}]
# Output:
## traces => [trace]; trace => [span];
##   span => {"spanID": {"operationName", "parentSpanID", "childSpanIDs", "startTime", "duration"}}
def preprocess(filename, from_file=True, jaeger_dict=None):
    # load raw tracing data
    json_dict = {}
    if from_file:
        print('Raw tracing data from file:', filename)
        with open(filename, 'r') as f:
            json_dict = json.load(f)
    else:
        print('Raw tracing data from dictionary...')
        json_dict = jaeger_dict

    if json_dict['errors'] != None:
        print('Unsuccessful processing of JSON file! Error:', json_dict['errors'])
        return

    data_dict = json_dict['data']
    print('Total # of raw traces:', len(data_dict))

    num_normal_traces = 0
    traces = []
    for entry in data_dict:
        # print('Warnings:', entry['warnings'])
        if entry['warnings']:
            continue

        spans = {}
        child_spans = []
        containsWarningMsg = False
        for item in entry['spans']:
            if item['warnings']:
                # print('Warnings:', item['warnings'])
                containsWarningMsg = True
                break
            span = {
                'operationName': item['operationName'],
                'startTime': item['startTime'],
                'duration': item['duration'],
                'childSpanIDs': [],
                'parentSpanID': None
            }
            if len(item['references']) > 0:
                span['parentSpanID'] = item['references'][0]['spanID']
                child_spans.append(item['spanID'])
            else:
                # root span
                spans['root'] = item['spanID']
            spans[item['spanID']] = span
        if containsWarningMsg:
            continue
        for child_span in child_spans:
            parent_spanID = spans[child_span]['parentSpanID']
            spans[parent_spanID]['childSpanIDs'].append(child_span)

        # no warning message found in the trace
        num_normal_traces += 1
        traces.append(spans)

    print('Total # of normal traces:', len(traces))
    return traces


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: python3 preprocess.py <tracing_data.json>')
        exit()
    traces = preprocess(sys.argv[1])
    for trace in traces:
        print('# of spans:', len(trace)-1) # -1 due to the root span is repeated
        for spanID in trace:
            if spanID == 'root':
                continue
            print(spanID, trace[spanID])
