import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# Define shapes
scaling_factor = 2
shapes = {
    "Small Triangle": np.array([[2, 2], [8, 2], [5, 10]]) / scaling_factor,
    "Small Square": np.array([[12, 12], [18, 12], [18, 18], [12, 18]]) / scaling_factor,
    "Irregular 1": np.array([[0, 0], [10, -8], [15, 5], [5, 12]]) / scaling_factor,
    "Irregular 2": np.array([[-10, -10], [-15, -8], [-12, -2], [-5, -5]]) / scaling_factor,
    "Small Star": np.array([[0, 15], [4, 5], [10, 5], [6, -2], [8, -10],
                            [0, -5], [-8, -10], [-6, -2], [-10, 5], [-4, 5]]) / scaling_factor,
}

# Sidebar Controls
st.sidebar.title("Controls")

# Rotation angle
angle = st.sidebar.slider("Rotation Angle (°)", 0, 360, 0)
angle_input = st.sidebar.text_input("Exact Angle", value=str(angle))

# Vector X
vector_x = st.sidebar.slider("Vector X", -30, 30, 0)
vector_x_input = st.sidebar.text_input("Exact Vector X", value=str(vector_x))

# Vector Y
vector_y = st.sidebar.slider("Vector Y", -30, 30, 0)
vector_y_input = st.sidebar.text_input("Exact Vector Y", value=str(vector_y))

# Center X
center_x = st.sidebar.slider("Center X", -10, 10, 0)
center_x_input = st.sidebar.text_input("Exact Center X", value=str(center_x))

# Center Y
center_y = st.sidebar.slider("Center Y", -10, 10, 0)
center_y_input = st.sidebar.text_input("Exact Center Y", value=str(center_y))

# Update slider values if exact inputs are modified
try:
    angle = int(angle_input)
    vector_x = int(vector_x_input)
    vector_y = int(vector_y_input)
    center_x = int(center_x_input)
    center_y = int(center_y_input)
except ValueError:
    st.sidebar.error("Please enter valid integers for the exact values.")

# Zoom Controls
st.sidebar.title("Zoom")
x_min = st.sidebar.slider("X-axis Min", -100, 0, -10)
x_max = st.sidebar.slider("X-axis Max", 0, 100, 10)
y_min = st.sidebar.slider("Y-axis Min", -100, 0, -10)
y_max = st.sidebar.slider("Y-axis Max", 0, 100, 10)

# Shape Visibility Checkboxes
shape_visibility = {}
for name in shapes.keys():
    shape_visibility[name] = st.sidebar.checkbox(f"Show {name}", value=True)

# Function to rotate a shape
def rotate_shape(shape_coords, angle, center):
    angle_rad = np.radians(angle)
    rotation_matrix = np.array([[np.cos(angle_rad), -np.sin(angle_rad)],
                                 [np.sin(angle_rad), np.cos(angle_rad)]])
    translated_coords = shape_coords - center
    rotated_coords = translated_coords @ rotation_matrix.T
    return rotated_coords + center

# Function to translate a shape
def translate_shape(shape_coords, vector):
    return shape_coords + vector

# Plot the shapes
fig, ax = plt.subplots(figsize=(8, 8))
ax.axhline(0, color="black", linewidth=0.5)
ax.axvline(0, color="black", linewidth=0.5)
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_aspect("equal")
ax.grid(color="gray", linestyle="--", linewidth=0.5)

for name, shape in shapes.items():
    if shape_visibility[name]:
        translated_shape = translate_shape(shape, np.array([vector_x, vector_y]))
        rotated_shape = rotate_shape(translated_shape, angle, np.array([center_x, center_y]))
        polygon = Polygon(rotated_shape, closed=True, fill=True, edgecolor="blue", alpha=0.5)
        ax.add_patch(polygon)

# Plot center of rotation
ax.plot(center_x, center_y, "ro", label="Center of Rotation")
ax.legend()

# Display the plot in Streamlit
st.pyplot(fig)
