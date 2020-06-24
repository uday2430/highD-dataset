import statistics

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
    n_car_lc = 0
    n_car = 0
    n_truck = 0
    n_truck_lc = 0
    for i in range(0, len(data)):
        ego_id = data[i].get('id')
        n_lc = meta_data[ego_id].get('numLaneChanges')
        type = meta_data[ego_id].get('class')
        if type == "Car":
            n_car_lc = n_car_lc + n_lc
            n_car = n_car + 1
        elif type == "Truck":
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
