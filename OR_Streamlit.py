import numpy as np
import streamlit as st
import plotly.graph_objects as go
import time

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
vector_x = st.sidebar.slider("Vector X", -30, 30, 0)
vector_y = st.sidebar.slider("Vector Y", -30, 30, 0)
center_x = st.sidebar.slider("Center X", -10, 10, 0)
center_y = st.sidebar.slider("Center Y", -10, 10, 0)

# Shape Visibility Checkboxes
shape_visibility = {}
for name in shapes.keys():
    shape_visibility[name] = st.sidebar.checkbox(f"Show {name}", value=True)

# Zoom Controls
st.sidebar.title("Zoom")
x_min = st.sidebar.slider("X-axis Min", -100, 0, -10)
x_max = st.sidebar.slider("X-axis Max", 0, 100, 10)
y_min = st.sidebar.slider("Y-axis Min", -100, 0, -10)
y_max = st.sidebar.slider("Y-axis Max", 0, 100, 10)

# Dynamic Animation Control
animate = st.sidebar.button("Start Animation")

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

# Initialize Plotly figure
fig = go.Figure()

# Plot the shapes
for name, shape in shapes.items():
    if shape_visibility[name]:
        translated_shape = translate_shape(shape, np.array([vector_x, vector_y]))
        rotated_shape = rotate_shape(translated_shape, angle, np.array([center_x, center_y]))
        x_coords, y_coords = rotated_shape[:, 0], rotated_shape[:, 1]
        fig.add_trace(go.Scatter(x=np.append(x_coords, x_coords[0]),
                                 y=np.append(y_coords, y_coords[0]),
                                 mode='lines+markers',
                                 name=name))

# Add center of rotation
fig.add_trace(go.Scatter(x=[center_x], y=[center_y],
                         mode='markers', name="Center of Rotation",
                         marker=dict(size=10, color="red")))

# Update layout for zooming and panning
fig.update_layout(
    xaxis=dict(range=[x_min, x_max]),
    yaxis=dict(range=[y_min, y_max]),
    dragmode='pan',  # Enables dragging for panning
    template="plotly_white",
    height=700, width=700
)

st.plotly_chart(fig, use_container_width=True)

# Handle Animation
if animate:
    for i in range(0, 361, 5):  # Rotate from 0 to 360 degrees in steps of 5
        angle = i
        fig = go.Figure()
        for name, shape in shapes.items():
            if shape_visibility[name]:
                translated_shape = translate_shape(shape, np.array([vector_x, vector_y]))
                rotated_shape = rotate_shape(translated_shape, angle, np.array([center_x, center_y]))
                x_coords, y_coords = rotated_shape[:, 0], rotated_shape[:, 1]
                fig.add_trace(go.Scatter(x=np.append(x_coords, x_coords[0]),
                                         y=np.append(y_coords, y_coords[0]),
                                         mode='lines+markers',
                                         name=name))
        fig.add_trace(go.Scatter(x=[center_x], y=[center_y],
                                 mode='markers', name="Center of Rotation",
                                 marker=dict(size=10, color="red")))
        fig.update_layout(
            xaxis=dict(range=[x_min, x_max]),
            yaxis=dict(range=[y_min, y_max]),
            dragmode='pan',
            template="plotly_white",
            height=700, width=700
        )
        st.plotly_chart(fig, use_container_width=True)
        time.sleep(0.1)  # Pause for smooth animation
