from flask import Flask, render_template, request, jsonify
from predction import PredictionService

app = Flask(__name__,
            static_url_path='',
            static_folder='assets',
            template_folder='templates')

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
        return jsonify({'message': 'Content-Type not supported!'})
    service = PredictionService()
    data = request.json
    return service.predict_diseases(data['variables'])

if __name__ == '__main__':
   app.run()