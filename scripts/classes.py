import scripts
import scripts.functions as funs
import math
import networkx as nx
import matplotlib.pyplot as plt


class Intersection():
    all_intersections = []

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.adjacent_intersections = []
        Intersection.all_intersections.append(self)
        self.intersection_id = len(Intersection.all_intersections)
        self.is_station = False

    def add_adjacent_intersection(self, adjacent_intersection):
        self.adjacent_intersections.append(adjacent_intersection)
        adjacent_intersection.adjacent_intersections.append(self)

    def does_have_free_docks(self):
        return False

    def does_have_free_bikes(self):
        return False

    @staticmethod
    def get_all_stations_with_free_bikes():
        return [intersection for intersection in Intersection.all_intersections if intersection.does_have_free_bikes()]
    
    @staticmethod
    def get_all_stations_with_free_docks():
        return [intersection for intersection in Intersection.all_intersections if intersection.does_have_free_docks()]

    @staticmethod
    def get_distance_between_intersections(first_intersection, second_intersection):
        return math.sqrt((first_intersection.lat - second_intersection.lat)**2 + (first_intersection.lon - second_intersection.lon)**2)

    @staticmethod
    def get_graph_of_intersections():
        the_graph = nx.Graph()
        for intersection in Intersection.all_intersections:
            the_graph.add_node(intersection.intersection_id, pos = (intersection.lat, intersection.lon))
            for adjacent_intersection in intersection.adjacent_intersections:
                the_graph.add_edge(intersection.intersection_id, adjacent_intersection.intersection_id, \
                    weight = Intersection.get_distance_between_intersections(intersection, adjacent_intersection))

        return the_graph

    @staticmethod
    def draw_graph_of_intersections(graph_of_stations = None):
        if graph_of_stations is None:
            graph_of_stations = Station.get_graph_of_stations()

        pos = nx.get_node_attributes(graph_of_stations, 'pos')
        
        node_colours = ['pink' if intersection.is_station else 'grey' for intersection in Intersection.all_intersections]
        # Re-order the colours to match the order of their appearance in the graph
        node_colours_reordered = [node_colours[i - 1] for i in pos.keys()]
        
        nx.draw(graph_of_stations, pos, node_color = node_colours_reordered, with_labels = True, font_weight = 'bold')
        plt.show()

    def get_intersection_as_str(self):
        if len(self.adjacent_intersections) == 0:
            adjacent_intersections_str = 'None'
        else:
            adjacent_intersections_str = '-'.join([str(adjacent_intersection.intersection_id) for adjacent_intersection in self.adjacent_intersections])

        return 'intersection_id:' + str(self.intersection_id) + \
            ' is_station:' + str(self.is_station) + \
            ' lat-lon:' + str(self.lat) + '-' + str(self.lon) + \
            ' adjacent_intersections:' + adjacent_intersections_str

    def __repr__(self):
        return '\n' + self.get_intersection_as_str()

    def __str__(self):
        return self.__repr__()


class Station(Intersection):
    all_pick_up_bonus_stations = []
    all_drop_off_bonus_stations = []

    def __init__(self, n_docks, n_bikes_docked, lat, lon):
        self.__n_docks = n_docks
        self.__n_bikes_docked = n_bikes_docked
        super().__init__(lat, lon)
        self.is_station = True
        self.pick_up_bonus_points = 0
        self.drop_off_bonus_points = 0

    def set_pick_up_bonus_points(self, pick_up_bonus_points):
        self.pick_up_bonus_points = pick_up_bonus_points
        if pick_up_bonus_points > 0 and self not in Station.all_pick_up_bonus_stations:
            Station.all_pick_up_bonus_stations.append(self)
        elif pick_up_bonus_points == 0 and self in Station.all_pick_up_bonus_stations:
            Station.all_pick_up_bonus_stations.remove(self)

    def set_drop_off_bonus_points(self, drop_off_bonus_points):
        self.drop_off_bonus_points = drop_off_bonus_points
        if drop_off_bonus_points > 0 and self not in Station.all_drop_off_bonus_stations:
            Station.all_drop_off_bonus_stations.append(self)
        elif drop_off_bonus_points == 0 and self in Station.all_drop_off_bonus_stations:
            Station.all_drop_off_bonus_stations.remove(self)

    def does_have_free_docks(self):
        return self.__n_bikes_docked < self.__n_docks

    def does_have_free_bikes(self):
        return self.__n_bikes_docked > 0

    def dock_a_bike(self):
        self.__n_bikes_docked += 1
    
    def rent_a_bike(self):
        self.__n_bikes_docked -= 1

    def __repr__(self):
        return '\n' + super().get_intersection_as_str() + \
                ' n_docks:' + str(self.__n_docks) + \
                ' n_bikes_docked:' + str(self.__n_bikes_docked)


class Rider():
    all_riders = []

    def __init__(self, home_station, work_station):
        self.__home_station = home_station
        self.__work_station = work_station

        Rider.all_riders.append(self)

    def get_best_route_for_rider(self, to_work):
        if to_work:
            return funs.get_best_route(self.__home_station, self.__work_station)
        else:
            return funs.get_best_route(self.__work_station, self.__home_station)
        
    def get_home_station(self):
        return self.__home_station

    def get_work_station(self):
        return self.__work_station

    def ride_from_to(self, from_station, to_station):
        from_station.rent_a_bike()
        to_station.dock_a_bike()


class Route():
    def __init__(self, start_intersection, walk_to_intersection, walk_from_intersection, end_intersection, time = None):
        self.start_intersection = start_intersection
        self.walk_to_intersection = walk_to_intersection
        self.walk_from_intersection = walk_from_intersection
        self.end_intersection = end_intersection
        self.time = time
        if time is not None:
            self.calculate_value_of_route()
            
    def calculate_time_of_route(self, graph_of_intersections):
        walking_time_A = funs.get_time_to_travel_between_intersections(graph_of_intersections, \
            self.start_intersection.intersection_id, \
            self.walk_to_intersection.intersection_id, \
            scripts.SPEED_OF_WALKING_KMPH)

        riding_time = funs.get_time_to_travel_between_intersections(graph_of_intersections, \
            self.walk_to_intersection.intersection_id, \
            self.walk_from_intersection.intersection_id, \
            scripts.SPEED_OF_BIKE_KMPH)
        
        walking_time_B = funs.get_time_to_travel_between_intersections(graph_of_intersections, \
            self.walk_from_intersection.intersection_id, \
            self.end_intersection.intersection_id, \
            scripts.SPEED_OF_WALKING_KMPH)

        self.time = walking_time_A + riding_time + walking_time_B

    def calculate_value_of_route(self):
        if self.walk_to_intersection != self.walk_from_intersection:
            drop_off_and_pick_up_bonus_points = self.walk_to_intersection.pick_up_bonus_points + \
                self.walk_from_intersection.drop_off_bonus_points
        else:
            drop_off_and_pick_up_bonus_points = 0
        self.value_of_route = -self.time + drop_off_and_pick_up_bonus_points

    def __repr__(self):
        return 'start_intersection:' + str(self.start_intersection.intersection_id) + \
            ' walk_to_intersection:' + str(self.walk_to_intersection.intersection_id) + \
            ' walk_from_intersection:' + str(self.walk_from_intersection.intersection_id) + \
            ' end_intersection:' + str(self.end_intersection.intersection_id) + \
            ' time:' + str(self.time) + \
            ' value_of_route:' + str(self.value_of_route)

    def __str__(self):
        return self.__repr__()