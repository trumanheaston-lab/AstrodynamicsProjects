# Budgeting Project
# 5-27-26
# Truman Heaston

import math 

# Standard gravity constant used in aerospace engineering
G0 = 9.80665 # m/s^2

def get_positive_float(prompt: str) -> float:
    """Repeatedly prompts the user for a number until they enter a valid positive float."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("  ⚠  Value must be greater than zero. Try again.")
                continue
            return value
        except ValueError:
            print("  ⚠  Invalid input. Please enter a valid numerical value.")

def calculate_final_mass(m_start: float, delta_v: float, Isp: float) -> float:
    """
    Calculate the final mass of a spacecraft after a maneuver using the Tsiolkovsky rocket equation.

    Parameters:
    m_start (float): Initial mass of the spacecraft (kg)
    delta_v (float): Required change in velocity (m/s)
    Isp (float): Specific impulse of the engine (s)

    Returns:
    float: Final mass of the spacecraft after the maneuver (kg)
    """
    # Calculate the effective exhaust velocity
    v_e = Isp * G0
    
    # Calculate the final mass using the Tsiolkovsky rocket equation
    m_final = m_start / math.exp(delta_v / v_e)
    
    return m_final


def main():
    print("=" * 50)
    print("       SPACECRAFT MASS BUDGET SIMULATION")
    print("=" * 50)
    print("Please input the mission profile details below:")
    print("-" * 50)
    
    # 1. Establish Initial Conditions interactively
    starting_mass = get_positive_float("Enter starting satellite wet mass (kg): ")
    print(f" -> Baseline Wet Mass Confirmed: {starting_mass:.1f} kg\n")
    
    # 2. MANEUVER 1: LEO Injection Burn
    print("--- MANEUVER 1 CONFIGURATION ---")
    dv1 = get_positive_float("Enter Burn 1 Delta-V (m/s) [e.g., 2400]: ")
    isp1 = get_positive_float("Enter Burn 1 Engine Isp (s)  [e.g., 310]: ")
    
    mass_after_burn1 = calculate_final_mass(starting_mass, dv1, isp1)
    fuel_burned1 = starting_mass - mass_after_burn1
    
    print("\nExecuting Burn 1 (LEO Injection):")
    print(f"  -> Propellant consumed: {fuel_burned1:.1f} kg")
    print(f"  -> Current vehicle mass: {mass_after_burn1:.1f} kg\n")
    
    # 3. MANEUVER 2: GEO Circularization Burn
    print("--- MANEUVER 2 CONFIGURATION ---")
    dv2 = get_positive_float("Enter Burn 2 Delta-V (m/s) [e.g., 1493]: ")
    isp2 = get_positive_float("Enter Burn 2 Engine Isp (s)  [e.g., 450]: ")
    
    mass_after_burn2 = calculate_final_mass(mass_after_burn1, dv2, isp2)
    fuel_burned2 = mass_after_burn1 - mass_after_burn2
    
    print("\nExecuting Burn 2 (GEO Circularization):")
    print(f"  -> Propellant consumed: {fuel_burned2:.1f} kg")
    print(f"  -> Current vehicle mass: {mass_after_burn2:.1f} kg\n")
    
    # 4. MANEUVER 3: GEO Station-Keeping Burn
    print("--- MANEUVER 3 CONFIGURATION ---")
    dv3 = get_positive_float("Enter Burn 3 Delta-V (m/s) [e.g., 200]: ")
    isp3 = get_positive_float("Enter Burn 3 Engine Isp (s)  [e.g., 3000]: ")
    
    final_dry_mass = calculate_final_mass(mass_after_burn2, dv3, isp3)
    fuel_burned3 = mass_after_burn2 - final_dry_mass
    
    print("\nExecuting Burn 3 (GEO Station-Keeping):")
    print(f"  -> Propellant consumed: {fuel_burned3:.1f} kg")
    print(f"  -> Current vehicle mass: {final_dry_mass:.1f} kg\n")
    
    # 5. Final Mission Summary
    total_fuel_burned = starting_mass - final_dry_mass
    print("=" * 50)
    print("MISSION SUMMARY:")
    print(f"  Final Satellite Dry Mass in GEO : {final_dry_mass:.1f} kg")
    print(f"  Total Propellant Consumed       : {total_fuel_burned:.1f} kg")
    print("=" * 50)


if __name__ == "__main__":
    main()
