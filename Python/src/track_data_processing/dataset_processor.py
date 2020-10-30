import statistics
import numpy as np
import matplotlib.pyplot as plt
from .extraction_conditions import *


def find_initial_state(meta_data, data):
    init_states = []
    for id in range(1, len(meta_data) + 1):
        veh_id = meta_data[id].get('id')
        veh_class = meta_data[id].get('class')
        veh_length = meta_data[id].get('width')
        veh_init_frame = meta_data[id].get('initialFrame')
        veh_init_lane = get_initial_lane(data, id)
        veh_init_pos = get_initial_position(meta_data, data, id)
        veh_init_speed = get_initial_speed(data, id)
        # record the behaviour
        init_states.append(
            {"id": veh_id,
             "length": veh_length,
             "class": veh_class,
             "initial_frame": veh_init_frame,
             "initial_lane": veh_init_lane,
             "initial_position": veh_init_pos,
             "initial_speed": veh_init_speed
             })
    return init_states


def get_initial_lane(data, id):
    for i in range(0, len(data)):
        if data[i].get('id') == id:
            lane = data[i].get('laneId')[0]
            return lane


def get_initial_position(meta_data, data, id):
    for i in range(0, len(data)):
        if data[i].get('id') == id:
            if meta_data[id].get('drivingDirection') == 2:
                pos = data[i].get('x')[0] + data[i].get('width')[0]
            elif meta_data[id].get('drivingDirection') == 1:
                pos = data[i].get('x')[0]
            return pos


def get_initial_speed(data, id):
    for i in range(0, len(data)):
        if data[i].get('id') == id:
            speed = data[i].get('xVelocity')[0]
            return speed


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
            if (data[i].get('precedingId')[frame] != 0
                    and (CF_TGAP_LOWER_BOUND < data[i].get('thw')[frame] < CF_TGAP_UPPER_BOUND)):
                if preceding_id != 0 and data[i].get('precedingId')[frame] != preceding_id and following_started:
                    # this condition means that the lead vehicle has changed
                    frame_following_end = frame - 1
                    if frame_following_end != frame_following_start:
                        following_data.append(
                            {"ego_id": ego_id, "pred_id": preceding_id, "following_start": frame_following_start,
                             "following_duration": following_duration, "following_end": frame_following_end,
                             "dhw": statistics.mean(following_dhw), "thw": np.nanmean(following_thw),
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
                        if data[i].get('dhw')[frame] > 0:
                            following_dhw.append(data[i].get('dhw')[frame])
                            following_ttc.append(get_ttc(data[i].get('dhw')[frame],
                                                         data[i].get('xVelocity')[frame],
                                                         data[i].get('precedingXVelocity')[frame]))
                        if data[i].get('thw')[frame] > 0:
                            following_thw.append(data[i].get('thw')[frame])
                        else:
                            following_thw.append(np.nan)
                        ego_speed.append(data[i].get('xVelocity')[frame])
                        pred_speed.append(data[i].get('precedingXVelocity')[frame])
                    else:
                        if data[i].get('dhw')[frame] > 0:
                            following_dhw.append(data[i].get('dhw')[frame])
                            following_ttc.append(get_ttc(data[i].get('dhw')[frame],
                                                         data[i].get('xVelocity')[frame],
                                                         data[i].get('precedingXVelocity')[frame]))
                        if data[i].get('thw')[frame] > 0:
                            following_thw.append(data[i].get('thw')[frame])
                        else:
                            following_thw.append(np.nan)
                        ego_speed.append(data[i].get('xVelocity')[frame])
                        pred_speed.append(data[i].get('precedingXVelocity')[frame])
                    following_duration = following_duration + 1
            else:
                if following_started is True:
                    frame_following_end = frame - 1
                    if frame_following_end != frame_following_start:
                        following_data.append(
                            {"ego_id": ego_id, "pred_id": preceding_id, "following_start": frame_following_start,
                             "following_duration": following_duration, "following_end": frame_following_end,
                             "dhw": statistics.mean(following_dhw), "thw": np.nanmean(following_thw),
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
    my_speed = abs(my_speed)
    pred_speed = abs(pred_speed)
    if my_speed > pred_speed and dhw != 0:
        return dhw / (my_speed - pred_speed)
    else:
        return np.nan


def find_lane_changes(meta_data, data):
    """
    Find out lane-changing situations from the dataset

    :param meta_data: track meta information from highD dataset
    :param data: track data from highD dataset

    :return: a list of dictionary with
        sumLC: total number of lane changes
        carLC: total number of lane changes by cars
        truckLC: total number of lane changes by trucks
        totalCar: total number of cars
        totalTruck: total number of trucks
    """
    n_car = 0
    n_car_lc = 0
    n_truck = 0
    n_truck_lc = 0
    for i in range(0, len(data)):
        ego_id = data[i].get('id')
        n_lc = meta_data[ego_id].get('numLaneChanges')
        vtype = meta_data[ego_id].get('class')
        if vtype == "Car":
            n_car_lc = n_car_lc + n_lc
            n_car = n_car + 1
        elif vtype == "Truck":
            n_truck_lc = n_truck_lc + n_lc
            n_truck = n_truck + 1
        else:
            print("vehicle class unknown")
    n_total_lc = n_car_lc + n_truck_lc
    lc_data = {
        "sumLC": n_total_lc,
        "carLC": n_car_lc,
        "truckLC": n_truck_lc,
        "totalCar": n_car,
        "totalTruck": n_truck
    }
    return lc_data


def get_lane_change_trajectory(meta_data, data):
    y_accel_car_LC = []
    y_accel_truck_LC = []
    y_accel_car_noLC = []
    y_accel_truck_noLC = []
    y_pos_car_LC = []
    y_pos_car_noLC = []
    y_pos_truck_LC = []
    y_pos_truck_noLC = []
    y_speed_car_LC = []
    y_speed_car_noLC = []
    y_speed_truck_LC = []
    y_speed_truck_noLC = []
    for i in range(0, len(data)):
        ego_id = data[i].get('id')
        n_lc = meta_data[ego_id].get('numLaneChanges')
        vtype = meta_data[ego_id].get('class')
        if n_lc > 0:
            # this vehicle changes lane
            # find lane change index
            LC_index = []
            totalFrames = len(data[i].get('laneId'))
            lane_ids = list(data[i].get('laneId'))
            current_lane = lane_ids[0]
            for j in range(0, totalFrames):
                if lane_ids[j] != current_lane:
                    LC_index.append(j)
                    current_lane = lane_ids[j]
            for index in LC_index:
                if LC_MARGIN_FRAMES < index < (totalFrames - LC_MARGIN_FRAMES):
                    lower_bound = index - LC_MARGIN_FRAMES
                    upper_bound = index + LC_MARGIN_FRAMES
                    if vtype == "Car":
                        y_accel_car_LC += list(data[i].get('yAcceleration')[lower_bound:upper_bound])
                        y_speed_car_LC += list(data[i].get('yVelocity')[lower_bound:upper_bound])
                        y_pos_car_LC = list(data[i].get('y')[lower_bound:upper_bound])
                        # plt.plot(data[i].get('y'))
                        # plt.axvline(x=index)
                        # plt.show()
                    elif vtype == "Truck":
                        y_accel_truck_LC += list(data[i].get('yAcceleration')[lower_bound:upper_bound])
                        y_speed_truck_LC += list(data[i].get('yVelocity')[lower_bound:upper_bound])
                        y_pos_truck_LC = list(data[i].get('y')[lower_bound:upper_bound])
                    else:
                        print("vehicle class unknown")
        else:
            # this vehicle did not change lane
            # find out average yAcceleration
            # this vehicle changes lane
            if vtype == "Car":
                y_accel_car_noLC += list(data[i].get('yAcceleration'))
                y_speed_car_noLC += list(data[i].get('yVelocity'))
                y_pos_car_noLC = list(data[i].get('y'))
            elif vtype == "Truck":
                # if absolute value is desired >> [abs(a) for a in list(data[i].get('yAcceleration'))]
                y_accel_truck_noLC += list(data[i].get('yAcceleration'))
                y_speed_truck_noLC += list(data[i].get('yVelocity'))
                y_pos_truck_noLC = list(data[i].get('y'))
            else:
                print("vehicle class unknown")
    lc_trajectory = {
        "Car_yAccel_LC": y_accel_car_LC,
        "Car_yAccel_noLC": y_accel_car_noLC,
        "Truck_yAccel_LC": y_accel_truck_LC,
        "Truck_yAccel_noLC": y_accel_truck_noLC,
        "Car_ySpeed_LC": y_speed_car_LC,
        "Car_ySpeed_noLC": y_speed_car_noLC,
        "Truck_ySpeed_LC": y_speed_truck_LC,
        "Truck_ySpeed_noLC": y_speed_truck_noLC,
        "Car_yPos_LC": y_pos_car_LC,
        "Car_yPos_noLC": y_pos_car_noLC,
        "Truck_yPos_LC": y_pos_truck_LC,
        "Truck_yPos_noLC": y_pos_truck_noLC
    }
    return lc_trajectory
