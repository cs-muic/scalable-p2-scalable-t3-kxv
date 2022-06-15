from flask import Flask, jsonify, request
from resource import RedisResource
from thumbnail_worker import extract_resize, extract_resize_all, list_all
from minio_setup import get_elements, delete_gif, delete_all_elements
import uuid
import base64

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
    all_gifs = list_all(bucket_name)
    return jsonify({'gifs': all_gifs}), 200

@app.route('/api/get-status/<jobID>', methods=['GET'])
def a_status_tracking(jobID):
    try:
        status = (RedisResource.conn.get(jobID)).decode("utf-8")
        return jsonify({jobID: status}), 200
    except Exception as e: 
        return jsonify({"error": "ID not found"}), 400

@app.route('/api/get-gifs', methods=['POST'])
def get_gifs():
    try:
        body = request.json
        bucket_name = body.get('bucket')
        gifs_binary = get_elements(bucket_name)
        stream_strs = []
        for b in gifs_binary:
            stream_strs.append(f"data:image/gif;base64,{base64.b64encode(b.read()).decode('utf-8')}")
        return jsonify({'gifs': stream_strs}), 200
    except Exception as e:
        return jsonify({"error": "failed to get elements"}), 400

@app.route('/api/get-vids', methods=['POST'])
def get_vids():
    try:
        body = request.json
        bucket_name = body.get('bucket')
        vids_binary = get_elements(bucket_name)
        stream_strs = []
        for b in vids_binary:
            stream_strs.append(f"data:video/mp4;base64,{base64.b64encode(b.read()).decode('utf-8')}")
        return jsonify({'gifs': stream_strs}), 200
    except Exception as e:
        return jsonify({"error": "failed to get elements"}), 400

@app.route('/api/delete-a-gif', methods=['POST'])
def delete_a_gif():
    try:
        body = request.json
        bucket_name = body.get('bucket')
        file_name = body.get('filename')
        delete_gif(file_name, bucket_name)
        return jsonify({"status": "OK"}), 200
    except Exception as e: 
        return jsonify({"error": "cannot delete a gif"}), 400

@app.route('/api/delete-all-gifs', methods=['POST'])
def delete_all_gifs():
    try:
        body = request.json
        bucket_name = body.get('bucket')
        delete_all_elements(bucket_name)
        return jsonify({"status": "OK"}), 200
    except Exception as e: 
        return jsonify({"error": "cannot delete all gifs"}), 400
    
app.run(host='0.0.0.0', port=5000)