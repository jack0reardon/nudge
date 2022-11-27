# nudge
### An algorithm which proposes how much to award people in an economy in order to optimise behaviour

#### Background

In my city, I use a public bike service. Bikes are docked at established locations throughout the city - about every four or so blocks, there is a dock capable of holding around 20 bikes. Demand for bikes fluctuates throughout the day and week as workers ride from the outside of the city to the financial district, and as shoppers ride to parks and coffee shops on the weekends. This leads to certain docks becoming full of bikes, and others being ghosted.

The public bike service that I use incentivises riders to return bikes from overused docks to underused docks by offering bike points. These points can be accumulated over time and are converted into real value once certain point thresholds are met. Sometimes the number of points offerd is 1, sometimes it is 2. The more points offered, the more incentive riders would have to move the bikes from overused docks to underused docks.

I was curious as to how the number of point offered is determined in the app, and how docks which attract bonus points are selected. I wondered whether a self-calibrating algorithm would be capable of increasing or decreasing the number of bonus points offered in order to maximise the reallocation of bikes, but which 


#### Thought process

- *AI Game Simulations:* I'm reminded of a demonstration that my computer science lecturer showed us once. It was a simple computer game - a player moving up, down, left, or right in a small grid. Their goal was to reach the exit gate in the shortest time. They should avoid landing on the square with the teleporter, since that would teleport them further away from the exit gate. But only the Architect knows this, the AI player is blind, and has no idea of the reward of the exit gate or the effects of the teleporter. The lecturer then shows that we can simply let the player walk randomly through the grid to see the effect. Each trip through the grid ends when they reach the exit gate, and with each trip, the player knows how long it took them to reach the end (there is a length to the trip), and each square in the grid can be assigned a cost. The cost of a square increases each time the route that uses that square is long, and the cost reduces each time the route is short. After one thousand walks, the player learns the shortest path through the grid - the one which avoids the teleporter, beelining for the exit gate.

  There are two aspects of this example which are relevant to the current: 1) How the 'cost' of each square is updated, and 2) That simulations are run in order to determine the optimal cost of each square.
 
- **The [Beta Distribution](https://en.wikipedia.org/wiki/Beta_distribution):** This distribution can be interpreted as being a way to estimate the a probability or a rate. Suppose we want to estimate the likelihood of encountering a rotten egg. We start by cracking one - it's not rotten. With this one data point, our best estimate of the probability of encountering a rotten egg is 0%. We crack another one - it's also not rotten. With these two data points, it's still a best estimate of 0% likelihood of ecountering a rotten egg, but this estimate is bolstered by two data points. Eventually, after nine normal eggs, we crack a rotten egg. The new best estimate is now 10%. The mean of the Beta Distribution reflects this idea (it the number of positive encounters divided by the total number of encounters).

  The Beta Distribution provides some variance around this estimate - we've cracked just 10 eggs after all, and the true underlying likelihood of encountering a rotten egg is most probably not 10%! The variance should reduce (the beta distribution should become pointier) as more and more eggs are cracked - the more eggs we crack, the more evidence we have pointing towards a strong best estimate of the true underlying likelihood.

  This is of course the same idea as formulated by Beysian statistics, but the example above and the reference to a concrete distrubution with variance I think is more useful than focussing just on the best estimate!

- **Pre-Existing Algorithms:** An algorithm of this kind must already exist (eg. in Operations Research), but I restrained from researching whether there was one initially so that I could immerse myself into the problem fully before relying on someone else's solution. 
