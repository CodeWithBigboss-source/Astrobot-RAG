import requests
import pandas as pd
import json
import os
from tqdm import tqdm

NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")

SOLAR_SYSTEM_DATA = [
    {"name": "Mercury", "type": "Terrestrial", "mass": 0.330, "radius": 2439.7,
     "distance_from_sun": 57.9, "orbital_period": 88.0, "moons": 0,
     "description": "Mercury is the smallest planet in our solar system and closest to the Sun. It has no atmosphere and extreme temperature swings ranging from -180 to 430 degrees Celsius. Mercury completes one orbit around the Sun every 88 Earth days."},
    {"name": "Venus", "type": "Terrestrial", "mass": 4.867, "radius": 6051.8,
     "distance_from_sun": 108.2, "orbital_period": 224.7, "moons": 0,
     "description": "Venus is the second planet from the Sun and the hottest planet at 465 degrees Celsius due to a thick CO2 atmosphere causing a runaway greenhouse effect. A day on Venus is longer than its year."},
    {"name": "Earth", "type": "Terrestrial", "mass": 5.972, "radius": 6371.0,
     "distance_from_sun": 149.6, "orbital_period": 365.25, "moons": 1,
     "description": "Earth is the third planet from the Sun and the only known planet to harbor life. It has a protective magnetic field, liquid water on the surface, and an atmosphere rich in nitrogen and oxygen."},
    {"name": "Mars", "type": "Terrestrial", "mass": 0.642, "radius": 3389.5,
     "distance_from_sun": 227.9, "orbital_period": 687.0, "moons": 2,
     "description": "Mars is the fourth planet from the Sun known as the Red Planet due to iron oxide on its surface. It has the largest volcano in the solar system, Olympus Mons, and a canyon system, Valles Marineris. Mars has two small moons: Phobos and Deimos."},
    {"name": "Jupiter", "type": "Gas Giant", "mass": 1898.0, "radius": 69911.0,
     "distance_from_sun": 778.5, "orbital_period": 4331.0, "moons": 95,
     "description": "Jupiter is the fifth planet from the Sun and the largest planet in our solar system. Its Great Red Spot is a storm larger than Earth that has persisted for centuries. Jupiter has at least 95 known moons including the four large Galilean moons: Io, Europa, Ganymede, and Callisto."},
    {"name": "Saturn", "type": "Gas Giant", "mass": 568.0, "radius": 58232.0,
     "distance_from_sun": 1432.0, "orbital_period": 10747.0, "moons": 146,
     "description": "Saturn is the sixth planet from the Sun and is famous for its stunning ring system made of ice and rock. It is the least dense planet and could float on water. Saturn has 146 known moons including Titan which has a thick atmosphere and liquid methane lakes."},
    {"name": "Uranus", "type": "Ice Giant", "mass": 86.8, "radius": 25362.0,
     "distance_from_sun": 2867.0, "orbital_period": 30589.0, "moons": 28,
     "description": "Uranus is the seventh planet from the Sun and rotates on its side with an axial tilt of 98 degrees. It is an ice giant with a cold atmosphere of hydrogen, helium, and methane. The methane absorbs red light giving Uranus its blue-green color."},
    {"name": "Neptune", "type": "Ice Giant", "mass": 102.0, "radius": 24622.0,
     "distance_from_sun": 4515.0, "orbital_period": 59800.0, "moons": 16,
     "description": "Neptune is the eighth and farthest known planet from the Sun. It has the strongest winds in the solar system reaching 2100 km/h. Neptune has a large storm called the Great Dark Spot and its largest moon Triton orbits in the opposite direction to the planet's rotation."},
]

NASA_MISSIONS_DATA = [
    {"name": "James Webb Space Telescope", "launch_date": "2021-12-25", "status": "Active",
     "target": "Deep Space / Early Universe", "agency": "NASA/ESA/CSA",
     "description": "The James Webb Space Telescope is the most powerful space telescope ever built. It observes in infrared light and can see the first galaxies formed after the Big Bang, peer into dusty stellar nurseries, and study the atmospheres of exoplanets for signs of habitability."},
    {"name": "Perseverance Rover", "launch_date": "2020-07-30", "status": "Active",
     "target": "Mars - Jezero Crater", "agency": "NASA",
     "description": "NASA's Perseverance rover landed on Mars in February 2021 in Jezero Crater, an ancient lake bed. It is searching for signs of ancient microbial life, collecting rock and soil samples for future return to Earth, and testing oxygen production from the Martian atmosphere using MOXIE."},
    {"name": "Artemis Program", "launch_date": "2022-11-16", "status": "Active",
     "target": "Moon - Lunar South Pole", "agency": "NASA",
     "description": "The Artemis program aims to return humans to the Moon including the first woman and first person of color. Artemis I was an uncrewed test flight around the Moon in 2022. Future missions will establish a sustainable lunar presence as a stepping stone to Mars."},
    {"name": "Voyager 1", "launch_date": "1977-09-05", "status": "Active",
     "target": "Interstellar Space", "agency": "NASA",
     "description": "Voyager 1 is the farthest human-made object from Earth, now in interstellar space over 23 billion kilometers away. Launched in 1977, it flew past Jupiter and Saturn. It still communicates with Earth despite being so far away, with signals taking over 22 hours to arrive."},
    {"name": "Hubble Space Telescope", "launch_date": "1990-04-24", "status": "Active",
     "target": "Various / Deep Field", "agency": "NASA/ESA",
     "description": "The Hubble Space Telescope has revolutionized astronomy since 1990. It has helped determine the age of the universe, discovered dark energy, observed the birth and death of stars, and captured stunning images of galaxies billions of light years away."},
    {"name": "Cassini-Huygens", "launch_date": "1997-10-15", "status": "Completed",
     "target": "Saturn System", "agency": "NASA/ESA/ASI",
     "description": "The Cassini spacecraft orbited Saturn for 13 years from 2004 to 2017, studying its rings, atmosphere, and moons. The Huygens probe landed on Titan revealing rivers and lakes of liquid methane. Cassini ended its mission by diving into Saturn's atmosphere in the Grand Finale."},
    {"name": "New Horizons", "launch_date": "2006-01-19", "status": "Active",
     "target": "Pluto / Kuiper Belt", "agency": "NASA",
     "description": "New Horizons performed the first flyby of Pluto in July 2015, revealing a geologically active world with mountains of water ice and a heart-shaped nitrogen plain called Tombaugh Regio. It continues into the Kuiper Belt studying distant objects."},
    {"name": "InSight Lander", "launch_date": "2018-05-05", "status": "Completed",
     "target": "Mars - Elysium Planitia", "agency": "NASA",
     "description": "NASA's InSight lander studied the deep interior of Mars using a seismometer detecting marsquakes and a heat probe. It operated from 2018 to 2022 providing the first detailed look at the interior structure of another planet."},
]

SPACE_FACTS = [
    "The Sun contains 99.86% of all the mass in the solar system.",
    "A neutron star is so dense that a teaspoon of its material would weigh about 10 million tonnes.",
    "The Milky Way galaxy contains an estimated 100 to 400 billion stars.",
    "Light from the Sun takes about 8 minutes and 20 seconds to reach Earth.",
    "The universe is approximately 13.8 billion years old.",
    "Black holes are regions where gravity is so strong that nothing, not even light, can escape.",
    "The International Space Station orbits Earth at approximately 28,000 km/h.",
    "There are more stars in the universe than grains of sand on all of Earth's beaches.",
    "The Great Red Spot on Jupiter is a storm that has been active for at least 350 years.",
    "Water has been found on the Moon in the form of ice in permanently shadowed craters.",
    "Olympus Mons on Mars is the tallest volcano in the solar system at 22 km high.",
    "Europa, a moon of Jupiter, is considered one of the most promising places to look for extraterrestrial life due to its subsurface ocean.",
    "The temperature at the core of the Sun is approximately 15 million degrees Celsius.",
    "Saturn's rings are made mostly of water ice particles ranging from tiny grains to boulders as large as a house.",
    "A day on Venus is longer than a year on Venus due to its extremely slow rotation.",
]

def fetch_apod(api_key: str = "DEMO_KEY") -> list:
    """Fetch Astronomy Picture of the Day data from NASA API."""
    try:
        url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}&count=10"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"Fetched {len(data)} APOD entries from NASA API.")
            return data
        else:
            print(f"NASA API returned status {response.status_code}, using fallback.")
            return []
    except Exception as e:
        print(f"Could not reach NASA API: {e}. Using local data.")
        return []

def load_planets_to_db(db_session) -> None:
    """Load planet data into MySQL database."""
    from app.models.database import Planet
    for planet_data in tqdm(SOLAR_SYSTEM_DATA, desc="Loading planets"):
        existing = db_session.query(Planet).filter(Planet.name == planet_data["name"]).first()
        if not existing:
            planet = Planet(**planet_data)
            db_session.add(planet)
    db_session.commit()
    print(f"Loaded {len(SOLAR_SYSTEM_DATA)} planets into database.")

def load_missions_to_db(db_session) -> None:
    """Load NASA mission data into MySQL database."""
    from app.models.database import NasaMission
    for mission_data in tqdm(NASA_MISSIONS_DATA, desc="Loading missions"):
        existing = db_session.query(NasaMission).filter(NasaMission.name == mission_data["name"]).first()
        if not existing:
            mission = NasaMission(**mission_data)
            db_session.add(mission)
    db_session.commit()
    print(f"Loaded {len(NASA_MISSIONS_DATA)} missions into database.")

def get_all_documents() -> list:
    """Return all documents formatted for RAG ingestion."""
    documents = []
    # Planet documents
    for p in SOLAR_SYSTEM_DATA:
        doc = f"Planet: {p['name']}\nType: {p['type']}\nMass: {p['mass']} x 10^24 kg\nRadius: {p['radius']} km\nDistance from Sun: {p['distance_from_sun']} million km\nOrbital Period: {p['orbital_period']} Earth days\nMoons: {p['moons']}\nDescription: {p['description']}"
        documents.append({"content": doc, "source": f"Planet: {p['name']}", "type": "planet"})
    # Mission documents
    for m in NASA_MISSIONS_DATA:
        doc = f"Mission: {m['name']}\nAgency: {m['agency']}\nLaunch Date: {m['launch_date']}\nStatus: {m['status']}\nTarget: {m['target']}\nDescription: {m['description']}"
        documents.append({"content": doc, "source": f"Mission: {m['name']}", "type": "mission"})
    # Space facts
    for i, fact in enumerate(SPACE_FACTS):
        documents.append({"content": f"Space Fact: {fact}", "source": f"Space Facts #{i+1}", "type": "fact"})
    print(f"Prepared {len(documents)} documents for RAG pipeline.")
    return documents