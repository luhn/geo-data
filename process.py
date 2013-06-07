import argparse
import sqlite3 as sqlite
import csv
from itertools import izip

from point_in_poly import point_in_poly
from point_to_poly import point_to_poly
import shapefile

state_codes = {'AK', 'AL', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN',
'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK',
'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'DC', 'WV',
'WI', 'WY'}

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--shapefiles', required=True,
        help='The timezone shapefiles.  Should be the filenames sans the ' +
            'extension.')
parser.add_argument('--cities', required=True, help='The CSV of cities.')
parser.add_argument('--zipcodes', required=True,
        help='The CSV of US zipcodes.')
parser.add_argument('--output', default='sqlite.db',
        help='The file for sqlite to save the output to.')
args = parser.parse_args()

# Read shapefiles
sf = shapefile.Reader(args.shapefiles)

# Connect to database and create the schema`
conn = sqlite.connect(args.output)
conn.text_factory = str
with open('schema.sql') as fh:
    c = conn.cursor()
    c.executescript(fh.read())
    conn.commit()

#Open up the cities CSV and start adding to the database
with open(args.cities) as fh:
    reader = csv.reader(fh)
    reader.next() #Skip first line
    c = conn.cursor()
    i = 0
    for row in reader:
        if row[0].lower() != 'us' or row[3].upper() not in state_codes:
            continue #Make sure it's a US city and in one of the 50 states
        city, state, lat, lng = (row[1].lower(), row[3].upper(), float(row[5]),
                float(row[6]))

        #Figure out the timezone
        timezone = None
        for record, shape in izip(sf.records(), sf.shapes()):
            if point_in_poly(lng, lat, shape.points):
                timezone = record[0]
                break
        if not timezone:
            print 'Could not find timezone, trying nearby: %s, %s' % (city,
                    state)
            for record, shape in izip(sf.records(), sf.shapes()):
                if point_to_poly(lng, lat, shape.points) < 0.1:
                    timezone = record[0]
                    print timezone
                    break
            if not timezone:
                print 'NOPE!'
                timezone = 'US/Pacific'

        #Save to database
        c.execute("""insert into city(city, state, lat, lng, timezone)
                values (?, ?, ?, ?, ?)""", (city, state, lat, lng, timezone))
        i += 1
        if i % 100 == 0:
            print i
            conn.commit() #Every 100 inserts, commit changes
    conn.commit()

#Read zip codes and start adding to database
with open(args.zipcodes) as fh:
    reader = csv.reader(fh)
    reader.next()
    c = conn.cursor()
    i = 0
    for row in reader:
        zip, city, state = row[0], row[2].lower(), row[3].upper()
        lat, lng = float(row[5]), float(row[6])

        c2 = conn.cursor()
        city = c2.execute("""select id from city where city=? and state=?""",
                (city, state)).fetchone()
        if city:
            city_id = city[0]
        else:
            city_id = None

        #Figure out the timezone
        timezone = None
        for record, shape in izip(sf.records(), sf.shapes()):
            if point_in_poly(lng, lat, shape.points):
                timezone = record[0]
                break
        if not timezone:
            print 'Could not find timezone, trying nearby: %s' % zip
            for record, shape in izip(sf.records(), sf.shapes()):
                if point_to_poly(lng, lat, shape.points) < 0.1:
                    timezone = record[0]
                    print timezone
                    break
            if not timezone:
                print 'NOPE!'
                timezone = 'US/Pacific'

        c.execute("""insert into zip(zip, city_id, lat, lng, timezone)
            values (?, ?, ?, ?, ?)""", (zip, city_id, lat, lng, timezone))

        i += 1
        if i % 100 == 0:
            print i
            conn.commit()

print 'Done!'


