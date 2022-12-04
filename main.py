import scripts.classes as classes
import scripts.setup


station_1 = classes.Station(10, 2, 1, 1)
station_2 = classes.Station(20, 0, 10, 10)
station_3 = classes.Station(10, 0, 2, 8)
station_4 = classes.Station(15, 14, 10, 1)
station_5 = classes.Station(1, 1, 5, 5)
station_1.add_adjacent_intersection(station_5)
station_5.add_adjacent_intersection(station_2)
station_3.add_adjacent_intersection(station_2)
station_4.add_adjacent_intersection(station_2)
station_4.add_adjacent_intersection(station_1)
station_4.add_adjacent_intersection(station_5)

graph_of_intersections = classes.Intersection.get_graph_of_intersections()
classes.Station.draw_graph_of_intersections(graph_of_intersections)




rider_1 = classes.Rider(station_1, station_2)
rider_2 = classes.Rider(station_1, station_2)
rider_3 = classes.Rider(station_1, station_2)
rider_4 = classes.Rider(station_3, station_2)
rider_5 = classes.Rider(station_3, station_2)
rider_6 = classes.Rider(station_3, station_4)

def update_poisson_mean_function(n_simulations, prior_mean, change_in_value, learning_rate):
    return max(0, ((n_simulations - 1) * prior_mean + change_in_value * learning_rate) / n_simulations)

is_traveling_to_work = True
for simulation_index in range(1000):
    for rider in classes.Rider.all_riders:
        best_route_for_rider = rider.get_best_route(to_work = is_traveling_to_work)
        rider.ride_from_to(best_route_for_rider.walk_to_intersection, best_route_for_rider.walk_from_intersection)

    classes.Station.update_prior_mean_bonus_points_for_each_station(simulation_index + 1, update_poisson_mean_function)
    is_traveling_to_work = not is_traveling_to_work

for intersection in classes.Intersection.all_intersections:
    if intersection.is_station:
        print('intersection_id:' + str(intersection.intersection_id) + \
            ' drop_off_bonus_points_mean:' + str(intersection.drop_off_bonus_points_mean) + \
            ' pick_up_bonus_points_mean:' + str(intersection.pick_up_bonus_points_mean))