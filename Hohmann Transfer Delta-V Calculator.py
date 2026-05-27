"""
PROJECT 1: Hohmann Transfer Delta-V Calculator

Author: Truman Heaston 
Concept: Move a satellite from LEO to GEO using two engine burns.

WHAT IS A HOHMANN TRANSFER?
A Hohmann transfer is the most fuel-efficient way to move between two
circular orbits. It uses exactly two burns (delta-V maneuvers) and an
intermediate elliptical "transfer orbit" to bridge them.

"""

import math  




MU = 3.986004418e14    

R_EARTH = 6_371_000   



def vis_viva(r: float, a: float) -> float:
    """
    Calculate orbital velocity at radius r for an orbit with semi-major axis a.

    The Vis-Viva equation: v = sqrt( μ * (2/r - 1/a) )

    Args:
        r: Current distance from Earth's center [m]
        a: Semi-major axis of the orbit [m]

    Returns:
        Orbital velocity [m/s]
    """
    
    return math.sqrt(MU * (2/r - 1/a))




def transfer_sma(r1: float, r2: float) -> float:
    """
    Calculate the semi-major axis of a Hohmann transfer ellipse.

    Args:
        r1: Radius of the initial circular orbit [m]
        r2: Radius of the final circular orbit [m]

    Returns:
        Semi-major axis of the transfer ellipse [m]
    """
    return (r1 + r2) / 2




def transfer_time(a: float) -> float:
    """
    Calculate the time for a Hohmann transfer (half the ellipse's period).

    Kepler's Third Law: T_full = 2π * sqrt(a³/μ)
    Transfer = half period: t = π * sqrt(a³/μ)

    Args:
        a: Semi-major axis of the transfer ellipse [m]

    Returns:
        Transfer time [seconds]
    """
    return math.pi * math.sqrt(a**3 / MU)



def get_altitude_km(prompt: str) -> float:
    """
    Prompt the user for an altitude in km, validate it's a positive number.

    Args:
        prompt: The message to display to the user

    Returns:
        Altitude in kilometers (positive float)
    """
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("  ⚠  Altitude must be positive. Try again.")
                continue
            return value
        except ValueError:
            # float() raises ValueError if the string can't be converted
            print("  ⚠  Please enter a number (e.g., 400). Try again.")




def main():
    print("=" * 60)
    print("  HOHMANN TRANSFER DELTA-V CALCULATOR")
    print("  Orbital Mechanics Fundamentals — Project 1")
    print("=" * 60)
    print()

    

    alt1_km = get_altitude_km("Enter starting altitude (km) [e.g., 400 for ISS orbit]: ")
    alt2_km = get_altitude_km("Enter final altitude    (km) [e.g., 35786 for GEO]:    ")

    if alt2_km <= alt1_km:
        print("\n  ⚠  Final altitude must be HIGHER than starting altitude for a standard")
        print("     Hohmann transfer. Reverse the inputs if you want to deorbit.")
        print("     Exiting.")
        return

   
    r1 = (alt1_km * 1000) + R_EARTH   # [m] Initial orbit radius
    r2 = (alt2_km * 1000) + R_EARTH   # [m] Final orbit radius

  

    # 1. Velocity in the initial circular orbit (at r1)
    #    For a circle: a = r, so vis_viva(r1, r1) = sqrt(μ/r1)
    v1_circ = vis_viva(r1, r1)

    # 2. The transfer ellipse semi-major axis
    a_transfer = transfer_sma(r1, r2)

    # 3. Velocity at the PERIGEE (bottom) of the transfer ellipse
    #    We're AT r1, but now our orbit's semi-major axis is a_transfer
    v_transfer_perigee = vis_viva(r1, a_transfer)

    # 4. Velocity at the APOGEE (top) of the transfer ellipse
    #    We're AT r2, still on the transfer ellipse
    v_transfer_apogee = vis_viva(r2, a_transfer)

    # 5. Velocity in the final circular orbit (at r2)
    v2_circ = vis_viva(r2, r2)

    # Delta-V calculations:
    # Burn 1: 
    delta_v1 = v_transfer_perigee - v1_circ

    # Burn 2
    delta_v2 = v2_circ - v_transfer_apogee

    # Total delta-V
    delta_v_total = delta_v1 + delta_v2

    # Transfer time
    t_seconds = transfer_time(a_transfer)
    t_hours   = t_seconds / 3600



    print()
    print("=" * 60)
    print("  RESULTS")
    print("=" * 60)
    print(f"  Initial orbit altitude  : {alt1_km:>10,.1f} km")
    print(f"  Final orbit altitude    : {alt2_km:>10,.1f} km")
    print(f"  Transfer ellipse SMA    : {a_transfer/1000:>10,.1f} km")
    print()
    print(f"  Initial circular velocity  : {v1_circ:>8,.1f} m/s")
    print(f"  Transfer perigee velocity  : {v_transfer_perigee:>8,.1f} m/s")
    print(f"  Transfer apogee velocity   : {v_transfer_apogee:>8,.1f} m/s")
    print(f"  Final circular velocity    : {v2_circ:>8,.1f} m/s")
    print()
    print(f"  ΔV₁ (LEO → Transfer)    : {delta_v1:>8,.2f} m/s")
    print(f"  ΔV₂ (Transfer → GEO)    : {delta_v2:>8,.2f} m/s")
    print(f"  ─────────────────────────────────────")
    print(f"  Total ΔV Required       : {delta_v_total:>8,.2f} m/s")
    print()
    print(f"  Transfer Time           : {t_seconds:>8,.0f} s")
    print(f"                          : {t_hours:>8.2f} hours")
    print("=" * 60)

    
    print()
    print("  REFERENCE CHECK (for 400km → 35,786km):")
    print("  Expected total ΔV ≈ 3,893 m/s | Transfer time ≈ 5.26 hours")
    print()


if __name__ == "__main__":
    main()
