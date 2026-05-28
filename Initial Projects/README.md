

A collection of custom Python scripts tracking my progression through foundational orbital mechanics, 3D coordinate transformations, and interplanetary mission architecture. This suite transitions from baseline 2D orbital profiles to a full patched conics trajectory simulation from Earth to Mars.

## Project Structure

The repository is organized chronologically as the math scaled in complexity:

* **`Hohmann Transfer Delta-V Calculator.py`**
Calculates the fundamental velocity shifts ($\Delta V$) required to transition a spacecraft between two coplanar, circular orbits using a standard two-burn Hohmann transfer.
* **`Spacecraft Mass Budgeting.py`**
Implements the Tsiolkovsky Rocket Equation to map velocity requirements to actual physical hardware. Tracks wet mass versus dry mass scaling based on engine specific impulse ($I_{sp}$) to build realistic propellant profiles.
* **`Matplotlib for Hohmann Transfer Orbit Visualization.py`**
Translates the mathematical state vectors into visual data. Generates 2D orbital plots mapping the departure orbit, the elliptical transfer highway, and the target destination orbit.
* **`Keplerian Elements (3D Plotting).py`**
Transitions simulations from 2D planes into 3D space. Implements directional rotation matrices utilizing the core Keplerian orbital elements: Inclination ($i$), Right Ascension of the Ascending Node ($\Omega$), and Argument of Perigee ($\omega$). Transforms flat perifocal vectors into Earth-Centered Inertial (ECI) 3D coordinate space.
* **`Mars Mission.py` (Capstone)**
An interplanetary mission architecture script utilizing the **Patched Conics Method**. It links separate gravitational frames of reference (Sun-centered and Earth-centered) to calculate the precise Hyperbolic Excess Velocity ($V_{\infty}$) and the required insertion velocity ($V_{burn}$) at Low Earth Orbit perigee to escape Earth and reach Mars.

---

## Core Astrodynamics Core Concepts Implemented

### 1. The Vis-Viva Equation

To calculate absolute velocities along non-circular elliptical paths relative to a primary body:


$$V = \sqrt{\mu \left(\frac{2}{r} - \frac{1}{a}\right)}$$

### 2. Coordinate Transformations (3D Matrix Rotations)

Transforming coordinates from the local orbital plane (Perifocal) to the true equatorial inertial framework (ECI) via a sequence of three principal rotations:


$$R_z(\Omega) \cdot R_x(i) \cdot R_z(\omega)$$

### 3. The Oberth Effect

Leveraging conservation of kinetic energy deep within a planetary gravity well to minimize the required upper-stage engine burn times during hyperbolic escape maneuvers:


$$V_{burn} = \sqrt{V_{\infty}^2 + \frac{2\mu_{earth}}{r_{parking}}}$$

---

## Technical Stack & Environment

* **Language:** Python 3.x
* **Primary Libraries:** `numpy` (vectorized math operations, matrix transformations), `matplotlib` (2D/3D coordinate plotting)
* **Reference Frames Modeled:** Perifocal ($P-Q$), Earth-Centered Inertial ($ECI$), Heliocentric Inertial.

