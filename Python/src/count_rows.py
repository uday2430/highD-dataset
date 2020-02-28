#just a script to count rows of a file

import os
import csv

target_dir = "../results/"
files = os.listdir(target_dir)
print(files)
tot_row = 0

for f in files:
    if "Truck_follow_Car" in f and "safety" not in f:
        with open(target_dir+f) as cf:
            reader = csv.reader(cf, delimiter=",")
            data = list(reader)
            row_count = len(data)
            tot_row = tot_row + row_count
print(tot_row)