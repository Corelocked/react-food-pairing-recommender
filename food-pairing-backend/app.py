from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Load the trained model and mappings
model = joblib.load('pairing_model.pkl')
dish_to_index = joblib.load('dish_to_index.pkl')
pairing_to_index = joblib.load('pairing_to_index.pkl')

# Create an inverse mapping for pairings
index_to_pairing = {index: pairing for pairing, index in pairing_to_index.items()}

@app.route('/pairing', methods=['POST'])
def get_pairing():
    data = request.json

    # Validate input
    if 'dish' not in data:
        return jsonify({'error': 'No dish provided'}), 400

    dish = data['dish']

    # Check if the dish exists in the mapping
    if dish not in dish_to_index:
        return jsonify({'error': 'Dish not found in the database'}), 404

    # Prepare the input for the model
    dish_index = dish_to_index[dish]
    input_vector = np.zeros(len(dish_to_index))
    input_vector[dish_index] = 1

    # Reshape for the model
    input_vector = input_vector.reshape(1, -1)

    # Get the pairings using the model
    distances, indices = model.kneighbors(input_vector)

    # Get the recommended pairing
    recommended_pairings = [index_to_pairing[i] for i in indices[0]]

    return jsonify({'recommended_pairings': recommended_pairings})

if __name__ == '__main__':
    app.run(debug=True)
