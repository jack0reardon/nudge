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

    def add_adjacent_intersection(self, adjacent_intersection):
        self.adjacent_intersections.append(adjacent_intersection)
        adjacent_intersection.adjacent_intersections.append(self)

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
        
        node_colours = ['pink' if intersection.__class__.__name__ == 'Station' else 'grey' for intersection in Intersection.all_intersections]
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
            ' lat:' + str(self.lat) + \
            ' lon:' + str(self.lon) + \
            ' adjacent_intersections:' + adjacent_intersections_str

    def __repr__(self):
        return '\n' + self.get_intersection_as_str()

    def __str__(self):
        return self.__repr__()


class Station(Intersection):
    def __init__(self, n_docks, n_bikes_docked, lat, lon):
        self.__n_docks = n_docks
        self.__n_bikes_docked = n_bikes_docked
        super().__init__(lat, lon)

    def does_have_free_docks(self):
        return self.__n_bikes_docked < self.__n_docks

    def does_have_free_bike(self):
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

    def get_best_path_for_rider(self, graph_of_stations):
        return funs.get_best_path(graph_of_stations, self.__home_station.station_id, self.__work_station.station_id)
        
    def get_home_station(self):
        return self.__home_station

    def get_work_station(self):
        return self.__work_station

    def ride_from_to(self, from_station, to_station):
        from_station.rent_a_bike()
        to_station.dock_a_bike()


class route():
    def __init__(self, start_station, end_station, cost):
        self.start_station = start_station
        self.end_station = end_station
        self.cost = cost