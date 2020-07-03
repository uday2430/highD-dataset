import statistics
import numpy as np

def find_car_following(meta_data, data, my_type, preceding_type):
    """
    Find out car-following situations from specific vehicle types

    :param meta_data: track meta information from highD dataset
    :param data: track data from highD dataset
    :param my_type: the ego vehicle's type
    :param preceding_type: the preceding vehicle's type

    :return: a list of dictionary with
        ego_id: identification of the ego vehicle
        pred_id: identification of the preceding vehicle
        following_start: the frame when the following starts
        following_duration: the following duration
        following_end: the frame when the following ends
        dhw: array of DHW while following
        thw: array of THW while following
        ttc: array of TTC while following
    """
    following_data = []
    for i in range(0, len(data)):
        following_started = False
        following_dhw = []
        following_thw = []
        following_ttc = []
        ego_speed = []
        pred_speed = []
        frame_following_start = 0
        following_duration = 0
        preceding_id = 0
        ego_id = data[i].get('id')
        for frame in range(0, len(data[i].get('frame'))):
            if data[i].get('precedingId')[frame] != 0:
                if preceding_id != 0 and data[i].get('precedingId')[frame] != preceding_id and following_started:
                    frame_following_end = frame - 1
                    if frame_following_end != frame_following_start:
                        following_data.append(
                            {"ego_id": ego_id, "pred_id": preceding_id, "following_start": frame_following_start,
                             "following_duration": following_duration, "following_end": frame_following_end,
                             "dhw": statistics.mean(following_dhw), "thw": statistics.mean(following_thw),
                             "ttc": statistics.mean(following_ttc),
                             "ego_speed": ego_speed, "pred_speed": pred_speed})
                    following_started = False
                    following_dhw = []
                    following_thw = []
                    following_ttc = []
                    ego_speed = []
                    pred_speed = []
                    frame_following_start = 0
                    following_duration = 0
                preceding_id = data[i].get('precedingId')[frame]
                if ((get_vehicle_class(meta_data, preceding_id) == preceding_type)
                        and (get_vehicle_class(meta_data, ego_id) == my_type)):
                    if following_started is False:
                        following_started = True
                        frame_following_start = frame
                        following_dhw.append(data[i].get('dhw')[frame])
                        following_thw.append(data[i].get('thw')[frame])
                        following_ttc.append(get_ttc(data[i].get('dhw')[frame],
                                                     data[i].get('xVelocity')[frame],
                                                     data[i].get('precedingXVelocity')[frame]))
                        ego_speed.append(data[i].get('xVelocity')[frame])
                        pred_speed.append(data[i].get('precedingXVelocity')[frame])
                    else:
                        following_dhw.append(data[i].get('dhw')[frame])
                        following_thw.append(data[i].get('thw')[frame])
                        following_ttc.append(get_ttc(data[i].get('dhw')[frame],
                                                     data[i].get('xVelocity')[frame],
                                                     data[i].get('precedingXVelocity')[frame]))
                        ego_speed.append(data[i].get('xVelocity')[frame])
                        pred_speed.append(data[i].get('precedingXVelocity')[frame])
                    following_duration = following_duration + 1
            else:
                if following_started is True:
                    frame_following_end = frame-1
                    if frame_following_end != frame_following_start:
                        following_data.append(
                            {"ego_id": ego_id, "pred_id": preceding_id, "following_start": frame_following_start,
                             "following_duration": following_duration, "following_end": frame_following_end,
                             "dhw": statistics.mean(following_dhw), "thw": statistics.mean(following_thw),
                             "ttc": statistics.mean(following_ttc),
                             "ego_speed": ego_speed, "pred_speed": pred_speed})
                    following_started = False
                    following_dhw = []
                    following_thw = []
                    following_ttc = []
                    ego_speed = []
                    pred_speed = []
                    frame_following_start = 0
                    following_duration = 0
                    preceding_id = 0
    return following_data


def get_vehicle_class(meta_data, id):
    """

    :param meta_data: track meta information from highD dataset
    :param id: vehicle's id in the dataset
    :return: vehicle type (string: 'Car' or 'Truck')
    """
    return meta_data[id].get('class')


def get_ttc(dhw, my_speed, pred_speed):
    if my_speed > pred_speed and dhw != 0:
        return dhw / (my_speed - pred_speed)
    else:
        return np.nan
