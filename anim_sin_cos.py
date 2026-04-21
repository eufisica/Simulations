import matplotlib.pyplot as plt
from math import sin, cos, radians
import matplotlib.animation as animation

# Create a string with spaces proportional to a cosine of x in degrees
def make_dot_string(x):
    return ' ' * int(20 * cos(radians(x)) + 20) + 'o'
    return ' ' * int(20 * sin(radians(x)) + 20) + 'x'

# Generate x and y values
x_values = range(0, 1800, 12)
y_values = [cos(radians(x)) for x in x_values]
z_values = [sin(radians(x)) for x in x_values]

# Create a new figure and axes
fig, ax = plt.subplots()

# Animation function
def animate(i):
    ax.clear()  # Clear previous frame
    x = x_values[:i]
    y = y_values[:i]
    z = z_values[:i]
    ax.plot(x, y, 'o', label='Cosine')
    ax.plot(x, z, 'x', label='Sine')
    ax.set_xlabel('x')
    ax.set_ylabel('Cosine and Sin of x')
    ax.set_title('Cosine and Sine Graph')
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

# Create animation
ani = animation.FuncAnimation(fig, animate, frames=len(x_values), interval=50, repeat=False)

# Display the animation
plt.show()
