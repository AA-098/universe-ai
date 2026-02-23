import matplotlib
matplotlib.use("Agg")
# universe_explorer.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import wikipediaapi

# -----------------------------
# 1. Wikipedia setup
# -----------------------------
wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent='UniverseExplorer/1.0 (contact: your_email@example.com)'
)

def wiki_search(topic, chars=1000):
    """Fetch summary from Wikipedia"""
    page = wiki.page(topic)
    if page.exists():
        return page.summary[0:chars] + ("..." if len(page.summary) > chars else "")
    else:
        return f"No Wikipedia page found for '{topic}'."

# -----------------------------
# 2. Streamlit UI Setup
# -----------------------------
st.set_page_config(page_title="Universe Explorer", layout="wide")
st.title("🌌 Universe Explorer")
st.markdown("Explore the cosmos: from the Sun to galaxies, planets, moons, stars, and more!")

# Sidebar for categories
st.sidebar.header("Space Categories")
categories = ["The Sun", "Stars", "Galaxies", "Planets", "Moons", "Black Holes", "Nebulae", "Exoplanets"]
selected_category = st.sidebar.selectbox("Select a topic category:", categories)

# Sidebar search
st.sidebar.subheader("Or search any space topic")
search_topic = st.sidebar.text_input("Search Wikipedia:")

# -----------------------------
# 3. Predefined popular topics
# -----------------------------
topic_mapping = {
    "The Sun": "Sun",
    "Stars": "Star",
    "Galaxies": "Galaxy",
    "Planets": "Planet",
    "Moons": "Moon",
    "Black Holes": "Black hole",
    "Nebulae": "Nebula",
    "Exoplanets": "Exoplanet"
}

if selected_category:
    topic = topic_mapping[selected_category]
    st.subheader(f"🌟 {selected_category}")
    summary = wiki_search(topic, chars=1200)
    st.write(summary)

if search_topic:
    st.subheader(f"🔍 Search result for '{search_topic}'")
    summary = wiki_search(search_topic, chars=1200)
    st.write(summary)

# -----------------------------
# 4. Solar System Simulation
# -----------------------------
st.subheader("🪐 Solar System Simulation")

# Constants
G = 6.67430e-11
AU = 1.496e11
DAY = 86400

class CelestialBody:
    def __init__(self, name, mass, radius, position, velocity, color='blue'):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.color = color

    def compute_gravity(self, other):
        r_vec = other.position - self.position
        r_mag = np.linalg.norm(r_vec)
        force_mag = G * self.mass * other.mass / r_mag**2
        return force_mag * (r_vec / r_mag)

# Solar System bodies (fallback data)
colors = {"Sun":"yellow", "Mercury":"gray", "Venus":"orange", "Earth":"green",
          "Mars":"red", "Jupiter":"orange", "Saturn":"gold", "Uranus":"lightblue", "Neptune":"blue"}

planets_data = {
    "Sun": (1.989e30, 6.963e8, [0,0], [0,0]),
    "Mercury": (3.3e23, 2.44e6, [0.387*AU,0], [0,47870]),
    "Venus": (4.867e24, 6.052e6, [0.723*AU,0], [0,35020]),
    "Earth": (5.972e24, 6.371e6, [AU,0], [0,29780]),
    "Mars": (6.39e23, 3.389e6, [1.524*AU,0], [0,24070]),
    "Jupiter": (1.898e27, 7.149e7, [5.2*AU,0], [0,13070]),
    "Saturn": (5.683e26, 6.03e7, [9.58*AU,0], [0,9680]),
    "Uranus": (8.681e25, 2.536e7, [19.2*AU,0], [0,6800]),
    "Neptune": (1.024e26, 2.462e7, [30.05*AU,0], [0,5430])
}

bodies = []
for name, data in planets_data.items():
    mass, radius, pos, vel = data
    color = colors.get(name, "white")
    bodies.append(CelestialBody(name, mass, radius, pos, vel, color))

# Simulation parameters
dt = DAY
steps = 365
positions = {body.name: [] for body in bodies}

for _ in range(steps):
    forces = {body.name: np.zeros(2) for body in bodies}
    for i, body in enumerate(bodies):
        for j, other in enumerate(bodies):
            if i != j:
                forces[body.name] += body.compute_gravity(other)
    for body in bodies:
        acceleration = forces[body.name]/body.mass
        body.velocity += acceleration*dt
        body.position += body.velocity*dt
        positions[body.name].append(body.position.copy())

for key in positions:
    positions[key] = np.array(positions[key])

# Plot Solar System
fig, ax = plt.subplots(figsize=(7,7))
for body in bodies:
    ax.plot(positions[body.name][:,0]/AU, positions[body.name][:,1]/AU, color=body.color, label=body.name)
ax.scatter([0],[0], color='yellow', s=250, label='Sun')
ax.set_xlabel("X (AU)")
ax.set_ylabel("Y (AU)")
ax.set_title("Solar System Orbits")
ax.grid(True)
ax.set_aspect('equal')
ax.legend()

st.pyplot(fig)

