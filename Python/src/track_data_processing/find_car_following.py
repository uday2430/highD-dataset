import numpy as np

def find_car_following(meta_data, data, my_type, preceding_type):
    """
    Find out car-following situations from specific vehicle types

    :param meta_data: track meta information from highD dataset
    :param data: track data from highD dataset
    :param my_type: the ego vehicle's type
    :param preceding_type: the preceding vehicle's type

    :return: a list of dictionary with
        id: identification of the vehicle
        following_start: the index of array when the following starts
        following_duration: the following duration
    """
    following_data = []
    for id in range(0,len(data)):
        following_duration = np.count_nonzero(data[id].get('precedingId'))
        if following_duration != 0:
            following_start = np.where(data[id].get('precedingId') > 0)[0][0]
            if(
                (get_vehicle_class(meta_data, data[id].get('precedingId')[following_start]) == preceding_type)
                and (get_vehicle_class(meta_data, id+1) == my_type)
            ):
                #record the behaviour
                following_data.append({"id": id, "following_start": following_start, "following_duration": following_duration})
    return following_data

def get_vehicle_class(meta_data, id):
    """

    :param meta_data: track meta information from highD dataset
    :param id: vehicle's id in the dataset
    :return: vehicle type (string: 'Car' or 'Truck')
    """
    return meta_data[id].get('class')
