import sys
import math

def recommend_next_location(list_of_request_locations, list_of_closest_fountains):
    
    scale = 1000
    max_points = find_max_and_min_points([list_of_request_locations])

    potential_points = []

    x_increment = (max_points[1] - max_points[0])/scale
    y_increment = (max_points[3] - max_points[2])/scale

    x_coords = []
    y_coords = []

    for i in range(scale):
        x_coords.append(max_points[0]+i*x_increment)
        y_coords.append(max_points[2]+i*y_increment)


    for x in x_coords:
        for y in y_coords:
            potential_points.append((x,y))
    
    best_coordinate = ()
    best_savings = 0
          
    for potential_point in potential_points:
        
        savings = 0
        
        for requested_location in list_of_requested_locations:
            new_distance = find_distance(potential_point, requested_location)
            closest_fountain_distance = find_distance(requested_location, closest_fountain) :
            if new_distance < closest_fountain_distance:
                savings = savings + (closest_fountain_distance-new_distance)

        if savings > best_savings:
            best_savings = savings
            best_coordinate = potential point
   

    return best_coordinate 
)

def find_max_and_min_points(list_of_locations):
    
    #sort based on x to find max and min
    list_of_locations = sorted(list_of_locations, cmp=lambda tupleA, tupleB: cmp(tupleA[0], tupleB[0]), reverse=False)
    print list_of_locations
    max_tuple = list_of_locations[-1]
    min_tuple = list_of_locations[0]
    max_x = max_tuple[0]
    # sort based on y to find max and min
    list_of_locations = sorted(list_of_locations, cmp=lambda tupleA, tupleB: cmp(tupleA[1], tupleB[1]), reverse=False)
    print list_of_locations
    max_tuple = list_of_locations[-1]
    min_tuple = list_of_locations[0]
    max_y = max_tuple[1]
    min_y = min_tuple[1]

    return (min_x, max_x, min_y, max_y)


def find_distance(tuple1, tuple2):
    
    xdist = tuple2[0]-tuple1[0]
    ydist = tuple2[1]-tuple1[1]

    return math.sqrt(pow(xdist,2)+pow(ydist,2))

def find_closest_fountain(current_location_tuple, list_of_fountain_tuples):
      
    closest_tuple = list_of_fountain_tuples[0]
    current_min_distance = find_distance(current_location_tuple, list_of_fountain_tuples[0])

    for fountain_location in list_of_fountain_tuples:
        
        distance = find_distance(current_location_tuple, fountain_location) 
        
        if distance < current_min_distance:
            current_min_distance = distance
            closest_tuple = fountain_location

    return closest_tuple


