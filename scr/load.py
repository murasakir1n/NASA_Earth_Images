from sqlalchemy import engine, text, inspect
import os
from dotenv import load_dotenv
import psycopg2
from extract import extract_data




def load_data():

    data = extract_data()

    load_dotenv()
    db = os.getenv('DB')

    connection = psycopg2.connect(db)
    cursor = connection.cursor()

    try:


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS images(    
            id SERIAL PRIMARY KEY,
            image_name TEXT UNIQUE,
            caption TEXT,
            date TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS position(
            id SERIAL PRIMARY KEY,
            image_id INT REFERENCES images(id),
            body TEXT,
            x FLOAT,
            y FLOAT,
            z FLOAT,
            UNIQUE (image_id, body)
        )
        """)


        for item in data:


            image_name = item['image']
            date = item['date']
            caption = item["caption"]

            cursor.execute("""
                INSERT INTO images(image_name, caption, date)
                VALUES(%s, %s, %s)
                ON CONFLICT (image_name) DO NOTHING
                RETURNING id
            """, (image_name, caption, date))

            result = cursor.fetchone()

            if result:
                image_id = result[0]
            else:
                cursor.execute(
                    'SELECT id FROM images WHERE image_name = %s',
                    (image_name,)
                )
                image_id = cursor.fetchone()[0]

            #positions
            coords = item['coords']

            positions = [
                ("sun", coords["sun_j2000_position"]),
                ("lunar", coords["lunar_j2000_position"]),
                ("dscovr", coords["dscovr_j2000_position"]),
            ]

            for body, pos in positions:
                cursor.execute("""
                    INSERT INTO position(image_id, body, x, y, z)
                    VALUES(%s, %s, %s, %s, %s)
                    ON CONFLICT (image_id, body) DO NOTHING
                """, (
                    image_id,
                    body,
                    pos['x'],
                    pos['y'],
                    pos['z']
                ))

        connection.commit()

    except Exception as e:
        print("ERROR:", e)
        connection.rollback()

    finally:
        cursor.close()
        connection.close()






load_data()

