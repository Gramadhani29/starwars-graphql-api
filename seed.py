from database import get_db_connection, init_db

def seed_data():
    """Mengisi database dengan data awal Star Wars."""
    conn = get_db_connection()
    c = conn.cursor()

    # Bersihkan data lama
    c.execute("DELETE FROM character_starships")
    c.execute("DELETE FROM characters")
    c.execute("DELETE FROM starships")
    c.execute("DELETE FROM planets")
    conn.commit()

    # Data planet
    planets = [
        ("Tatooine", "Arid", "Desert"),
        ("Alderaan", "Temperate", "Grasslands, Mountains"),
        ("Yavin IV", "Temperate, Humid", "Jungle, Rainforests"),
        ("Naboo", "Temperate", "Grassy Hills, Swamps"),
        ("Coruscant", "Temperate", "Cityscape"),
    ]
    c.executemany("INSERT INTO planets (name, climate, terrain) VALUES (?, ?, ?)", planets)
    planet_ids = {row["name"]: row["id"] for row in c.execute("SELECT id, name FROM planets").fetchall()}

    # Data karakter
    characters = [
        ("Luke Skywalker", "Human", planet_ids["Tatooine"]),
        ("Leia Organa", "Human", planet_ids["Alderaan"]),
        ("Han Solo", "Human", None),
        ("C-3PO", "Droid", None),
        ("Yoda", "Unknown", None),
    ]
    c.executemany("INSERT INTO characters (name, species, home_planet_id) VALUES (?, ?, ?)", characters)
    character_ids = {row["name"]: row["id"] for row in c.execute("SELECT id, name FROM characters").fetchall()}

    # Data kapal
    starships = [
        ("Millennium Falcon", "YT-1300 light freighter", "Corellian Engineering"),
        ("X-wing", "T-65 X-wing starfighter", "Incom Corporation"),
        ("TIE Fighter", "TIE/LN starfighter", "Sienar Fleet Systems"),
    ]
    c.executemany("INSERT INTO starships (name, model, manufacturer) VALUES (?, ?, ?)", starships)
    starship_ids = {row["name"]: row["id"] for row in c.execute("SELECT id, name FROM starships").fetchall()}

    # Relasi karakter-kapal
    character_starships = [
        (character_ids["Han Solo"], starship_ids["Millennium Falcon"]),
        (character_ids["Luke Skywalker"], starship_ids["X-wing"]),
    ]
    c.executemany("INSERT INTO character_starships (character_id, starship_id) VALUES (?, ?)", character_starships)

    conn.commit()
    conn.close()
    print("Database berhasil diisi dengan data Star Wars!")

if __name__ == "__main__":
    init_db()  # Pastikan tabel ada
    seed_data()