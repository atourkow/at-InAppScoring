#!/usr/bin/env python
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool

import sys
import time
import resource

from cassandra.cqlengine import connection
from collections import defaultdict
from prettytable import PrettyTable

from _config import Config
from _models import *

# Command line arguements
def usage():
    print "Usage:"
    print "02.search_data.py n_top_results 'Comma, Separated, Topics'"
    print "                  Must be Int   'Must include quotes     '"
    print ""
    sys.exit()

if len(sys.argv) < 3:
    usage()

top_max = int(sys.argv[1])
if not isinstance( top_max, ( int, long ) ):
    usage()

# "SoftLayer, GSM, GitHub, Infrastructure Performance Layer, Website Performance"
topics = [x.strip() for x in sys.argv[2].split(',')]

# Load our config
config = Config()
# Connect to Cassandra
connection.setup(config.servers, config.keyspace, protocol_version=3)

start = time.time()
print "Mem Before Read: {}".format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000)

# Number of threads to run concurrently
pool = Pool(20)

# Get list of topics and map a score to them
topic_scores = pool.map( lambda x: TopicScores.get(topic=x), topics)
topics_map = dict( [(x.topic, x.score) for x in topic_scores] )
#sys.exit()

# look up all topics
#topics_map = {"GSM": .9, "GitHub": .5, 'Windows 7': .1, 'ITIL': .2, 'Grid Computing': .3, 'Fortinet': .4, 'Server Power': .6}

# Create a map of users to scores
expert_scores = defaultdict(lambda: 0)
# Function to get experts by topic and then add the confidence for a user
def get_experts_for_topics(topic):
    topic_score = topics_map[topic]
    print "Fetching Data for Topic: {:60} {}".format(topic, topic_score)
    for x in ExpertByTopic.objects(topic=topic):
        expert_scores[x.expert_id] += topic_score
    print "Scores Merged for      : {}".format(topic)

# Run async queries
pool.map(get_experts_for_topics, topics_map.keys())

# Put the results into a tuple and sort by score descending
result = expert_scores.items()
result = sorted(result, key=lambda x: x[1], reverse=True)
#Output the top 100
result = result[0:top_max]

# Get the expert meta info
experts = pool.map( lambda x: Experts.get(expert_id=x), [expert_id for expert_id, score in result])

# Make it pretty
pt = PrettyTable(['ID', 'Name', 'City', 'zip', 'Lat Lon', 'Score'])
pt.align = "l"

for ex in experts:
    pt.add_row([ex.expert_id, ex.name, ex.city, ex.zip, ex.lat_lon, expert_scores[ex.expert_id]])

print pt


total_time = time.time() - start
print "\n"
print "Total Users Sorted: {}".format(len(expert_scores))
print "Top n returned in : {} | {}s".format(top_max, total_time)
print "Mem Used          : {}".format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000)
print ""

headers = ['Max Top Count', 'Topics Searched', 'Users Sorted', 'Time']
out = [top_max, len(topics), len(expert_scores), total_time]
pt = PrettyTable(headers)
pt.add_row(out)
pt.align = "l"
print pt

print "\t".join(map(str,out))

# Output to CSV
f_out = open('results_search.txt','a')
f_out.write("\t".join(map(str,out)) + "\n")
f_out.close()
