import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
g = 9.81  # Acceleration due to gravity (m/s^2)
v0 = 20   # Initial velocity (m/s)
angle1 = 45  # Launch angle (degrees)
angle2 = 30
angle3 =60
t_max1 = 2 * v0 * np.sin(np.radians(angle1)) / g  # Total time of flight
t_max2 = 2 * v0 * np.sin(np.radians(angle2)) / g
t_max3 = 2 * v0 * np.sin(np.radians(angle3)) / g
dt = 0.01  # Time step

# Initial conditions
theta1 = np.radians(angle1)
v0x1 = v0 * np.cos(theta1)
v0y1 = v0 * np.sin(theta1)
theta2 = np.radians(angle2)
v0x2 = v0 * np.cos(theta2)
v0y2 = v0 * np.sin(theta2)
theta3 = np.radians(angle3)
v0x3 = v0 * np.cos(theta3)
v0y3 = v0 * np.sin(theta3)

# Time array
t1 = np.arange(0, t_max1, dt)
t2 = np.arange(0, t_max2, dt)
t3 = np.arange(0, t_max3, dt)

# Trajectory equations
x1 = v0x1 * t1
y1 = v0y1 * t1 - 0.5 * g * t1**2
x2 = v0x2 * t2
y2 = v0y2 * t2 - 0.5 * g * t2**2
x3 = v0x3 * t3
y3 = v0y3 * t3 - 0.5 * g * t3**2

# Set up the figure and axis
fig, ax = plt.subplots()
ax.set_xlim(0, max(np.max(x1), np.max(x2), np.max(x3)) * 1.1) # Adjusted x-limit
ax.set_ylim(0, max(np.max(y1), np.max(y2), np.max(y3)) * 1.1) # Adjusted y-limit
line1, = ax.plot([], [], 'b-', label=f"Angle = {angle1}°")
point1, = ax.plot([], [], 'bo')  # Point for the first projectile
line2, = ax.plot([], [], 'g-', label=f"Angle = {angle2}°")
point2, = ax.plot([], [], 'go')  # Point for the second projectile
line3, = ax.plot([], [], 'r-', label=f"Angle = {angle3}°")
point3, = ax.plot([], [], 'ro')  # Point for the third projectile
ax.legend()
ax.set_xlabel("Horizontal Distance (m)")
ax.set_ylabel("Vertical Distance (m)")
ax.set_title("Ballistic Motion by José Gonçalves (eufisica)")
             
# Initialization function
def init():
    line1.set_data([], [])
    point1.set_data([], [])
    line2.set_data([], [])
    point2.set_data([], [])
    line3.set_data([], [])
    point3.set_data([], [])
    return line1, point1, line2, point2, line3, point3

# Animation function
def update(frame):
    # Ensure frame doesn't exceed trajectory length for each line
    f1 = min(frame, len(t1) - 1)
    f2 = min(frame, len(t2) - 1)
    f3 = min(frame, len(t3) - 1)

    line1.set_data(x1[:f1], y1[:f1])
    point1.set_data([x1[f1]], [y1[f1]])
    line2.set_data(x2[:f2], y2[:f2])
    point2.set_data([x2[f2]], [y2[f2]])
    line3.set_data(x3[:f3], y3[:f3])
    point3.set_data([x3[f3]], [y3[f3]])
    return line1, point1, line2, point2, line3, point3


# Create the animation
max_frames = max(len(t1), len(t2), len(t3))
ani = FuncAnimation(fig, update, frames=max_frames, init_func=init, blit=True, interval=dt*1000)


# Show the animation
plt.show()
