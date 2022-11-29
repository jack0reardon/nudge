import scripts
import scripts.classes as classes
import networkx as nx

def get_cost_of_travelling_between_stations(graph_of_stations, start_station, end_station, speed):
    distance = nx.shortest_path_length(graph_of_stations, source = start_station, target = end_station, weight = 'weight')
    time = distance / speed
    cost = time
    return cost

def get_best_path(graph_of_stations, start_station, end_station, explored_stations = None):
    if not start_station.does_have_free_bike():
        # Propose an alternative start station
        latest_explored_stations = explored_stations.append(start_station)
        next_best_path = None
        for adj_start_station in end_station.adjacent_stations:
            if adj_start_station not in explored_stations:
                cost_of_walking_to_adj_end_station = get_cost_of_travelling_between_stations(graph_of_stations, start_station, adj_start_station, scripts.SPEED_OF_WALKING_KMPH)
                alternative_path = get_best_path(graph_of_stations, start_station, adj_start_station, latest_explored_stations)

                if next_best_path is None:
                    next_best_path = alternative_path
                elif alternative_path.cost + cost_of_walking_to_adj_end_station < next_best_path.cost:
                    next_best_path = alternative_path
        
        if next_best_path is None:
            # No path is better - just walk!
            cost = get_cost_of_travelling_between_stations(graph_of_stations, start_station, end_station, scripts.SPEED_OF_WALKING_KMPH)
            return classes.Route(start_station, end_station, cost)
        else:
            return next_best_path
    
    if end_station.does_have_free_docks():
        # Propose an alternative end station
        return None

    # If the code made it here, then the start and end stations have bikes
    cost = get_cost_of_travelling_between_stations(graph_of_stations, start_station, end_station, scripts.SPEED_OF_BIKE_KMPH)
    return classes.Route(start_station, end_station, cost)