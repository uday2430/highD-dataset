import os
import sys
import numpy as np
import pandas as pd

from data_management.read_csv_from_path import *
from track_data_processing.find_car_following import *
#frame rate is 25Hz

range = np.arange(60)
data_id = []
for number in range:
    data_id.append((str((number+1)) if (number+1) >= 10 else "0"+str(number+1)))

data_dir = "../data/"
results_dir = "../results/"

EGO_TYPE = "Car"
PRECEDING_TYPE = "Car"

for id in data_id:
    print(id)
    recording_meta_path = data_dir+id+"_recordingMeta.csv"
    track_meta_path = data_dir + id + "_tracksMeta.csv"
    track_path = data_dir + id + "_tracks.csv"

    recording_meta_data = read_meta_info(str(recording_meta_path))
    track_meta_data = read_static_info(str(track_meta_path))
    track_data = read_track_csv(str(track_path))

    #to extract car-following period and save it to a file
    car_following_data = find_car_following(track_meta_data, track_data, EGO_TYPE, PRECEDING_TYPE)
    pd.DataFrame(car_following_data).to_csv(results_dir+id+"_"+EGO_TYPE+"_follow_"+PRECEDING_TYPE+".csv", index=False)

    #numCar = recording_meta_data.get('numCars')
    #numTruck = recording_meta_data.get('numTrucks')
    #percentageTrucks = (numTruck/(recording_meta_data.get('numVehicles')))*100
    #print("Number of cars: "+str(numCar))
    #print("Number of trucks: "+str(numTruck))
    #print("Percentage of trucks: " + str(percentageTrucks))
    print('-------------------------------')
