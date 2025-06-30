from linear_interpolation import *


kf1 = [100, 150, 80, 90, 200]
kf2 = [200, 170, 80, 70, 150]
kf3 = [220, 150, 60, 20, 50]

keyframes = [kf1, kf2, kf3]
durations = [5, 2]


lin = LinearInterpolation(keyframes, durations)


interpolated = lin.get_values_for_time(2.5)

print(interpolated)


lin.plot()


