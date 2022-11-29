import scripts.classes as classes

station_1 = classes.Station(10, 6, 1, 1)
station_2 = classes.Station(20, 14, 10, 10)
station_3 = classes.Station(15, 12, 2, 8)
station_4 = classes.Station(15, 12, 10, 1)
intersection_1 = classes.Intersection(5, 5)
station_1.add_adjacent_intersection(intersection_1)
intersection_1.add_adjacent_intersection(station_2)
station_3.add_adjacent_intersection(station_2)
station_4.add_adjacent_intersection(station_2)
station_4.add_adjacent_intersection(station_1)
station_4.add_adjacent_intersection(intersection_1)
print(classes.Intersection.all_intersections)

graph_of_intersections = classes.Intersection.get_graph_of_intersections()
classes.Station.draw_graph_of_intersections(graph_of_intersections)




rider_1 = classes.Rider(station_1, station_2)
rider_2 = classes.Rider(station_1, station_2)
rider_3 = classes.Rider(station_1, station_2)
rider_4 = classes.Rider(station_3, station_2)
rider_5 = classes.Rider(station_3, station_2)
rider_6 = classes.Rider(station_3, station_4)

# rider_6.get_best_path_for_rider(graph_of_intersections)

for rider in classes.Rider.all_riders:
    rider.ride_from_to(rider.get_home_station(), rider.get_work_station())

print(classes.Intersection.all_intersections)

for rider in classes.Rider.all_riders:
    rider.ride_from_to(rider.get_work_station(), rider.get_home_station())

print(classes.Intersection.all_intersections)