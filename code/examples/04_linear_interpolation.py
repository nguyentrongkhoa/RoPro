import time                               # For accessing the current time
from linear_interpolation import *        # Custom python package for linear interpolation


# Here, we define four different keyframes.
# All keyframes must have the same number of dimensions. In this case, all four keyframes have three dimensions.
kf_1 = [0, 0, 0]
kf_2 = [1, 2, 3]
kf_3 = [1, 2, 3]
kf_4 = [2, 3, 4]

# We now put three keyframes in a list, starting with kf_1 and ending with kf_3
keyframes = [kf_1, kf_2, kf_3]

# Here we specify the time (in seconds) it takes to transition between keyframes.
# Since there are three keyframes in the list above, there can only be two (n_keyframes-1) time durations.
durations = [1, 2] # in seconds

# Here we create an object of class LinearInterpolation. This object is called <lin>
# This object provides all relevant functionality for linearly interpolating between the keyframes.
lin = LinearInterpolation(keyframes, durations)


# First, we plot the linear interpolation between the three keyframes.
print('n_keyframes:', lin.n_keyframes)
lin.plot()

# Now we add keyframe kf_4 at the beginning of the sequence and also at the end of the sequence.
lin.append(kf_4, 3)
lin.appfront(kf_4, 3)
print('n_keyframes:', lin.n_keyframes)
lin.plot()

# Here, we delete the very first keyframe (first -> index = 0).
lin.delete(0)
print('n_keyframes:', lin.n_keyframes)
lin.plot()

# Here, we delete the second keyframe of the new keyframe sequence (second -> index = 1).
lin.delete(1)
print('n_keyframes:', lin.n_keyframes)
lin.plot()

# Again, we add keyframe kf_4 at the beginning and of the end of the sequence.
lin.append(kf_4, 3)
lin.appfront(kf_4, 3)
print('n_keyframes:', lin.n_keyframes)
lin.plot()

lin.delete(lin.n_keyframes-1)
print('n_keyframes:', lin.n_keyframes)
lin.plot()



# The code below runs for exacly ten seconds.
# During this process, it prints out the corresponding interpolated values for the current time.

start_time = time.time()    # store the time the program started
max_time_duration = 10.     # amount of time this program will run

# the following code will run as long as 10 seconds are not over yet
while (time.time() - start_time < max_time_duration):

    # compute how long we are already in this loop
    time_in_loop = time.time() - start_time

    # get interpolated values from <lin> for the current point in time
    values = lin.get_values_for_time(time_in_loop)
    
    # print out interpolated values
    print('time:', time_in_loop, 'values:', values)

# - while