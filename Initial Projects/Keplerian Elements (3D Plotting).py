# Project Four: 3D Orbital Elements Visualizer
# 5-27-26
# Truman Heaston

import numpy as np
import matplotlib.pyplot as plt

# Standard gravity constant
G0 = 9.80665 # m/s^2

def get_rotation_matrix(raan: float, inc: float, arg_per: float) -> np.ndarray:
    """Creates a 3D direction cosine rotation matrix using Euler angles in radians."""
    R = raan
    I = inc
    w = arg_per
    
    row1 = [
        np.cos(R)*np.cos(w) - np.sin(R)*np.sin(w)*np.cos(I),
        -np.cos(R)*np.sin(w) - np.sin(R)*np.cos(w)*np.cos(I),
        np.sin(R)*np.sin(I)
    ]
    row2 = [
        np.sin(R)*np.cos(w) + np.cos(R)*np.sin(w)*np.cos(I),
        -np.sin(R)*np.sin(w) + np.cos(R)*np.cos(w)*np.cos(I),
        -np.cos(R)*np.sin(I)
    ]
    row3 = [
        np.sin(w)*np.sin(I),
        np.cos(w)*np.sin(I),
        np.cos(I)
    ]
    return np.array([row1, row2, row3])


def generate_3d_orbit(a: float, e: float, raan_deg: float, inc_deg: float, arg_per_deg: float):
    """Generates X, Y, Z coordinates for a 3D orbit trajectory."""
    raan = np.radians(raan_deg)
    inc = np.radians(inc_deg)
    arg_per = np.radians(arg_per_deg)
    
    R_matrix = get_rotation_matrix(raan, inc, arg_per)
    nu_array = np.linspace(0, 2 * np.pi, 300) # Increased resolution for smooth rendering
    
    x_coords, y_coords, z_coords = [], [], []
    
    for nu in nu_array:
        r = (a * (1 - e**2)) / (1 + e * np.cos(nu))
        r_perifocal = np.array([r * np.cos(nu), r * np.sin(nu), 0.0])
        
        r_eci = np.dot(R_matrix, r_perifocal)
        
        x_coords.append(r_eci[0])
        y_coords.append(r_eci[1])
        z_coords.append(r_eci[2])
        
    return np.array(x_coords), np.array(y_coords), np.array(z_coords)


def main():
    # 1. Initialize the 3D Plotter Environment
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # 2. Define our Molniya Mission Profile parameters
    a = 26600.0       # Semi-major axis (km)
    e = 0.74          # Eccentricity 
    inc = 63.4        # Inclination (degrees)
    raan = 0.0        # RAAN (degrees)
    arg_per = 270.0   # Argument of Perigee (degrees)
    
    # 3. Process the 3D pipeline math
    x, y, z = generate_3d_orbit(a, e, raan, inc, arg_per)
    
    # 4. Draw a marker representing the center of the Earth at (0,0,0)
    ax.scatter(0, 0, 0, color='blue', s=200, label='Earth')
    
    # 5. Plot the 3D trajectory path curve
    ax.plot3D(x, y, z, color='red', linewidth=2, label='Molniya Orbit')
    
    # 6. Customize the 3D labels and layout bounds
    ax.set_title("3D Orbit Visualizer (Molniya Mission Profile)", fontsize=12, fontweight='bold')
    ax.set_xlabel("X Position (km)")
    ax.set_ylabel("Y Position (km)")
    ax.set_zlabel("Z Position (km)")
    
    # Equalizing the view scaling bounds so the orbit isn't stretched oddly
    max_bound = max(max(abs(x)), max(abs(y)), max(abs(z)))
    ax.set_xlim(-max_bound, max_bound)
    ax.set_ylim(-max_bound, max_bound)
    ax.set_zlim(-max_bound, max_bound)
    
    ax.legend()
    plt.show()

if __name__ == "__main__":
    main()
