geo-data
========

US zipcode and city list with latitude, longitude, and timezone.

[Download](https://github.com/luhn/geo-data/releases/download/2013.6/geo-data.zip) [.zip, 2.5MB]

## Usage

The usage is pretty basic.

    python process.py --shapefiles shapefiles/tz_us --cities cities.csv --zipcodes zipcodes.csv --output sqlite.
    
Notice how we don't have an extension for `shapefiles/tz_us`.  Since the timezone shapefile is composed of many individual files, omit the extension and the shapefile library will automatically load all the needed files.

If these instructions didn't really do it for you, there's also `python process.py --help`.

Note that this is a very resource-intensive script (O(m*n)), and will take quite a while to complete.  (Two days on an AWS Medium EC2 instance I spun up.)  And because it's written in Python, GIL will prevent it from using more than a single core.

## Sources

This data is compiled using the following sources:

 * [Maxmind World City Database](http://www.maxmind.com/en/worldcities) [[license](http://download.maxmind.com/download/geoip/database/LICENSE_WC.txt)]
 * [Zip Code Database](http://federalgovernmentzipcodes.us/) [license?]
 * [US Timezones Shapefile](http://efele.net/maps/tz/us/) [[license](http://creativecommons.org/publicdomain/zero/1.0/)]
