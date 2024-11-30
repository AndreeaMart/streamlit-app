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
angle = st.sidebar.slider("Rotation Angle (°)", 0, 360, 0, step=1)
vector_x = st.sidebar.slider("Vector X", -30, 30, 0)
vector_y = st.sidebar.slider("Vector Y", -30, 30, 0)
center_x = st.sidebar.slider("Center X", -10, 10, 0)
center_y = st.sidebar.slider("Center Y", -10, 10, 0)
animate = st.sidebar.checkbox("Animate Rotation", value=False)

# Zoom Controls
x_min = st.sidebar.slider("X-axis Min", -50, 0, -10)
x_max = st.sidebar.slider("X-axis Max", 0, 50, 10)
y_min = st.sidebar.slider("Y-axis Min", -50, 0, -10)
y_max = st.sidebar.slider("Y-axis Max", 0, 50, 10)

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

# Plot the shapes dynamically using Plotly
def plot_shapes(angle, vector, center):
    fig = go.Figure()

    # Add shapes
    for name, shape in shapes.items():
        if shape_visibility[name]:
            translated_shape = translate_shape(shape, np.array([vector[0], vector[1]]))
            rotated_shape = rotate_shape(translated_shape, angle, np.array([center[0], center[1]]))
            rotated_shape = np.vstack((rotated_shape, rotated_shape[0]))  # Close the shape
            fig.add_trace(go.Scatter(
                x=rotated_shape[:, 0],
                y=rotated_shape[:, 1],
                mode="lines",
                name=name,
                fill="toself"
            ))

    # Add center of rotation
    fig.add_trace(go.Scatter(
        x=[center[0]],
        y=[center[1]],
        mode="markers",
        name="Center of Rotation",
        marker=dict(size=10, color="red")
    ))

    # Set axes and grid
    fig.update_layout(
        xaxis=dict(range=[x_min, x_max], zeroline=True),
        yaxis=dict(range=[y_min, y_max], zeroline=True),
        title="Interactive Shape Transformation",
        showlegend=True,
        template="plotly_white"
    )
    return fig

# Animate if the checkbox is selected
if animate:
    for i in range(0, 360, 5):  # Animate through angles 0 to 360
        fig = plot_shapes(i, [vector_x, vector_y], [center_x, center_y])
        st.plotly_chart(fig, use_container_width=True)
        time.sleep(0.05)
else:
    # Static plot
    fig = plot_shapes(angle, [vector_x, vector_y], [center_x, center_y])
    st.plotly_chart(fig, use_container_width=True)
