# nudge
## A simulation of riders in a bike sharing program. Aim is to determine the optimum number of points to award each rider for moving bikes to or from under and overused stations.


### Background

In my city, I use a public bike service. Bikes are docked at established stations throughout the city - about every four blocks or so, there is a station able to dockaround 20 bikes. Demand for bikes fluctuates throughout the day and week as workers ride from the outside of the city to the financial district, and as shoppers ride to parks and coffee shops on the weekends. This leads to certain stations being over and underused throughout the day.

To reduce certain stations being overused, riders are incentivies to return bikes from overused stations to underused stations by offering bonus membership points. These points can be accumulated over time and can be converted into real value once certain point thresholds are met. Sometimes the number of points offerd for returning the bike to a particular station is 1, sometimes it is 2. The more points offered, the more incentive riders have to move the bikes from overused stations to underused stations.

I was curious as to how the number of points offered to riders is determined in the app, and how stations attracting bonus points are selected. I wondered whether a self-calibrating algorithm would be able to increase or decrease the number of bonus points offered in order to maximise the reallocation of bikes, and which minimised the cost to the bike company.


#### Design

The program is of two parts:
- **The World:** Classes were created to represent the Riders, Stations, and Intersections of the real world. Methods were created to determine how a Rider might choose a route through this world - they would probably just choose the shortest route, but the rider might be encouraged to take an alternate route if the number of bonus points up for grabs is appealing.
- **The Experiment:** Given the world, the company that runs the bike sharing service must decide how many points to offer for drop off or pick up of bikes at their stations. This is the experiment:
  1. Propose a number of bonus points at each station to be awarded for drop off or pick up
  2. See how Riders react to the bonus points when the head to work and go back home each day - does it lead to congestion?
  3. Increase or decrease the number of bonus points on offer at each station to discourage congestion
  

### Differences With Existing Graph Search Problems

Existing shortest-path algorithms (such as Dijkstra's) do not work in this program. This is because the cost to a Rider to traverse the graph of Stations is dependent on whether they are on a bike or whether they are on foot. Not all Stations in the network will have bikes or docks available, meaning the Rider must walk around a bit before finding a bike and getting on their way. The Rider may elect to walk in the opposite direction to their target destination if it means that they can get on a bike sooner.

Additionally, bonus points have the potential encourage strange routing behaviour by Riders. Imagine an absurd World in which there are four stations arranged in a square: A, B, C, D. You are at A and wish to get to the opposite station, C. The shortest route is to ride directly to C. The longest route is to walk from A to B, take a bike from B to D and then walk from D to C. However, if the bike ride from B to D attracts a number of points for pick up and drop off, then the Rider may well choose this longer route over the shortest route (A to C directly).


### Method of Proposing Number of Bonus Points

A *Poisson distribution* of bonus points is modelled rather than a single estimate of bonus points:
1. Initially, all stations are assumed to offer an average of 1 bonus point for drop off and pick up. This doesn't meant that all stations offer 1 point exactly. Instead, at the very start of The Experiment, the number of points offered is sampled from a Poisson distribution of mean 1 - some stations will offer zero points, some will offer 1 or more.
2. Once all Riders have travelled to work, check the state of each Station: Penalise the station for issuing bonus points to Riders and reward the Station for achieving a balanced number of bikes finally docked there (aiming for 50% usage rate at each Station). A *Value* heuristic is calculated for each Station, combining these characteristices into a quantifiable number.
3. The change in the value of the Station in each simualtion feeds into the mean of the Poisson distribution using the following formula: $$\texttt{revisedMean} = \texttt{max}(0, ((\texttt{nSimulations} - 1) * \texttt{priorMean} + \texttt{changeInValue} * \texttt{learningRate}) / \texttt{nSimulations})$$
4. The *revisedMean* is then adopted as the new mean of a Poisson distribution. Per step 1, this distribution is re-sampled to determine the new number of bonus points offered, and the simulation continues.

This methodology will be improved over time.
