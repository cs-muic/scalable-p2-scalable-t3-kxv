from flask import Flask, jsonify, request
from resource import RedisResource
from thumbnail_worker import extract_resize

app = Flask(__name__)

@app.route('/api/extract', methods=['POST'])
def post_extract_job():
    body = request.json
    filename = body.get('filename')
    RedisResource.extracting_queue.enqueue(extract_resize, args=[filename])

    return jsonify({'status': 'OK'})

app.run(host='0.0.0.0', port=5000)