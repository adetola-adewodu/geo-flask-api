from flask import Flask, Response, request, jsonify
import pg8000
import json
import yaml

app = Flask(__name__)
conn = None
cursor = None

with open("database.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile)
        database_variables = cfg["dev"]
        # use our connection values to establish a connection
        user = database_variables['user']
        database = database_variables['db']
        conn = pg8000.connect(user=user, database=database)
        cursor = conn.cursor()

def to_geojson(rows, root='features'):

    return "{\"type\": \"FeatureCollection\"," + \
    "\"crs\": { \"type\": \"name\", \"properties\": { \"name\": \"urn:ogc:def:crs:OGC:1.3:CRS84\" } }," +\
    "\"" + root + "\":" + json.dumps(rows, separators=(',', ':')) + "}"

def init():
    with open("database.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile)
    database_variables = cfg["dev"]
    # use our connection values to establish a connection
    user = database_variables['user']
    database = database_variables['db']
    conn = pg8000.connect(user=user, database=database)
    # create a psycopg2 cursor that can execute queries
    
    return conn.cursor()


@app.route("/nearest")
def get_nearest():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    k_nearest = request.args.get('k')
    print(latitude, longitude)
    query = '''SELECT 'Feature' as type, row_to_json((SELECT l FROM ( select id,ogc_fid,name, city, country, faa "abbreviation") as l)) 
            as properties,st_asgeojson(wkb_geometry)::json as geometry from airports
            order by st_astext(wkb_geometry) 
            <-> ST_Point({longitude}, {latitude}) limit {k_nearest};'''.format(latitude=latitude, longitude=longitude, k_nearest=k_nearest)
    print(query)
    results = {}
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        results = to_geojson(rows)
    except Exception as err:
        print("Exception: {0}".format(err))
        cursor.execute("ROLLBACK")
    
    return results

@app.route('/airport/<id>')
def get_airport_by_id(id):

    query = '''select * from airports where id = '{id}';'''.format(id=id)
    result = {}
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        result = to_geojson(rows)
    except Exception as err:
        print("Exception: {0}".format(err))
        cursor.execute("ROLLBACK")
    
    return result

@app.route('/airports')
def get_airports_by_name():
    name = request.args.get('name')
    query = '''select * from airports where name like '%{name}%';'''.format(name=name)
    results = {}
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        results = to_geojson(rows)
    except Exception as err:
        print("Exception: {0}".format(err))
        cursor.execute("ROLLBACK")
    
    return results


if __name__ == '__main__':
    
    app.debug = True
    app.run()