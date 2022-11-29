import scripts
import scripts.functions as funs
import math
import networkx as nx
import matplotlib.pyplot as plt

class Station():
    n_stations = 0
    all_stations = []

    def __init__(self, n_docks, n_bikes_docked, lat, lon):
        self.__n_docks = n_docks
        self.__n_bikes_docked = n_bikes_docked
        self.lat = lat
        self.lon = lon

        Station.all_stations.append(self)

        self.station_id = len(Station.all_stations)
        self.adjacent_stations = []

    def add_adjacent_station(self, adjacent_station):
        self.adjacent_stations.append(adjacent_station)
        adjacent_station.adjacent_stations.append(self)

    def does_have_free_docks(self):
        return self.__n_bikes_docked < self.__n_docks

    def does_have_free_bike(self):
        return self.__n_bikes_docked > 0

    def dock_a_bike(self):
        self.__n_bikes_docked += 1
    
    def rent_a_bike(self):
        self.__n_bikes_docked -= 1

    def __repr__(self):
        if len(self.adjacent_stations) == 0:
            adjacent_stations_str = 'None'
        else:
            adjacent_stations_str = ', '.join([str(adjacent_station.station_id) for adjacent_station in self.adjacent_stations])

        return 'n_docks: ' + str(self.__n_docks) + \
            ', n_bikes_docked: ' + str(self.__n_bikes_docked) + \
            ', lat: ' + str(self.lat) + \
            ', lon: ' + str(self.lon) + \
            ', adjacent_stations: ' + adjacent_stations_str

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def get_distance_between_stations(first_station, second_station):
        return math.sqrt((first_station.lat - second_station.lat)**2 + (first_station.lon - second_station.lon)**2)

    @staticmethod
    def get_graph_of_stations():
        the_graph = nx.Graph()
        for station in Station.all_stations:
            the_graph.add_node(station.station_id, pos = (station.lat, station.lon))
            for adjacent_station in station.adjacent_stations:
                the_graph.add_edge(station.station_id, adjacent_station.station_id, weight = Station.get_distance_between_stations(station, adjacent_station))

        return the_graph

    @staticmethod
    def draw_graph_of_stations(graph_of_stations = None):
        if graph_of_stations is None:
            graph_of_stations = Station.get_graph_of_stations()

        pos = nx.get_node_attributes(graph_of_stations, 'pos')
        nx.draw(graph_of_stations, pos, with_labels = True, font_weight = 'bold')
        plt.show()


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