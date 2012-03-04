import sys
import math


def recommend_next_location(list_of_request_locations_and_closest_fountains):
    #structure of the input is (req lat, req long, close fount lat, close long)
    
    scale = float(20)
    max_points = find_max_and_min_points(list_of_request_locations_and_closest_fountains)
    potential_points = []

    x_increment = (max_points[1] - max_points[0]) / scale
    y_increment = (max_points[3] - max_points[2]) / scale

    x_coords = []
    y_coords = []

    for i in range(int(scale)):
        x_coords.append(max_points[0] + (i * x_increment))
        y_coords.append(max_points[2] + (i * y_increment))


    for x in x_coords:
        for y in y_coords:
            potential_points.append((x,y))
    
    best_coordinate = ()
    best_savings = 0
          
    #print potential_points
    
    for potential_point in potential_points:
        
        savings = 0
        
        for requested_location in list_of_request_locations_and_closest_fountains:
            new_distance = find_distance(potential_point, requested_location[0:2])
            closest_fountain_distance = find_distance(requested_location[0:2], 
                    requested_location[2:]) 
            if new_distance < closest_fountain_distance:
                savings = savings + (closest_fountain_distance - new_distance)

        if savings > best_savings:
            best_savings = savings
            best_coordinate = potential_point
   

    return best_coordinate 



def find_max_and_min_points(list_of_locations):
    #sort based on x to find max and min
    list_of_locations = sorted(list_of_locations, 
            cmp=lambda tupleA, tupleB: cmp(tupleA[0], tupleB[0]))
    
    max_tuple = list_of_locations[-1]
    min_tuple = list_of_locations[0]
    
    max_x = max_tuple[0]
    min_x = min_tuple[0]

    # sort based on y to find max and min
    list_of_locations = sorted(list_of_locations, 
            cmp=lambda tupleA, tupleB: cmp(tupleA[1], tupleB[1]))
    max_tuple = list_of_locations[-1]
    min_tuple = list_of_locations[0]
    max_y = max_tuple[1]
    min_y = min_tuple[1]

    return (min_x, max_x, min_y, max_y)


def find_distance(tuple1, tuple2):
    xdist = tuple2[0]-tuple1[0]
    ydist = tuple2[1]-tuple1[1]

    return math.sqrt(pow(xdist,2) + pow(ydist,2))


def find_closest_fountain(current_location_tuple, list_of_fountain_tuples):
    closest_tuple = list_of_fountain_tuples[0]
    current_min_distance = find_distance(current_location_tuple, list_of_fountain_tuples[0])

    for fountain_location in list_of_fountain_tuples:
        distance = find_distance(current_location_tuple, fountain_location) 

        if distance < current_min_distance:
            current_min_distance = distance
            closest_tuple = fountain_location

    return closest_tuple

def test_generator():
    list_of_fountains = [(2,3), (10,12), (20,30), (6,14)]
    list_of_requests = [(1,1), (1,10), (10,20), (5,5), (40,12), (3,20), (20,3)]

    output = []

    for request in list_of_requests:
        output.append(request + find_closest_fountain(request, list_of_fountains))

    return output
