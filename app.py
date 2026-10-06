from flask import Flask, render_template, jsonify, request
from datetime import datetime
import json
import os

app = Flask(__name__)

# JSON file path
KPI_DATA_FILE = 'data/kpi_data.json'

FEDERATED_AGGREGATORS = [
    {'name': 'FedAvg', 'accuracy': 96, 'loss': 0.15},
    {'name': 'FedMiddleAvg', 'accuracy': 88, 'loss': 0.33},
    {'name': 'FedAvgMomentum', 'accuracy': 92, 'loss': 0.62}
]

FEDERATED_DEPLOYMENT = [
    {'label': 'Desktop application', 'value': 'PyCharm'},
    {'label': 'Operating system', 'value': 'Linux'},
    {'label': 'System name', 'value': 'LAPTOP-PKUA4UTD'},
    {'label': 'Kernel release', 'value': '5.15.146.1-microsoft-standard-WSL2'},
    {'label': 'Kernel version', 'value': '#1 SMP Thu Jan 11 04:09:03 UTC 2024'},
    {'label': 'Architecture', 'value': 'x86_64'},
    {'label': 'Processor', 'value': 'AMD Ryzen 7 5700U'},
    {'label': 'RAM', 'value': '16 GB'},
    {'label': 'Python version', 'value': '3.10.12'}
]

FEDERATED_CONFIGURATION = [
    {'label': 'Training split', 'value': '89.3%'},
    {'label': 'Test split', 'value': '10.7%'},
    {'label': 'Learning rate', 'value': '0.002'},
    {'label': 'Optimizer', 'value': 'Adam'},
    {'label': 'Loss function', 'value': 'Cross-entropy'},
    {'label': 'Metric', 'value': 'Accuracy'},
    {'label': 'Batch size', 'value': '32'},
    {'label': 'Epochs per client', 'value': '40'},
    {'label': 'Number of clients', 'value': '10'},
    {'label': 'Communication rounds', 'value': '64'}
]

def load_kpi_data():
    if os.path.exists(KPI_DATA_FILE):
        with open(KPI_DATA_FILE, 'r') as f:
            return json.load(f)
    return {
        'metadata': {
            'title': 'KPIHub ',
            'author': 'Palma Errico',
            'created_at': '2024-04-05',
            'updated_at': '2026-10-06',
            'version': '2'
        },
        'dataset': {
            'name': 'EMNIST',
            'description': 'The EMNIST (Extended MNIST) dataset is an extension of the MNIST dataset, widely used for training and evaluating machine learning models in handwritten digit and character recognition tasks. In this project, the Only_Digits version will be used, which is a subset of the dataset containing only images belonging to the digit classes from 0 to 9.',
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
                'name': 'Best Federated Model',
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

@app.route('/aggregators')
def aggregator_comparison():
    return render_template(
        'aggregators.html',
        aggregators=FEDERATED_AGGREGATORS,
        deployment=FEDERATED_DEPLOYMENT,
        configuration=FEDERATED_CONFIGURATION
    )

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