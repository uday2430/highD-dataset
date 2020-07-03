import numpy as np

def find_initial_state(meta_data, data):
    init_states = []
    for id in range(1, len(meta_data)+1):
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