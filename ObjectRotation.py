import numpy as np
import matplotlib
matplotlib.use("TkAgg")  # Use Tkinter for interactivity
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.widgets import Slider, TextBox, CheckButtons

# Define a function to create the XoY axes
def draw_axes(ax):
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(color='gray', linestyle='--', linewidth=0.5)
    ax.set_xlim(-10, 10)  # Extend X-axis range
    ax.set_ylim(-10, 10)  # Extend Y-axis range
    ax.set_aspect('equal', adjustable='box')

    # Set integer ticks
    major_ticks = np.arange(-10, 10, 1)  # Integers from -60 to 60
    ax.set_xticks(major_ticks)
    ax.set_yticks(major_ticks)
    ax.xaxis.set_tick_params(labelsize=8)  # Smaller labels for better visibility
    ax.yaxis.set_tick_params(labelsize=8)



# Function to rotate a shape about a center of rotation
def rotate_shape(shape_coords, angle, center):
    """Rotates a shape (list of vertices) around a center by a given angle."""
    angle_rad = np.radians(angle)
    rotation_matrix = np.array([[np.cos(angle_rad), -np.sin(angle_rad)],
                                 [np.sin(angle_rad), np.cos(angle_rad)]])
    translated_coords = shape_coords - center
    rotated_coords = translated_coords @ rotation_matrix.T
    return rotated_coords + center

# Function to translate a shape by a vector
def translate_shape(shape_coords, vector):
    """Translates a shape by a given vector."""
    return shape_coords + vector

# Initial setup
fig, ax = plt.subplots(figsize=(16, 16))  # Increase the size of the figure
plt.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.35)  # Increase top and bottom margins
draw_axes(ax)

# Define shapes as lists of vertices, scaled down by a factor of 2
scaling_factor = 2

shapes = {
    "Small Triangle": np.array([[2, 2], [8, 2], [5, 10]]) / scaling_factor,
    "Small Square": np.array([[12, 12], [18, 12], [18, 18], [12, 18]]) / scaling_factor,
    "Irregular 1": np.array([[0, 0], [10, -8], [15, 5], [5, 12]]) / scaling_factor,
    "Irregular 2": np.array([[-10, -10], [-15, -8], [-12, -2], [-5, -5]]) / scaling_factor,
    "Small Star": np.array([[0, 15], [4, 5], [10, 5], [6, -2], [8, -10],
                            [0, -5], [-8, -10], [-6, -2], [-10, 5], [-4, 5]]) / scaling_factor,
}


# Define initial center of rotation and vector
center_of_rotation = np.array([0, 0])
translation_vector = np.array([0, 0])

# Plot initial shapes
polygons = {}
for name, shape in shapes.items():
    polygon = Polygon(shape, closed=True, fill=True, edgecolor='blue', alpha=0.5, label=name)
    ax.add_patch(polygon)
    polygons[name] = polygon

# Mark the center of rotation
center_point, = ax.plot(center_of_rotation[0], center_of_rotation[1], 'ro', label='Center of Rotation')

# Update the plot with rotation and translation
def update_plot(angle, center, vector, visible_shapes):
    for name, shape in shapes.items():
        if visible_shapes[name]:
            translated_shape = translate_shape(shape, vector)  # Apply the vector translation
            rotated_shape = rotate_shape(translated_shape, angle, center)  # Rotate around the center
            polygons[name].set_xy(rotated_shape)
            polygons[name].set_visible(True)
        else:
            polygons[name].set_visible(False)

    center_point.set_data(center[0], center[1])  # Keep the center fixed
    fig.canvas.draw_idle()

# Sliders for rotation angle, center of rotation, and translation vector
angle_slider_ax = plt.axes([0.2, 0.2, 0.55, 0.03], facecolor='lightgray')
angle_slider = Slider(angle_slider_ax, 'Angle', 0, 360, valinit=0)

vector_x_slider_ax = plt.axes([0.2, 0.15, 0.55, 0.03], facecolor='lightgray')
vector_x_slider = Slider(vector_x_slider_ax, 'Vector X', -30, 30, valinit=0)

vector_y_slider_ax = plt.axes([0.2, 0.1, 0.55, 0.03], facecolor='lightgray')
vector_y_slider = Slider(vector_y_slider_ax, 'Vector Y', -30, 30, valinit=0)

# Sliders for the center of rotation
rotation_x_slider_ax = plt.axes([0.2, 0.05, 0.55, 0.03], facecolor='lightgray')
rotation_x_slider = Slider(rotation_x_slider_ax, 'Center X', -10, 10, valinit=0)

rotation_y_slider_ax = plt.axes([0.2, 0.0, 0.55, 0.03], facecolor='lightgray')
rotation_y_slider = Slider(rotation_y_slider_ax, 'Center Y', -10, 10, valinit=0)

# Text boxes for exact input
angle_text_box_ax = plt.axes([0.77, 0.2, 0.1, 0.03])
angle_text_box = TextBox(angle_text_box_ax, '', initial="0")

vector_x_text_box_ax = plt.axes([0.77, 0.15, 0.1, 0.03])
vector_x_text_box = TextBox(vector_x_text_box_ax, '', initial="0")

vector_y_text_box_ax = plt.axes([0.77, 0.1, 0.1, 0.03])
vector_y_text_box = TextBox(vector_y_text_box_ax, '', initial="0")

rotation_x_text_box_ax = plt.axes([0.77, 0.05, 0.1, 0.03])  # Next to Center X slider
rotation_x_text_box = TextBox(rotation_x_text_box_ax, '', initial="0")

rotation_y_text_box_ax = plt.axes([0.77, 0.0, 0.1, 0.03])  # Next to Center Y slider
rotation_y_text_box = TextBox(rotation_y_text_box_ax, '', initial="0")


# Checkboxes for shape visibility
checkbox_ax = plt.axes([0.85, 0.5, 0.1, 0.3])
checkbox_labels = list(shapes.keys())
checkbox_status = [True] * len(checkbox_labels)
checkbox = CheckButtons(checkbox_ax, checkbox_labels, checkbox_status)

# Update function for sliders and text boxes
def on_slider_change(val):
    angle = angle_slider.val
    vector = np.array([vector_x_slider.val, vector_y_slider.val])
    center = np.array([rotation_x_slider.val, rotation_y_slider.val])  # Read center sliders
    visible_shapes = {name: status for name, status in zip(checkbox_labels, checkbox.get_status())}
    update_plot(angle, center, vector, visible_shapes)

def on_text_submit(text, target):
    try:
        value = float(text)
        if target == "angle":
            angle_slider.set_val(value)
        elif target == "vector_x":
            vector_x_slider.set_val(value)
        elif target == "vector_y":
            vector_y_slider.set_val(value)
        elif target == "center_x":
            rotation_x_slider.set_val(value)
        elif target == "center_y":
            rotation_y_slider.set_val(value)

        angle = angle_slider.val
        vector = np.array([vector_x_slider.val, vector_y_slider.val])
        center = np.array([rotation_x_slider.val, rotation_y_slider.val])
        visible_shapes = {name: status for name, status in zip(checkbox_labels, checkbox.get_status())}
        update_plot(angle, center, vector, visible_shapes)
    except ValueError:
        print(f"Invalid value for {target}!")
    except ValueError:
        print(f"Invalid value for {target}!")

# Connect text boxes to update functions
angle_text_box.on_submit(lambda text: on_text_submit(text, "angle"))
vector_x_text_box.on_submit(lambda text: on_text_submit(text, "vector_x"))
vector_y_text_box.on_submit(lambda text: on_text_submit(text, "vector_y"))

# Connect sliders and checkboxes to update function
angle_slider.on_changed(on_slider_change)
vector_x_slider.on_changed(on_slider_change)
vector_y_slider.on_changed(on_slider_change)
rotation_x_text_box.on_submit(lambda text: on_text_submit(text, "center_x"))
rotation_y_text_box.on_submit(lambda text: on_text_submit(text, "center_y"))


checkbox.on_clicked(lambda _: on_slider_change(None))

# Show the plot
plt.legend()
plt.show()
