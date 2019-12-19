import pandas as pd
import numpy as np
from statistics import mean, median

results_dir = "../results/"

def extract_safety(dataset_id, meta_data, data, my_type, preceding_type):
    """

    :param dataset_id: id of the dataset
    :param meta_data: track meta information
    :param data: track data
    :param my_type: my vehicle type (either 'Car' or 'Truck')
    :param preceding_type: the preceding vehicle's type (either 'Car' or 'Truck')

    :return: a list of dictionary with
        id: identification of the ego vehicle
        my_type: my vehicle type (either 'Car' or 'Truck')
        preceding_type: the preceding vehicle's type (either 'Car' or 'Truck')
        dhw: the distance headway
        thw: the time headway
        ttc: the time-to-collision
    """

    safety_data = []
    filename = str(dataset_id)+"_"+str(my_type)+"_follow_"+str(preceding_type)+".csv"
    following_list = pd.read_csv(results_dir+filename)
    following_df = following_list.set_index('id')
    for ego_id in following_list['id']:
        following_start = following_df.loc[ego_id, 'following_start']
        following_duration = following_df.loc[ego_id, 'following_duration']
        following_end = following_start + following_duration
        dhw = data[ego_id].get('dhw')[following_start:following_end]
        thw = data[ego_id].get('thw')[following_start:following_end]
        ttc = data[ego_id].get('ttc')[following_start:following_end]
        ttc_non_zero = np.array(ttc)
        ttc_non_zero = ttc_non_zero[ttc_non_zero>=0]

        max_dhw, min_dhw, mean_dhw, med_dhw = get_max_min_mean_median(dhw)
        max_thw, min_thw, mean_thw, med_thw = get_max_min_mean_median(thw)
        if len(ttc_non_zero) == 0:
            #the list is empty
            max_ttc, min_ttc, mean_ttc, med_ttc = 0, 0, 0, 0
        else:
            max_ttc, min_ttc, mean_ttc, med_ttc = get_max_min_mean_median(ttc_non_zero)

        safety_data.append({"id": ego_id, "my_type": my_type, "preceding_type": preceding_type,
                            "max_dhw": max_dhw, "min_dhw": min_dhw, "mean_dhw": mean_dhw, "median_dhw": med_dhw,
                            "max_thw": max_thw, "min_thw": min_thw, "mean_thw": mean_thw, "median_thw": med_thw,
                            "max_ttc": max_ttc, "min_ttc": min_ttc, "mean_ttc": mean_ttc, "median_ttc": med_ttc
                            })
    return safety_data

def get_max_min_mean_median(data):

    max_val = max(data)
    min_val = min(data)
    mean_val = mean(data)
    median_val = median(data)

    return max_val, min_val, mean_val, median_val
