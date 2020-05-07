import os
import sys
import numpy as np
import pandas as pd

from data_management.read_csv_from_path import *
from track_data_processing.find_car_following import *
from car_following_data_processing.extract_safety import *

data_id = []

#Go through all the data from 1 to 60
for number in np.arange(60):
    data_id.append((str((number + 1)) if (number + 1) >= 10 else "0" + str(number + 1)))

#define the directory where you have the dataset
data_dir = "../data/"

#define the directory to save your output file(s), if any
results_dir = "../results/"

#defind the vehicle type for data extraction example
EGO_TYPE = "Truck"
PRECEDING_TYPE = "Car"


for dataset_id in data_id:
    print("Now reading the dataset number ", dataset_id)

    #define which file to read
    recording_meta_path = data_dir + dataset_id + "_recordingMeta.csv"
    track_meta_path = data_dir + dataset_id + "_tracksMeta.csv"
    track_path = data_dir + dataset_id + "_tracks.csv"

    #read the data into these variable
    recording_meta_data = read_meta_info(str(recording_meta_path))
    track_meta_data = read_static_info(str(track_meta_path))
    track_data = read_track_csv(str(track_path))

    #Look at the format defined in https://www.highd-dataset.com/format

    #For example, if you would like to get number of cars and trucks from the meta data
    numCar = recording_meta_data.get('numCars')
    numTruck = recording_meta_data.get('numTrucks')
    percentageTrucks = (numTruck / (recording_meta_data.get('numVehicles'))) * 100

    #Example of extracting car-following period
    car_following_data = find_car_following(track_meta_data, track_data, EGO_TYPE, PRECEDING_TYPE)

    #Extract safety information (dhw, thw, ttc)
    safety_stats = extract_safety(dataset_id, track_meta_data, track_data, EGO_TYPE, PRECEDING_TYPE)


    #If you want to save the data to a csv file, you can uncomment the line below
    ### WARNING: it will create a file per dataset, so it will create a lot of files ###
    #pd.DataFrame(safety_stats).to_csv(
    #    results_dir + dataset_id + "_" + EGO_TYPE + "_follow_" + PRECEDING_TYPE + "_safety_stats.csv",
    #    index=False)