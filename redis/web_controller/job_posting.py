from flask import Flask, jsonify, request

from resource import RedisResource

app = Flask(__name__)

@app.route('/extract', methods=['POST'])
def post_extract_job():
    body = request.json
    filename = body.get('filename')

    # TODO: make the extract function accessible from within this function
    RedisResource.extracting_queue.enqueue(thumbnail_worker.extract_resize, args=filename)
    
    return jsonify({'status': 'OK'})