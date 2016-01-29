DROP keyspace IF EXISTS at_inappscoring;
CREATE KEYSPACE at_inappscoring WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
