'''
Track four moons: Io, Europa, Ganymede and Callisto.

Each moon has a (x, y, and z) position and velocity (vel_x,vel_y,vel_z). 
The position of each moon is given; the velocity starts at 0.

Simulate the motion of the moons:
1. update the velocity of every moon by applying gravity. 
2. update the position of every moon by applying velocity. 
Time progresses by one step once all of the positions are updated.

Gravity:
consider every pair of moons. 
On each axis (x, y, and z), the velocity of each moon changes by exactly +1 or -1 to pull the moons together.
However, if the positions on a given axis are the same, the velocity on that axis does not change for that pair of moons.
Velocity:
Add the velocity of each moon to its own position

total energy = pot * kin. Pot= sum(abs(x,y,z)) Kin = sum(abs(vel_x,vel_y,vel_z))