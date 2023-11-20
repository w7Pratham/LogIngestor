from flask import Flask, request, jsonify, render_template
from cassandra.cluster import Cluster
from datetime import datetime

app = Flask(__name__)

# Connect to Cassandra
# Replace 'dbs-1' with the appropriate contact points
cluster = Cluster(['dbs-1'])
session = cluster.connect()

# Create keyspace
keyspace_query = """
CREATE KEYSPACE IF NOT EXISTS your_keyspace
WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1}
"""
session.execute(keyspace_query)

# Use the keyspace
session.set_keyspace('your_keyspace')

# Create table with a primary key on the commit field
table_query = """
CREATE TABLE IF NOT EXISTS your_table (
    id UUID PRIMARY KEY,
    level TEXT,
    message TEXT,
    resourceId TEXT,
    timestamp TEXT,
    traceId TEXT,
    spanId TEXT,
    commit TEXT,
    parentResourceId TEXT
)
"""

session.execute(table_query)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/insert', methods=['POST'])
def insert_data():
    try:
        # Extract data from the request
        data = request.json
        level = data.get('level')
        message = data.get('message')
        resourceId = data.get('resourceId')
        timestamp_str = data.get('timestamp')
        traceId = data.get('traceId')
        spanId = data.get('spanId')
        commit = data.get('commit')
        parentResourceId = data['metadata'].get('parentResourceId')

        # Insert data into Cassandra with a generated UUID for the primary key
        query = """
        INSERT INTO your_table (id, level, message, resourceId, timestamp, traceId, spanId, commit, parentResourceId)
        VALUES (uuid(), %s, %s, %s, %s, %s, %s, %s, %s)
        """
        session.execute(query, (level, message, resourceId, timestamp_str, traceId, spanId, commit, parentResourceId))

        return jsonify({'message': 'Data inserted successfully'})
    except Exception as e:
        error_message = str(e)
        print(f"Error: {error_message}")
        return jsonify({'error': f'400 Bad Request: {error_message}'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
