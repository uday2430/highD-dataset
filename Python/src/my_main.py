import os
import sys
import numpy as np
import argparse

from data_management.read_csv_from_path import *

#frame rate is 25Hz

range = np.arange(60)
data_id = []
for number in range:
    data_id.append((str((number+1)) if (number+1) >= 10 else "0"+str(number+1)))

data_dir = "../data/"
parser = argparse.ArgumentParser(description="ParameterOptimizer")

for id in data_id:
    print(id)
    recording_meta_path = data_dir+id+"_recordingMeta.csv"
    track_meta_path = data_dir + id + "_tracksMeta.csv"
    track_path = data_dir + id + "_tracks.csv"

    recording_meta_data = read_meta_info(str(recording_meta_path))
    track_meta_data = read_static_info(str(track_meta_path))
    #track_data = read_track_csv(str(track_path))

    numCar = recording_meta_data.get('numCars')
    numTruck = recording_meta_data.get('numTrucks')
    percentageTrucks = (numTruck/(recording_meta_data.get('numVehicles')))*100
    print("Number of cars: "+str(numCar))
    print("Number of trucks: "+str(numTruck))
    print("Percentage of trucks: " + str(percentageTrucks))
    print('-------------------------------')
