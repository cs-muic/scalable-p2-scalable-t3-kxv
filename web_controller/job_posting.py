from flask import Flask, jsonify, request
from resource import RedisResource
from thumbnail_worker import extract_resize
import uuid

app = Flask(__name__)

@app.route('/api/extract', methods=['POST'])
def post_extract_job():
    body = request.json
    filename = body.get('filename')
    unique_id = uuid.uuid4().hex
    RedisResource.extracting_queue.enqueue(extract_resize, args=[unique_id, filename])
    return jsonify({'video name': filename,
                    'tracking id': unique_id}), 200

# @app.route('/api/extract-all', methods=['POST'])
# def extract_all():
#     ...

# @app.route('/api/gifs', methods=['POST'])
# def all_gifs():
#     ...

@app.route('/api/get-status/<jobID>', methods=['GET'])
def a_status_tracking(jobID):
    try:
        status = (RedisResource.conn.get(jobID)).decode("utf-8")
        return jsonify({jobID: status}), 200
    except Exception as e: 
        return jsonify({"error": "ID not found"}), 400


app.run(host='0.0.0.0', port=5000)