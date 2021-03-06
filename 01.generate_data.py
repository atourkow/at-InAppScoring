#!/usr/bin/env python
import sys
import time
import resource

from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from faker import Faker

from _config import Config
from _models import *

import random
from prettytable import PrettyTable

# Command line arguements
if len(sys.argv) < 4:
    print "Usage:"
    print "01.generate_data.py n_experts_start n_experts_stop n_topics_per_expert"
    print ""
    sys.exit()

expert_start = int(sys.argv[1])
expert_total = int(sys.argv[2])
topic_max_per_expert = int(sys.argv[3])

# Load our config
config = Config()
# Connect to Cassandra
connection.setup(config.servers, config.keyspace, protocol_version=3)
# Create/Update tables
sync_table(TopicScores)
sync_table(ExpertByTopic)
sync_table(Experts)

fake = Faker()


# Get list of topics and map a score to them
start = time.time()
total = 0
print "Mem Before Read: {}".format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000)
topics = open("setup/topics.txt", 'r').read().splitlines()
GeoLocations = open("setup/GeoLocationsUS.delim.txt", 'r').read().splitlines()
print "Mem After Read : {}".format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000)
print ""

for line in topics:
    total += 1

    topic = line.strip()
    score = round(random.uniform(0.1,1), 5)
    TopicScores.create(topic=topic, score=score)

    sys.stdout.write("\r{:4} | {:60} | {:>2}".format(total, topic, score))
    sys.stdout.flush()

total_time = time.time() - start
print "\n"
print "Records    : {}".format(total)
print "Total Time : {}".format(total_time)
print "Rec per Sec: {}/s".format(float(total) / total_time)
print "Mem Used   : {}".format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000)
print ""

# For N number of experts randomly assign to topics, an expert can be in more than one topic
expert_count = expert_start
start = time.time()
total_records = 0

while expert_count < expert_total:
    expert_count += 1

    # Insert the Expert Meta Data
    (metaCity, metaZip, metaLatLon) = GeoLocations[random.randint(0, len(GeoLocations)-1)].split("||")
    #ExpertMeta.create(expert_id=expert_count, city=metaCity, zip=metaZip, lat_lon=metaLatLon)

    # Randomly select how many topics an expert knows
    topic_max = random.randint(1,topic_max_per_expert)
    topic_count = 0
    topic_list = []
    while topic_count < topic_max:
        total_records += 1
        topic_count += 1
        topic = random.choice(topics)

        # Make a list of topics for expert
        topic_list.append(topic)

        # Group experts into a topic
        ExpertByTopic.create(topic=topic, expert_id=expert_count)
        sys.stdout.write("\rUser:{: >7}/{: <7} Topics:{: >3}/{: <3} | {:60}".format(expert_count, expert_total, topic_max, topic_count, topic))
        sys.stdout.flush()

    #sys.stdout.write("\rUser:{: >7} {} {} {} {} {}".format(expert_count, fake.name(), metaCity, metaZip, metaLatLon, topic_list))
    #sys.stdout.flush()
    #Put the expert data in
    Experts.create(expert_id=expert_count, name=fake.name(), city=metaCity, zip=metaZip, lat_lon=metaLatLon, topics=topic_list)

total_time = time.time() - start
print "\n"
print "Experts Start: {}".format(expert_start)
print "Experts Stop : {}".format(expert_total)
print "Records      : {}".format(total_records)
print "Total Time   : {}".format(total_time)
print "Rec per Sec  : {}/s".format(float(total_records) / total_time)
print "Mem Used     : {}".format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000)
print ""

out = [expert_start, expert_count, topic_max_per_expert, total_records]
pt = PrettyTable(['Experts Start', 'Total Experts', 'Max Topics per Expert', 'Total Records'])
pt.add_row(out)
pt.align = "l"
print pt

f_out.write("\t".join(map(str,out)) + "\n")

# Output to CSV
f_out = open('results_generator.txt','a')
f_out.write("\t".join(map(str,out)) + "\n")
f_out.close()
