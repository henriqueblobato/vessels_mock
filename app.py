from flask import Flask, jsonify
from faker import Faker
from flask_cors import CORS
import random
from global_land_mask import globe
from uuid import uuid4
fake = Faker()

app = Flask(__name__)
CORS(app)

vessels = []


def generate_vessels():
    while True:
        lat, lon = fake.latlng()
        if globe.is_ocean(float(lat), float(lon)):
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
        if len(vessels) == 300:
            print('Vessels created!')
            return True


generate_vessels()


def move_vessels():
    for vessel in vessels:
        movement = float(random.random() / 1_000_000)
        vessel['latitude'] += movement
        vessel['longitude'] += movement
        try:
            current_porcentage = int(vessel['complete'][:2])
            add_porcentage = random.random()
            if current_porcentage + add_porcentage >= 100:
                vessel['complete'] = 'COMPLETE'
            else:
                vessel['complete'] = f'{round(current_porcentage + add_porcentage, 2)}%'
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