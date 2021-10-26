from flask import Flask, jsonify
from faker import Faker
import random
# from mpl_toolkits.basemap import Basemap
#bm = Basemap()
fake = Faker()

app = Flask(__name__)

vessels = []


def generate_vessels_sea():
    while True:
        lat, lon = fake.latlng()
        if True:  # bm.is_land(lon, lat):
            vessels.append({
                'latitude': float(lat),
                'longitude': float(lon)
            })
        if len(vessels) == 10:
            return True
#generate_vessels_sea()


def generate_vessels():
    while True:
        lat, lon = fake.latlng()
        vessels.append({
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
        if len(vessels) == 10:
            print('Vessels created!')
            return True
generate_vessels()


def move_vessels():
    for vessel in vessels:
        movement = float(random.random() / 1000000)
        vessel['latitude'] += movement
        vessel['longitude'] += movement
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