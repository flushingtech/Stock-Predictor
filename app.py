from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS from flask_cors

app = Flask(__name__)
CORS(app)  # Add CORS middleware to your Flask app

@app.route('/predict', methods=['GET'])
def predict():
    # Add your prediction logic here
    symbol = request.args.get('symbol')
    # Make predictions and return the result as a JSON response
    prediction_data = {
        'symbol': symbol,
        'price': 200,  # Replace with actual real-time price
        'changePercent': -3.5,  # Replace with actual change percent
        'predictedPrice': 210.50  # Replace with actual predicted price
    }
    return jsonify(prediction_data)

if __name__ == '__main__':
    app.run(debug=True)
