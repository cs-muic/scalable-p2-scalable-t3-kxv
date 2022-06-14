from flask import Flask, jsonify, request
from resource import RedisResource
from thumbnail_worker import extract_resize, extract_resize_all, list_all_gifs
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

@app.route('/api/extract-all', methods=['POST'])
def extract_all():
    body = request.json
    bucket_name = body.get('bucket')
    RedisResource.extracting_queue.enqueue(extract_resize_all, args=[bucket_name])
    return jsonify({'bucket name': bucket_name}), 200

@app.route('/api/gifs', methods=['POST'])
def all_gifs():
    body = request.json
    bucket_name = body.get('bucket')
    all_gifs = list_all_gifs(bucket_name)
    return jsonify({'gifs': all_gifs}), 200

@app.route('/api/get-status/<jobID>', methods=['GET'])
def a_status_tracking(jobID):
    try:
        status = (RedisResource.conn.get(jobID)).decode("utf-8")
        return jsonify({jobID: status}), 200
    except Exception as e: 
        return jsonify({"error": "ID not found"}), 400


app.run(host='0.0.0.0', port=5000)