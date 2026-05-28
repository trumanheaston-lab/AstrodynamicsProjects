#MatPlotLib for Hohmann Transfer Orbit Visualization
#5-27-2026
#Truman Heaston 

import math 
import matplotlib.pyplot as plt
import numpy as np 

#Constants (Earth centered inertial frame)
MU = 3.986004418e14    
R_EARTH = 6_371_000

#Defining the orbital radii 
def main(): 
    alt1_km = float(input("Enter starting altitude in km: "))
    alt2_km = float(input("Enter target altitude in km: "))

    r1 = alt1_km + (R_EARTH / 1000)  # Convert to km
    r2 = alt2_km + (R_EARTH / 1000)
    r_earth_km = R_EARTH / 1000

    a_transfer = (r1 + r2) / 2  # Semi-major axis of the transfer orbit
    eccentricity = (r2 - r1) / (r2 + r1)  # Eccentricity of the transfer orbit

    #Genrate 500 angles between 0 and 360 degrees or 0 and 2*pi radians
    theta_circular = np.linspace(0, 2 * math.pi, 500)

    #Map Leo Cords
    x_leo = r1 * np.cos(theta_circular)
    y_leo = r1 * np.sin(theta_circular)

    #Map Geo Cords
    x_geo = r2 * np.cos(theta_circular)
    y_geo = r2 * np.sin(theta_circular)

    #The Transfer Ellipse

    #Generate 250 angles (half a circle) 
    theta_transfer = np.linspace(0, math.pi, 250)
    #transfer orbit radius at each angle
    r_transfer = (a_transfer * (1 - eccentricity**2)) / (1 + eccentricity * np.cos(theta_transfer))
    #polar to cartesian coordinates for the transfer orbit
    x_transfer = r_transfer * np.cos(theta_transfer)
    y_transfer = r_transfer * np.sin(theta_transfer)

    #make the map
    plt.figure(figsize=(8, 8))

    #Plot Earth
    earth = plt.Circle((0, 0), r_earth_km, color='blue', alpha=0.5, label='Earth')
    plt.gca().add_patch(earth)

    #line vectors for the orbits
    plt.plot(x_leo, y_leo, label='LEO Orbit', color='green')
    plt.plot(x_geo, y_geo, label='GEO Orbit', color='orange')
    plt.plot(x_transfer, y_transfer, label='Hohmann Transfer Orbit', color='red')

    #Mark Burn 1 and 2 locations
    plt.scatter(x_transfer[0], y_transfer[0], color='red', marker='^', label='Burn 1')
    plt.scatter(x_transfer[-1], y_transfer[-1], color='darkred', marker='^', label='Burn 2')

    #force the aspect ratio to be equal so the orbits look circular
    plt.axis('equal')
    plt.title('Hohmann Transfer Orbit Visualization')
    plt.xlabel('X Position (km)')
    plt.ylabel('Y Position (km)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()

    plt.show()

if __name__ == "__main__":
    main()
    


