import numpy as np
import pandas as pd
from data_management.read_csv_from_path import *
from track_data_processing.find_car_following import *
from track_data_processing.find_lane_changes import *
from track_data_processing.find_initial_stats import *
from car_following_data_processing.extract_safety import *

# ----- Configuration for the script ------
save_to_csv = False     # Would you like to save the results to .csv file? Yes = True; No = False
# WARNING: choosing to save will create one result file per dataset, so it will create a lot of files

# There are 60 datasets: from 1 to 60
begin_id = 1
last_id = 60
data_id = []
for number in np.arange(begin_id, last_id):
    data_id.append((str((number)) if (number) >= 10 else "0"+str(number)))

data_dir = "../data/"           # Directory where the HighD dataset is stored
results_dir = "../results/"     # Directory where the results should be saved

# ----- Car-following configuration -----
EGO_TYPE = "Car"        # The follower's vehicle type (can be either "Car" or "Truck")
PRECEDING_TYPE = "Car"  # The leader's vehicle type (can be either "Car" or "Truck")

nCar = 0
nTruck = 0

for dataset_id in data_id:
    print("Now reading the dataset number..." + dataset_id)

    # Define which file to read
    recording_meta_path = data_dir+dataset_id+"_recordingMeta.csv"
    track_meta_path = data_dir + dataset_id + "_tracksMeta.csv"
    track_path = data_dir + dataset_id + "_tracks.csv"

    # Read the data into these variable
    # Look at the format defined in https://www.highd-dataset.com/format
    recording_meta_data = read_meta_info(str(recording_meta_path))
    track_meta_data = read_static_info(str(track_meta_path))
    track_data = read_track_csv(str(track_path))

    # ----- Get number of cars and trucks from the meta data -----
    numCar = recording_meta_data.get('numCars')
    numTruck = recording_meta_data.get('numTrucks')
    percentageTrucks = (numTruck / (recording_meta_data.get('numVehicles'))) * 100
    print("There are %d cars" % numCar)
    print("There are %d trucks" % numTruck)

    # ----- Extract car-following period ------
    car_following_data = find_car_following(track_meta_data, track_data, EGO_TYPE, PRECEDING_TYPE)

    # ----- Extracting lane-changing statistics -----
    LC_stats = find_lane_changes(track_meta_data, track_data)
    print("There are %d lane changes in total for this dataset" % LC_stats.get('sumLC'))
    print("%d cars changed lanes" % LC_stats.get('carLC'))
    print("%d trucks changed lanes" % LC_stats.get('truckLC'))

    # ----- Print location of this dataset (there are 6 locations in total) -----
    print("The location for this dataset is ",recording_meta_data.get('locationId'))

    # ----- Find initial states for all vehicles (position, speed, lane, class, length) -----
    init_states = find_initial_state(track_meta_data, track_data)

    if save_to_csv:
        pd.DataFrame(car_following_data).to_csv(
            results_dir + dataset_id + "_" + EGO_TYPE + "_follow_" + PRECEDING_TYPE + "_stats.csv",
            index=False)
        pd.DataFrame(safety_stats).to_csv(
            results_dir + dataset_id + "_" + EGO_TYPE + "_follow_" + PRECEDING_TYPE + "_safety_stats.csv",
            index=False)
        pd.DataFrame(init_states).to_csv(
            results_dir + dataset_id + "_initial_states.csv",
            index=False)

    print("---------------------------")