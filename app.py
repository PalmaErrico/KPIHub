from flask import Flask, render_template, jsonify, request
from datetime import datetime
import json
import os

app = Flask(__name__)

# JSON file path
KPI_DATA_FILE = 'data/kpi_data.json'

def load_kpi_data():
    if os.path.exists(KPI_DATA_FILE):
        with open(KPI_DATA_FILE, 'r') as f:
            return json.load(f)
    return {
        'metadata': {
            'title': 'KPI MNIST',
            'author': 'Palma Errico',
            'date': '05/04/2024',
            'version': '1'
        },
        'dataset': {
            'name': 'MNIST',
            'description': 'MNIST dataset for handwritten digit recognition',
            'total_records': 382705,
            'format': 'gzip',
            'image_size': '28x28 px',
            'classes': 10,
            'pixel_range': 255
        },
        'models': {
            'centralized': {
                'name': 'Centralized Model',
                'description': 'Centralized implementation using LeNet-5',
                'type': 'CNN',
                'train': '80%',
                'test': '20%',
                'learning_rate': 0.001,
                'optimizer': 'Adam',
                'loss_function': 'MSE Loss',
                'batch_size': 64,
                'epochs': 50,
                'kpi': {
                    'accuracy': 0.95,
                    'loss': 0.05,
                    'execution_time': 120,
                    'memory_usage': 1024,
                    'instruction_count': 50000
                }
            },
            'federated': {
                'name': 'Federated Model',
                'description': 'Federated implementation with client/server architecture',
                'type': 'fedAvg',
                'train': '80%',
                'test': '20%',
                'learning_rate': 0.1,
                'optimizer': 'SGD',
                'loss_function': 'MSE Loss',
                'batch_size': 32,
                'epochs': 15,
                'rounds': 10,
                'clients': 10,
                'kpi': {
                    'accuracy': 0.92,
                    'loss': 0.08,
                    'execution_time': 180,
                    'memory_usage': 512,
                    'instruction_count': 75000
                }
            }
        }
    }

def save_kpi_data(data):
    with open(KPI_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def home():
    data = load_kpi_data()
    return render_template('index.html', **data)

@app.route('/model/<model_id>')
def model_detail(model_id):
    data = load_kpi_data()
    if model_id in data['models']:
        return render_template('model_detail.html', model=data['models'][model_id])
    return "Model not found", 404

@app.route('/compare')
def compare():
    return render_template('compare.html', models=load_kpi_data()['models'])

@app.route('/api/models')
def get_models():
    return jsonify(load_kpi_data())

@app.route('/api/update_model', methods=['POST'])
def update_model():
    data = load_kpi_data()
    update = request.get_json()
    model_id = update.get('model_id')
    if model_id in data['models']:
        data['models'][model_id]['kpi'].update(update.get('kpi', {}))
        save_kpi_data(data)
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Model not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)