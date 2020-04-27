# Create Objects Points

    POST x,y

#   Get Nearest Airports

    GET nearest point(x,y), number of points

    airports

# load data

    ogr2ogr -f PostgreSQL PG:"dbname=geodatabase user=postgres password=password" file -nln table

    airports - airports.geojson
    states - state.geojson
    zipcodes - zipcode.geojson