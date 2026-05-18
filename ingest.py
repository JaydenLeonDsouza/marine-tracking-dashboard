import pandas as pd
import psycopg2

# Load first 1000 rows
df = pd.read_csv("data/ais-2025-12-31.csv", nrows=1000)

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="marine",
    user="postgres",
    password="jlds",
    port="5432"
)

cur = conn.cursor()

# Insert rows
for _, row in df.iterrows():

    cur.execute(
        """
        INSERT INTO ship_positions (
            mmsi,
            base_date_time,
            latitude,
            longitude,
            sog,
            cog,
            heading,
            vessel_name,
            vessel_type,
            status,
            length,
            width,
            draft,
            cargo,
            transceiver
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            row["mmsi"],
            row["base_date_time"],
            row["latitude"],
            row["longitude"],
            row["sog"],
            row["cog"],
            row["heading"],
            row["vessel_name"],
            row["vessel_type"],
            row["status"],
            row["length"],
            row["width"],
            row["draft"],
            row["cargo"],
            row["transceiver"]
        )
    )

conn.commit()

print("Inserted 1000 real AIS rows successfully!")

cur.close()
conn.close()