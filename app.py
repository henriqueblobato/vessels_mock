from flask import Flask, jsonify
from faker import Faker
from flask_cors import CORS
import random
from uuid import uuid4
fake = Faker()

app = Flask(__name__)
CORS(app)

positions = [
    (31.322174, 32.239129),
    (31.324851, 32.343782),
    (36.018881, -5.440807),
    (35.962376, -6.002181),
    (35.926254, -5.465578),
    (-22.990278, -43.173343),
    (-22.988333, -43.171667),
    (-22.752565, -43.142199),
    (1.137489, 103.772821),
    (1.472769, 103.796110),
    (1.476490, 103.805328),
    (8.614388, 111.579314),
    (30.209297, 120.725029),
    (30.208889, 120.724444),
    (30.557001, 121.531522),
    (31.049639, 122.447354),
    (31.448518, 122.896698),
    (42.017706, -138.981602),
    (33.999203, -128.610508),
    (37.659521, -122.279078),
    (30.316922, -119.149503),
    (48.167490, -60.568659),
    (48.166667, -60.566667),
    (41.725496, -67.506965),
    (12.223368, -45.131178),
]
print('Positions:', len(positions))

vessels = []


def generate_vessels():
    for lat, lon in positions:
        vessels.append({
            'id': str(uuid4()),
            'latitude': float(lat),
            'longitude': float(lon),
            'type': random.choice(['cargo ship', 'tourism', 'fishing', 'tanker', 'tug']),
            'name': f'{fake.company()}',
            'size': random.randint(20, 250),
            'country': fake.country(),
            'from': fake.country(),
            'to': fake.country(),
            'complete': f'{random.randint(20, 85)}%',
            'speed': f'{random.randint(20, 90)} MPH'
        })


def move_vessels():
    for vessel in vessels:
        movement = float(random.random() / 1_000_000)
        vessel['latitude'] += movement
        vessel['longitude'] += movement
        try:
            current_percentage = int(vessel['complete'][:2])
            add_percentage = random.random()
            if current_percentage + add_percentage >= 100:
                vessel['complete'] = 'COMPLETE'
            else:
                vessel['complete'] = f'{round(current_percentage + add_percentage, 2)}%'
        except ValueError:
            continue
    print('Moved!')


@app.route("/")
def hello():
    if len(vessels) == 0:
        generate_vessels()
    move_vessels()
    return jsonify(vessels)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=8000,
        host='0.0.0.0'
    )
