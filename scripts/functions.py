import scripts
import scripts.classes as classes
import networkx as nx

def get_time_to_travel_between_intersections(graph_of_intersections, start_intersection_id, end_intersection_id, speed):
    distance = nx.shortest_path_length(graph_of_intersections, source = start_intersection_id, target = end_intersection_id, weight = 'weight')
    time = distance / speed
    return time

def get_best_route(start_intersection, end_intersection):
    # First - find the fastest route
    graph_of_intersections = classes.Intersection.get_graph_of_intersections()
    fastest_route = get_fastest_route(graph_of_intersections, start_intersection, end_intersection, explored_intersections = [])

    # Second - target any other intersection that offers a reward (either starting or ending there)
    # No need to target intersections that don't offer a reward since they would be longer routes and therefore less appealing
    # No need to target intersections that cost more to get to than they reward, since it would be preferable for the Rider
    # to just take a bike from a non-bonus intersection and dock it at Work (or dock it at a )
    all_stations_with_free_bikes = classes.Intersection.get_all_stations_with_free_bikes()
    all_stations_with_free_docks = classes.Intersection.get_all_stations_with_free_docks()
    
    best_route = fastest_route

    for pick_up_bonus_station in classes.Station.all_pick_up_bonus_stations:
        for free_dock_station in all_stations_with_free_docks:
            if pick_up_bonus_station != free_dock_station and pick_up_bonus_station.does_have_free_bikes():
                proposed_route = classes.Route(start_intersection, pick_up_bonus_station, free_dock_station, end_intersection, time = None)
                proposed_route.calculate_time_of_route(graph_of_intersections)
                proposed_route.calculate_value_of_route()
                if proposed_route.value_of_route > best_route.value_of_route:
                    best_route = proposed_route

    for drop_off_bonus_station in classes.Station.all_drop_off_bonus_stations:
        for free_bike_station in all_stations_with_free_bikes:
            if free_bike_station != drop_off_bonus_station and drop_off_bonus_station.does_have_free_docks():
                proposed_route = classes.Route(start_intersection, free_bike_station, drop_off_bonus_station, end_intersection, time = None)
                proposed_route.calculate_time_of_route(graph_of_intersections)
                proposed_route.calculate_value_of_route()
                if proposed_route.value_of_route > best_route.value_of_route:
                    best_route = proposed_route
    
    return best_route
     

def get_fastest_route(graph_of_intersections, start_intersection, end_intersection, explored_intersections):
    fastest_route = None

    latest_explored_intersections = explored_intersections.copy()

    if not start_intersection.does_have_free_bikes():
        # Propose an alternative start intersection
        latest_explored_intersections.append(start_intersection)
        for alt_start_intersection in start_intersection.adjacent_intersections:
            if alt_start_intersection not in latest_explored_intersections:
                time_to_walk_to_adj_start_intersection = get_time_to_travel_between_intersections(graph_of_intersections, start_intersection.intersection_id, alt_start_intersection.intersection_id, scripts.SPEED_OF_WALKING_KMPH)
                alternative_route = get_fastest_route(graph_of_intersections, alt_start_intersection, end_intersection, latest_explored_intersections)

                if fastest_route is None:
                    fastest_route = classes.Route(start_intersection, \
                        alternative_route.walk_to_intersection, \
                        alternative_route.walk_from_intersection, \
                        end_intersection,
                        alternative_route.time + time_to_walk_to_adj_start_intersection)
                elif alternative_route.time + time_to_walk_to_adj_start_intersection < fastest_route.time:
                    fastest_route = classes.Route(start_intersection, \
                        alternative_route.walk_to_intersection, \
                        alternative_route.walk_from_intersection, \
                        end_intersection, \
                        alternative_route.time + time_to_walk_to_adj_start_intersection)
        
        if fastest_route is None:
            # No path is better - just walk!
            time = get_time_to_travel_between_intersections(graph_of_intersections, start_intersection.intersection_id, end_intersection.intersection_id, scripts.SPEED_OF_WALKING_KMPH)
            return classes.Route(start_intersection, end_intersection, end_intersection, end_intersection, time)
        else:
            return fastest_route
    
    if not end_intersection.does_have_free_docks():
        # Propose an alternative end intersection
        latest_explored_intersections.append(end_intersection)
        for alt_end_intersection in end_intersection.adjacent_intersections:
            if alt_end_intersection not in latest_explored_intersections:
                time_to_walk_to_adj_end_intersection = get_time_to_travel_between_intersections(graph_of_intersections, alt_end_intersection.intersection_id, end_intersection.intersection_id, scripts.SPEED_OF_WALKING_KMPH)
                alternative_route = get_fastest_route(graph_of_intersections, start_intersection, alt_end_intersection, latest_explored_intersections)

                if fastest_route is None:
                    fastest_route = classes.Route(start_intersection, \
                        alternative_route.walk_to_intersection, \
                        alternative_route.walk_from_intersection, \
                        end_intersection,
                        alternative_route.time + time_to_walk_to_adj_end_intersection)
                elif alternative_route.time + time_to_walk_to_adj_end_intersection < fastest_route.time:
                    fastest_route = classes.Route(start_intersection, \
                        alternative_route.walk_to_intersection, \
                        alternative_route.walk_from_intersection, \
                        end_intersection, \
                        alternative_route.time + time_to_walk_to_adj_end_intersection)
        
        if fastest_route is None:
            # No path is better - just walk!
            time = get_time_to_travel_between_intersections(graph_of_intersections, start_intersection.intersection_id, end_intersection.intersection_id, scripts.SPEED_OF_WALKING_KMPH)
            return classes.Route(start_intersection, end_intersection, end_intersection, end_intersection, time)
        else:
            return fastest_route

    # If the code made it here, then the start and end intersections have bikes
    time = get_time_to_travel_between_intersections(graph_of_intersections, start_intersection.intersection_id, end_intersection.intersection_id, scripts.SPEED_OF_BIKE_KMPH)
    return classes.Route(start_intersection, start_intersection, end_intersection, end_intersection, time)
