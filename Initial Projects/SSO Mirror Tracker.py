# SSO Mirror Tracker 
# 5-28-2026
# Truman Heaston 

import numpy as np
import matplotlib.pyplot as plt

MU_EARTH = 398600.4418  # km^3/s^2
R_EARTH = 6378.137      # km
J2 = 1.08262668e-3

# Target sun-synchronous orbit precession rate (Positive scalar value)
# 360 degrees (2*pi rad) / 365.2422 days in a year
OMEGA_DOT_TARGET = (2 * np.pi) / (365.2422 * 24 * 3600)  # rad/s

def get_sso_inclination(a):
    """Calculate the inclination for a sun-synchronous orbit given the semi-major axis."""
    # Classical J2 nodal regression equation solved directly for cos(i):
    # cos(i) = OMEGA_DOT_TARGET / (-1.5 * J2 * sqrt(MU_EARTH) * R_EARTH^2 / a^(7/2))
    denominator = -1.5 * J2 * np.sqrt(MU_EARTH) * (R_EARTH**2) / (a**3.5)
    cos_i = OMEGA_DOT_TARGET / denominator
    
    return np.arccos(cos_i)

def get_sso_orbit(a):
    """Calculate the orbital elements for a sun-synchronous orbit given the semi-major axis."""
    i = get_sso_inclination(a)
    return {
        'semi_major_axis': a,
        'inclination': np.degrees(i),  # Storing in degrees for easier tracking
        'eccentricity': 0.0,
        'argument_of_perigee': 0.0,
        'right_ascension_of_ascending_node': 0.0,
        'true_anomaly': 0.0
    }

def generate_sso_trajectory(orbit_dict, points=200):
    """Generates the 3D ECI Coordinates for a full circular SSO orbit."""
    a = orbit_dict['semi_major_axis']
    inc = np.radians(orbit_dict['inclination'])
    omega = np.radians(orbit_dict['argument_of_perigee'])
    raan = np.radians(orbit_dict['right_ascension_of_ascending_node'])
    
    # Create true anomaly array for a full orbit
    nu_values = np.linspace(0, 2 * np.pi, points)

    x_eci = []
    y_eci = []
    z_eci = []

    for nu in nu_values:
        # Position in perifocal plane where r = a for circular orbit
        p = a * np.cos(nu)
        q = a * np.sin(nu)

        # Apply rotation to ECI using Direction Cosine Matrix (DCM)
        x = (np.cos(raan) * np.cos(omega) - np.sin(raan) * np.sin(omega) * np.cos(inc)) * p + \
            (-np.cos(raan) * np.sin(omega) - np.sin(raan) * np.cos(omega) * np.cos(inc)) * q
        y = (np.sin(raan) * np.cos(omega) + np.cos(raan) * np.sin(omega) * np.cos(inc)) * p + \
            (-np.sin(raan) * np.sin(omega) + np.cos(raan) * np.cos(omega) * np.cos(inc)) * q
        z = (np.sin(omega) * np.sin(inc)) * p + (np.cos(omega) * np.sin(inc)) * q

        x_eci.append(x)
        y_eci.append(y)
        z_eci.append(z)

    return np.array(x_eci), np.array(y_eci), np.array(z_eci)

def main():
    print("=" * 60)
    print(" REFLECT ORBITAL: SSO MIRROR TRACKER ".center(60, "="))
    print("=" * 60)

    test_altitude = 500.0  # km
    semi_major_axis = R_EARTH + test_altitude
    
    my_orbit = get_sso_orbit(semi_major_axis)
    x_eci, y_eci, z_eci = generate_sso_trajectory(my_orbit)

    print(f"Calculated inclination for SSO at {test_altitude} km altitude: {my_orbit['inclination']:.2f} degrees")
    print("Generating 3D Visualization...")

    # Calculate orbital period in seconds, then convert to minutes
    period_seconds = 2 * np.pi * np.sqrt(semi_major_axis**3 / MU_EARTH)
    period_minutes = period_seconds / 60.0
    
    print(f"Orbital Period: {period_minutes:.2f} minutes")
    print(f"Passes around Earth per day: {24 * 60 / period_minutes:.1f}")

    # 1. Create a 3D figure canvas
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # 2. Plot the 3D Satellite Trajectory Line
    ax.plot(x_eci, y_eci, z_eci, color='gold', linewidth=2.5, label='SSO Mirror Satellite Path')

    # Plot a marker showing the initial placement
    ax.scatter(x_eci[0], y_eci[0], z_eci[0], color='red', s=50, label='Initial Position')

    # 3. Create a basic wireframe sphere to represent Earth
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 30)
    x_earth = R_EARTH * np.outer(np.cos(u), np.sin(v))
    y_earth = R_EARTH * np.outer(np.sin(u), np.sin(v))
    z_earth = R_EARTH * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_wireframe(x_earth, y_earth, z_earth, color='royalblue', alpha=0.3, linewidth=0.5)

    # 4. Label the Axes (ECI frame alignment)
    ax.set_xlabel('X (ECI Frame - km)')
    ax.set_ylabel('Y (ECI Frame - km)')
    ax.set_zlabel('Z (ECI Frame - km)')
    ax.set_title(f"Sun-Synchronous Orbit Profile\nAltitude: {test_altitude} km | Inclination: {my_orbit['inclination']:.2f}°")
    
    # 5. Force aspect ratio scaling so Earth looks like a sphere, not a potato
    max_range = semi_major_axis * 1.2
    ax.set_xlim([-max_range, max_range])
    ax.set_ylim([-max_range, max_range])
    ax.set_zlim([-max_range, max_range])
    ax.legend()

    # 6. Show the interactive window
    plt.show()

if __name__ == "__main__":
    main()
