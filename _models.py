from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class TopicScores(Model):
    topic = columns.Text(primary_key=True)
    score = columns.Float()

class ExpertByTopic(Model):
    topic = columns.Text(primary_key=True)
    expert_id = columns.Integer(primary_key=True)

class Experts(Model):
    expert_id = columns.Integer(primary_key=True)
    name = columns.Text()
    city = columns.Text()
    zip = columns.Text()
    lat_lon = columns.Text()
    topics = columns.Set(columns.Text)
