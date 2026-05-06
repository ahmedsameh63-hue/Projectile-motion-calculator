import streamlit as st
import math
import matplotlib.pyplot as plt
import pandas as pd
# --- Helper Functions ---
def solve_quadratic(a, b, c):
    """Finds the total flight time using the quadratic formula."""
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return None
    elif discriminant == 0:
        return -b / (2*a)
    else:
        root1 = (-b + math.sqrt(discriminant)) / (2*a)
        root2 = (-b - math.sqrt(discriminant)) / (2*a)
        return max(root1, root2)

def to_rad(d):
    return math.radians(d)

# --- Main Program ---


st.title("PROJECTILE MOTION CALCULATOR")
# 1. Inputs
vi = st.number_input("Enter Initial Velocity (m/s): ", min_value=0.0, max_value = 100.0, value=20.0)
theta = st.number_input("Enter Angle (degrees): ", min_value=0.0, max_value=90.0, value=45.0 )
yi = st.number_input("Enter Initial Y-position (m): ", min_value=0.0, max_value=40.0, value=0.0)

gravity_options = {
    "mercury (3.7)": 3.7, "Earth (9.8)": 9.81, "venus (8.9)": 8.9, "mars (3.7)": 3.7, "jupiter (24.8)": 24.8,
    "saturn (10.4)": 10.4, "uranus (8.7)": 8.7, "neptune (11.2)": 11.2
}
choice = st.selectbox("Gravity Preset", options=list(gravity_options.keys()))
gravity = gravity_options[choice]

time_step = st.number_input("Enter Time Step for printout (s): ", min_value=0.00, max_value=100.0, value=0.5, step=0.01)
            

if st.button("Run simulation"):
    vx = vi * math.cos(to_rad(theta))
    vy_initial = vi * math.sin(to_rad(theta))
    total_flight_time = solve_quadratic(-0.5 * gravity, vy_initial, yi)
    if total_flight_time is None:
                    st.error("Error: Projectile does not return to ground.")
                    st.stop()

        # 3. PRINTING LOOP
        # format this as a nice table
        
    current_time = 0.0

    # Lists to store the points specifically for the user's chosen steps
    rows=[]
    user_x = []
    user_y = []

    while True:
        # Calculate positions
        x_pos = vx * current_time
        y_pos = yi + (vy_initial * current_time) - (0.5 * gravity * current_time**2)

        # Stop if we hit the ground
        if y_pos < 0:
            break

                # Add to lists
        user_x.append(x_pos)
        user_y.append(y_pos)

            # Print row in the table
        print(f"| {current_time:<10.2f} | {x_pos:<15.2f} | {y_pos:<15.2f} |")
        rows.append({"Time (s)": current_time, "X Position (m)": round(x_pos, 2), "Y Position (m)": round(y_pos, 2)})
        # Increment time
        current_time = round(current_time + time_step, 4)
    st.dataframe(pd.DataFrame(rows), use_container_width=True)

    print("-"*50 + "\n")

        # 4. Final Calculations

    max_range = vx * total_flight_time
    max_height = yi + (vy_initial**2) / (2 * gravity)
    vy_final = vy_initial - (gravity * total_flight_time)
    impact_v = math.sqrt(vx**2 + vy_final**2)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Flight Time", f"{total_flight_time:.2f} s")
    col2.metric("max range", f"{max_range:.2f} m")
    col3.metric("max height", f"{max_height:.2f} m")
    col4.metric("impact vilocity", f"{impact_v:.2f} m/s")

        # 5. GRAPHING
    print("\nGenerating Graph...")

    smooth_x = []
    smooth_y = []
    steps = 200
    dt_smooth = total_flight_time / steps

    for i in range(steps + 1):
        t = i * dt_smooth
        sx = vx * t
        sy = yi + (vy_initial * t) - (0.5 * gravity * t**2)
        smooth_x.append(sx)
        smooth_y.append(sy)

        # Plot Setup
        smooth_x, smooth_y = [], []
        smooth_x = []
    smooth_y = []
    for i in range(201):
        t = i * (total_flight_time / 200)
        smooth_x.append(vx * t)
        smooth_y.append(yi + (vy_initial * t) - (0.5 * gravity * t**2))

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')
    ax.plot(smooth_x, smooth_y, label='Trajectory', color='#0072B2', linewidth=2)
    ax.plot(user_x, user_y, 'ro', label='Measured Steps', markersize=5, color="#FF4B4B")
    ax.axhline(0, color='white', linewidth=2)
    ax.set_title(f"Projectile Motion (Angle: {theta}°, Vi: {vi}m/s)")
    ax.set_xlabel("Distance (X) meters")
    ax.set_ylabel("Height (Y) meters")
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    ax.grid(True, linestyle='--', color='#333333')
    for spine in ax.spines.values():
        spine.set_edgecolor('#333333')
    ax.legend()
    st.pyplot(fig)



