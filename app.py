from flask import Flask, request, jsonify, render_template
import os
import json
from db_manager import db
from assistant import handle_query
from deal_score import calculate_deal_score

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        return jsonify(handle_query(data.get('query', ''), db.get_all_products()))

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)