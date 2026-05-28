#Mars Misson 
#5-27-2026
#Truman Heaston

import numpy as np 

#Gravitational constants (km^3/s^2)
MU_SUN = 1.32712440018e11
MU_EARTH = 3.986004418e5
MU_MARS = 4.282837e4

#Orbital radii
R_EARTH_ORBIT = 1.496e8  # km
R_MARS_ORBIT = 2.279e8    # km

def get_transfer_departure_velocity(mu_sun: float, r_earth: float, r_mars: float) -> float:
    """Calculate absolute departure velocity relative to the Sun for Hohmann transfer."""
    # We change this to return the absolute speed on the ellipse, NOT the difference
    v_transfer = np.sqrt(2 * mu_sun * r_mars / (r_earth * (r_earth + r_mars)))
    return v_transfer

def get_circular_velocity(mu: float, r: float) -> float:
    """Return circular orbital velocity for a body at radius r around central body with gravitational parameter mu."""
    return np.sqrt(mu / r)

def get_earth_escape_velocity(v_infinity: float, mu_earth: float, r_parking: float) -> float:
    """Calculates the absolute insertion velocity required at low Earth orbit perigee."""
    # This is the energy conservation equation (V_burn = sqrt(V_inf^2 + 2*mu/r))
    v_burn = np.sqrt(v_infinity**2 + (2 * mu_earth / r_parking))
    return v_burn
def calculate_launch_mass(m_dry: float, delta_v: float, isp: float) -> float:
    """Calculate the required launch mass using the Tsiolkovsky rocket equation."""
    G0 = 9.80665  # m/s^2
    v_e = isp * G0  # Effective exhaust velocity
    m_start = m_dry * np.exp(delta_v / v_e)  # Tsiolkovsky rocket equation
    return m_start
def main():
    print("=" * 60)
    print("INTERPLANETARY MISSION TO MARS")
    print("=" * 60)
    
    # 1. Calculate heliocentric velocities of Earth and Mars
    v_earth_sun = get_circular_velocity(MU_SUN, R_EARTH_ORBIT)
    v_mars_sun = get_circular_velocity(MU_SUN, R_MARS_ORBIT)

    print(f"Earth's orbital velocity around the Sun: {v_earth_sun:.2f} km/s")
    print(f"Mars' orbital velocity around the Sun:  {v_mars_sun:.2f} km/s")
    
    # 2. Get absolute departure speed relative to the Sun
    v_dep_sun = get_transfer_departure_velocity(MU_SUN, R_EARTH_ORBIT, R_MARS_ORBIT)
    print(f"Required Injection Velocity (Sun-relative): {v_dep_sun:.2f} km/s")
    
    # 3. Calculate V_infinity (excess velocity needed beyond Earth's orbital speed)
    v_infinity = v_dep_sun - v_earth_sun
    print(f"Required Hyperbolic Excess Velocity (V_inf): {v_infinity:.2f} km/s")
    
    # 4. Establish Earth Parking Orbit radius (6378 km Earth radius + 300 km altitude)
    r_parking = 6378.0 + 300.0
    
    # 5. Calculate the absolute velocity needed at engine burnout near Earth
    v_burn = get_earth_escape_velocity(v_infinity, MU_EARTH, r_parking)
    print(f"Required Injection Velocity from LEO (V_burn): {v_burn:.2f} km/s")
    
    # 6. Calculate the delta-V the rocket must provide 
    # (V_burn minus the orbital speed the satellite already has in its 300km LEO parking orbit)
    v_leo_circular = get_circular_velocity(MU_EARTH, r_parking)
    dv_injection_km_s = v_burn - v_leo_circular
    
    # Convert km/s to m/s for the rocket equation!
    dv_injection_m_s = dv_injection_km_s * 1000.0
    
    # 7. Mass Budget Calculation
    m_dry = 1000.0  # 1,000 kg satellite payload
    isp = 450.0     # Hydrolox upper stage efficiency (seconds)
    
    total_launch_mass = calculate_launch_mass(m_dry, dv_injection_m_s, isp)
    
    print("-" * 60)
    print(f"Injection Delta-V Required:             {dv_injection_km_s:.2f} km/s")
    print(f"Total Required Spacecraft Mass in LEO:  {total_launch_mass:.1f} kg")
    print("=" * 60)

if __name__ == "__main__":    main()
