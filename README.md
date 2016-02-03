# Real-Time In-Application Aggregates/Joins at Scale

The purpose of this demo is to show that doing aggregations in-application (app), to work around the lack of joins/aggregates within Cassandra, can work at scale

This demo is built to work with DataStax Entereprise 4.8+ and the Python Cassandra Driver 3.0+ (for the [Object Mapper](http://datastax.github.io/python-driver/object_mapper.html))

### Requirements ###
* Python PIP
* Python Virtual Environment
* Python Cassandra-driver


### Virtual Env (Understanding/Using it) ###
These steps are based on using [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/).
It is highly recommended to use virtualenv as it keeps packages separate between apps.
[Here's a good intro](http://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/).  
Install virtualenv
```bash
    sudo pip install virtualenv
```

Enter the directory of your application and create the virtualenv in the app directory (the name env is the standard)
```bash
git clone https://github.com/atourkow/at-InAppScoring.git
# Create a virtual environment in the `env` directory
virtualenv env
source env/bin/activate
    # If you're using fish shell (like I am):
    source env/bin/activate.fish
```

You are now in the virtualenv, your prompt should reflect this, and are ready to install other python packages.  
Type `deactivate` to exit the active virtualenv.


### Setup

```bash
#Install Python Requirements: (This can take a while)
pip install -r setup/requirements.txt

# If not started, Start DSE in search mode
dse cassandra -s

# Create the keyspace - We'll create the tables in the generator
deactivate
cqlsh -f setup/setup.cql
source env/bin/activate

# Update _config.py to use your server credentials
vim _config.py

# Get and parse Geo Location data which outputs to GeoLocationsUS.delim.txt
cd setup
wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCity_CSV/GeoLiteCity-latest.zip
unzip GeoLiteCity-latest.zip
python parse_cities_into_geo.py GeoLiteCity_20160105/GeoLiteCity-Location.csv
cd ..

# Create and populate the tables
01.generate_data.py n_experts_start n_experts_stop n_topics_per_expert
```

### Running the demo
You can get a list of topics in setup/topics.txt

* Run the Ratings Generator Feed
  * `python 02.search_data.py n_num_of_total "Comma, Separated, Topics"`
  * Example
    * `python 02.search_data.py 5 "SoftLayer, GSM, GitHub, Python"`
