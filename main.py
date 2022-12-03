import scripts.classes as classes
import networkx as nx

station_1 = classes.Station(10, 2, 1, 1)
station_2 = classes.Station(20, 0, 10, 10)
station_3 = classes.Station(10, 0, 2, 8)
station_4 = classes.Station(15, 14, 10, 1)
station_5 = classes.Station(1, 1, 5, 5)
station_1.set_pick_up_bonus_points(100)
station_3.set_drop_off_bonus_points(100)
station_1.add_adjacent_intersection(station_5)
station_5.add_adjacent_intersection(station_2)
station_3.add_adjacent_intersection(station_2)
station_4.add_adjacent_intersection(station_2)
station_4.add_adjacent_intersection(station_1)
station_4.add_adjacent_intersection(station_5)
print(classes.Intersection.all_intersections)

graph_of_intersections = classes.Intersection.get_graph_of_intersections()
classes.Station.draw_graph_of_intersections(graph_of_intersections)




rider_1 = classes.Rider(station_1, station_2)
rider_2 = classes.Rider(station_1, station_2)
rider_3 = classes.Rider(station_1, station_2)
rider_4 = classes.Rider(station_3, station_2)
rider_5 = classes.Rider(station_3, station_2)
rider_6 = classes.Rider(station_3, station_4)

for rider in classes.Rider.all_riders:
    best_route_for_rider = rider.get_best_route_for_rider(to_work = True)
    rider.ride_from_to(best_route_for_rider.walk_to_intersection, best_route_for_rider.walk_from_intersection)

print(classes.Intersection.all_intersections)

for rider in classes.Rider.all_riders:
    best_route_for_rider = rider.get_best_route_for_rider(to_work = False)
    print(best_route_for_rider)
    rider.ride_from_to(best_route_for_rider.walk_to_intersection, best_route_for_rider.walk_from_intersection)

print(classes.Intersection.all_intersections)


for simulation in range(10):
    print(simulation)