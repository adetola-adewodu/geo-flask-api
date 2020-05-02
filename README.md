# Start postgres on the mac os:

    pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start

    pg_ctl -D /usr/local/var/postgres stop -s -m fast


# Create Objects Points

    POST x,y

#   Get Nearest Airports

    GET nearest point(x,y), k number of points

#    airports

# load data

    ogr2ogr -f PostgreSQL PG:"dbname=geodatabase user=postgres password=password" file -nln table

    airports - airports.geojson
    states - state.geojson
    zipcodes - zipcode.geojson