import os
import sys
import numpy as np
import pandas as pd

from data_management.read_csv_from_path import *
from track_data_processing.find_car_following import *
from car_following_data_processing.extract_safety import *
#frame rate is 25Hz

range = np.arange(60)
data_id = []
for number in range:
    data_id.append((str((number+1)) if (number+1) >= 10 else "0"+str(number+1)))

data_dir = "../data/"
results_dir = "../results/"

EGO_TYPE = "Truck"
PRECEDING_TYPE = "Car"

totCar = 0
totTruck = 0

for dataset_id in data_id:
    print(dataset_id)
    recording_meta_path = data_dir+dataset_id+"_recordingMeta.csv"
    track_meta_path = data_dir + dataset_id + "_tracksMeta.csv"
    track_path = data_dir + dataset_id + "_tracks.csv"

    recording_meta_data = read_meta_info(str(recording_meta_path))
    track_meta_data = read_static_info(str(track_meta_path))
    track_data = read_track_csv(str(track_path))

    ### Extract car-following period and save it to a file
    #car_following_data = find_car_following(track_meta_data, track_data, EGO_TYPE, PRECEDING_TYPE)
    #pd.DataFrame(car_following_data).to_csv(results_dir+id+"_"+EGO_TYPE+"_follow_"+PRECEDING_TYPE+".csv", index=False)

    ### Extract safety information (dhw, thw, ttc)
    #safety_stats = extract_safety(dataset_id, track_meta_data, track_data, EGO_TYPE, PRECEDING_TYPE)
    #pd.DataFrame(safety_stats).to_csv(results_dir + dataset_id + "_" + EGO_TYPE + "_follow_" + PRECEDING_TYPE + "_safety_stats.csv",
    #                                       index=False)

    numCar = recording_meta_data.get('numCars')
    numTruck = recording_meta_data.get('numTrucks')
    percentageTrucks = (numTruck/(recording_meta_data.get('numVehicles')))*100
    print("Number of cars: "+str(numCar))
    print("Number of trucks: "+str(numTruck))
    print("Percentage of trucks: " + str(percentageTrucks))
    print('-------------------------------')
    totCar = totCar + numCar
    totTruck = totTruck + numTruck

print("total number of cars is ",totCar)
print("total number of trucks is ", totTruck)