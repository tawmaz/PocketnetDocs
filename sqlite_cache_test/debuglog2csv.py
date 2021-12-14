import sys
import json
import csv

STATISTIC_START = "Statistic for last 60s:"
JSON_START = "{\n"
JSON_END = "}\n"
def parse_log(filename):
    # Use a breakpoint in the code line below to debug your script.
    f = open(filename, "r")  # Press ⌘F8 to toggle the breakpoint.
    samples = []
    while s := f.readline():
        if STATISTIC_START in s:
            timestamp = s.split()[0]
            # Read entire JSON blob
            json_string = ""
            s = f.readline()
            if (s == JSON_START):
                json_string += s
                while (s != JSON_END):
                    s = f.readline()
                    json_string += s
            if json_string:
                sample = json.loads(json_string)
                sample['time'] = timestamp
                print(sample)
                samples.append(sample.copy())
    csvname = filename.split('.')[0] + ".csv"
    fields = ["time", "Height", "CacheUsed", "CacheHit", "CacheMiss", "CacheSpill", "MemoryUsed", "PeersALL"]
    with open(csvname, 'w') as f:
        w = csv.DictWriter(f, fields)
        w.writeheader()
        for sample in samples:
            row = {"time": sample["time"],
                   "Height": sample["General"]["Height"],
                   "PeersALL": sample["General"]["PeersALL"],
                   "CacheUsed": sample["SQL"]["CacheUsed"],
                   "CacheHit": sample["SQL"]["CacheHit"],
                   "CacheMiss": sample["SQL"]["CacheMiss"],
                   "CacheSpill": sample["SQL"]["CacheSpill"],
                   "MemoryUsed": sample["SQL"]["MemoryUsed"]}
            w.writerow(row)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Parse stats data from PocketNet debug.log into a csv file for performance analysis.\n")
        print("Usage: debuglog2csv.py [debug.log filename]\n")
    else:
        parse_log(sys.argv[1])
