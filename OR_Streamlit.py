import numpy as np
import streamlit as st
import plotly.graph_objects as go
import time
import ast  # To safely evaluate string input for coordinates

# Initialize session state for custom shape
if "custom_shape_coords" not in st.session_state:
    st.session_state.custom_shape_coords = None  # Stores the coordinates of the custom shape

# Define default shapes
scaling_factor = 4  # Scale down the shapes
shapes = {
    "Small Triangle": np.array([[2, 2], [8, 2], [5, 10]]) / scaling_factor,
    "Small Square": np.array([[12, 12], [18, 12], [18, 18], [12, 18]]) / scaling_factor,
    "Irregular 1": np.array([[0, 0], [10, -8], [15, 5], [5, 12]]) / scaling_factor,
    "Irregular 2": np.array([[-10, -10], [-15, -8], [-12, -2], [-5, -5]]) / scaling_factor,
    "Small Star": np.array([[0, 15], [4, 5], [10, 5], [6, -2], [8, -10],
                            [0, -5], [-8, -10], [-6, -2], [-10, 5], [-4, 5]]) / scaling_factor,
}

# Add custom shape from session state if it exists
if st.session_state.custom_shape_coords is not None:
    shapes["Custom Shape"] = np.array(st.session_state.custom_shape_coords)

# Sidebar Controls
st.sidebar.title("Controls")

# Add input for custom shape
st.sidebar.title("Custom Shape")
custom_shape_input = st.sidebar.text_area(
    "Enter Coordinates (e.g., [[1,1], [2,3], [3,1]]):",
    value="" if st.session_state.custom_shape_coords is None else str(st.session_state.custom_shape_coords),
)

# Button to update custom shape
if st.sidebar.button("Update Shape"):
    try:
        custom_shape_coords = ast.literal_eval(custom_shape_input)  # Safely evaluate input
        st.session_state.custom_shape_coords = custom_shape_coords  # Persist in session state
        shapes["Custom Shape"] = np.array(custom_shape_coords)
        st.sidebar.success("Custom shape updated successfully!")
    except (ValueError, SyntaxError):
        st.sidebar.error("Invalid input! Ensure the coordinates are in the correct format.")

# Rotation angle and direction
start_angle = st.sidebar.slider("Starting Rotation Angle (°)", 0, 360, 0)
start_angle_input = st.sidebar.text_input("Exact Starting Angle", value=str(start_angle))
end_angle = st.sidebar.slider("Ending Rotation Angle (°)", 0, 360, 360)
end_angle_input = st.sidebar.text_input("Exact Ending Angle", value=str(end_angle))
rotation_step = st.sidebar.slider("Rotation Step (°)", 1, 30, 5)
rotation_step_input = st.sidebar.text_input("Exact Step", value=str(rotation_step))

# Add dropdown for rotation direction
rotation_direction = st.sidebar.selectbox("Rotation Direction", ["Clockwise", "Anti-clockwise"])

# Adjust rotation direction
rotation_multiplier = -1 if rotation_direction == "Clockwise" else 1

# Translation vector
vector_x = st.sidebar.slider("Vector X", -30, 30, 0)
vector_x_input = st.sidebar.text_input("Exact Vector X", value=str(vector_x))
vector_y = st.sidebar.slider("Vector Y", -30, 30, 0)
vector_y_input = st.sidebar.text_input("Exact Vector Y", value=str(vector_y))
center_x = st.sidebar.slider("Center X", -10, 10, 0)
center_x_input = st.sidebar.text_input("Exact Center X", value=str(center_x))
center_y = st.sidebar.slider("Center Y", -10, 10, 0)
center_y_input = st.sidebar.text_input("Exact Center Y", value=str(center_y))

# Update values from text input boxes
try:
    start_angle = int(start_angle_input)
    end_angle = int(end_angle_input)
    rotation_step = int(rotation_step_input)
    vector_x = int(vector_x_input)
    vector_y = int(vector_y_input)
    center_x = int(center_x_input)
    center_y = int(center_y_input)
except ValueError:
    st.sidebar.error("Please enter valid integers in the input boxes.")

# Shape Visibility Checkboxes
shape_visibility = {}
for name in shapes.keys():
    shape_visibility[name] = st.sidebar.checkbox(f"Show {name}", value=True)

# Zoom Controls
st.sidebar.title("Zoom")
x_min = st.sidebar.slider("X-axis Min", -20, 0, -10)
x_max = st.sidebar.slider("X-axis Max", 0, 20, 10)
y_min = st.sidebar.slider("Y-axis Min", -20, 0, -10)
y_max = st.sidebar.slider("Y-axis Max", 0, 20, 10)

# Dynamic Animation Control
animate = st.sidebar.button("Start Animation")

# Function to rotate a shape
def rotate_shape(shape_coords, angle, center):
    angle_rad = np.radians(angle * rotation_multiplier)  # Adjust direction
    rotation_matrix = np.array([[np.cos(angle_rad), -np.sin(angle_rad)],
                                 [np.sin(angle_rad), np.cos(angle_rad)]])
    translated_coords = shape_coords - center
    rotated_coords = translated_coords @ rotation_matrix.T
    return rotated_coords + center

# Function to translate a shape
def translate_shape(shape_coords, vector):
    return shape_coords + vector

# Plot the shapes
def plot_shapes(angle, vector_x, vector_y, center_x, center_y):
    fig = go.Figure()

    # Add X and Y axes
    fig.add_trace(go.Scatter(x=[x_min, x_max], y=[0, 0],
                             mode="lines", name="X-Axis",
                             line=dict(color="black", dash="dash")))
    fig.add_trace(go.Scatter(x=[0, 0], y=[y_min, y_max],
                             mode="lines", name="Y-Axis",
                             line=dict(color="black", dash="dash")))

    # Add grid with discrete steps of 1
    fig.update_xaxes(
        tickmode="linear",
        tick0=0,
        dtick=1,
        range=[x_min, x_max],
        showgrid=True,
        gridcolor="lightgray",
    )
    fig.update_yaxes(
        tickmode="linear",
        tick0=0,
        dtick=1,
        range=[y_min, y_max],
        showgrid=True,
        gridcolor="lightgray",
    )

    # Plot each shape
    for name, shape in shapes.items():
        if shape_visibility[name]:
            translated_shape = translate_shape(shape, np.array([vector_x, vector_y]))
            rotated_shape = rotate_shape(translated_shape, angle, np.array([center_x, center_y]))
            x_coords, y_coords = rotated_shape[:, 0], rotated_shape[:, 1]
            fig.add_trace(go.Scatter(x=np.append(x_coords, x_coords[0]),
                                     y=np.append(y_coords, y_coords[0]),
                                     mode='lines', fill='toself',
                                     name=name,
                                     line=dict(color="blue"),
                                     fillcolor="rgba(0, 0, 255, 0.2)"))

    # Add center of rotation
    fig.add_trace(go.Scatter(x=[center_x], y=[center_y],
                             mode='markers', name="Center of Rotation",
                             marker=dict(size=10, color="red")))

    # Update layout
    fig.update_layout(
        plot_bgcolor="white",  # Set background to white
        dragmode='pan',
        template="plotly_white",
        height=700, width=700
    )

    return fig

# Display the plot
placeholder = st.empty()  # Placeholder to overwrite frames during animation
fig = plot_shapes(start_angle, vector_x, vector_y, center_x, center_y)
placeholder.plotly_chart(fig, use_container_width=True)

# Handle Animation
if animate:
    for angle in range(start_angle, end_angle + 1, rotation_step):  # Rotate smoothly between start and end angles
        fig = plot_shapes(angle, vector_x, vector_y, center_x, center_y)
        placeholder.plotly_chart(fig, use_container_width=True, key=f"rotation_{angle}")  # Add a unique key for each frame
        time.sleep(0.1)  # Pause for smooth animation
