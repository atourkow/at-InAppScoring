# Real-Time In-Application Aggregates/Joins at Scale

The purpose of this demo is to show that doing aggregations in-application (app), to work around the lack of joins/aggregates within Cassandra, can work at scale

This demo is built to work with DataStax Entereprise 4.8+ and the Python Cassandra Driver 3.0+ (for the [Object Mapper](http://datastax.github.io/python-driver/object_mapper.html))

### Virtual Env ###
These steps are based on using [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/).
It is highly recommended to use virtualenv as it keeps packages separate between apps.
[Here's a good intro](http://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/).  
Install virtualenv
```bash
    sudo pip install virtualenv
```

Enter the directory of your application and create the virtualenv in the app directory (the name env is the standard)
```bash
mkdir /path/to/at_InAppScoring
cd /path/to/at_InAppScoring
git clone someURL .
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

#Start DSE in search mode
dse cassandra -s

# Create the keyspace - We'll create the tables in the generator
cqlsh -f setup/setup.cql

# Create and populate the tables
python 01.generate_data.py

#Create the SOLR Core
dsetool create_core at_inappscoring.expoerts generateResources=true reindex=true
```

### Running the demo

* Run the Ratings Generator Feed
    * `python 02.search_data.py 5 "SoftLayer, GSM, GitHub, Infrastructure Performance Layer"`


#### TODO
* Add recommendations
* Add Faceted Search
* Add GeoSpatial
