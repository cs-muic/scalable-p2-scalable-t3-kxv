from enum import unique
from flask import Flask, jsonify, request
from resource import RedisResource
from thumbnail_worker import extract_resize, list_all, given_id, update_status
from minio_setup import get_elements, delete_gif, delete_all_elements
import uuid
import base64

app = Flask(__name__)

@app.route('/api/extract', methods=['POST'])
def post_extract_job():
    body = request.json
    filename = body.get('filename')
    unique_id = uuid.uuid4().hex
    RedisResource.status_queue.enqueue(update_status, args=[unique_id, "waiting for a queue"])
    RedisResource.extracting_queue.enqueue(extract_resize, args=[unique_id, filename])
    return jsonify({'video_name': filename,
                    'tracking_id': unique_id}), 200

@app.route('/api/extract-all', methods=['POST'])
def extract_all():
    body = request.json
    bucket_name = body.get('bucket')
    work_dict = given_id(bucket_name)
    return jsonify({'id_lst': work_dict}), 200

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
        return jsonify({'id': jobID,
                        'status': status}), 200
    except Exception as e: 
        return jsonify({"error": "ID not found"}), 400

@app.route('/api/get-all-status', methods=['POST'])
def all_status_tracking():
    try:
        body = request.json
        bucket_name = body.get('bucket')
        work_dict = given_id(bucket_name)
        rec_status = []
        for work in work_dict:
            unique_id = work['id']
            status = (RedisResource.conn.get(unique_id)).decode("utf-8")
            rec_status.append({
                'id': unique_id,
                'status': status
            })
        return jsonify({'all_status': rec_status}), 200
    except Exception as e:
        return jsonify({"error": "not able to get all status"}), 400

@app.route('/api/get-gifs', methods=['POST'])
def get_gifs():
    try:
        body = request.json
        bucket_name = body.get('bucket')
        gifs_binary = get_elements(bucket_name)
        stream_strs = []
        for b in gifs_binary:
            stream_strs.append({
                'name': b['name'], 
                'file': f"data:image/gif;base64,{base64.b64encode(b['data'].read()).decode('utf-8')}"
            })
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
            stream_strs.append({
                'name': b['name'], 
                'file': f"data:video/mp4;base64,{base64.b64encode(b['data'].read()).decode('utf-8')}"
            })
        return jsonify({'vids': stream_strs}), 200
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