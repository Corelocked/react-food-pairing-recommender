import React, { useState } from 'react';
import axios from 'axios';

const PairingForm = () => {
    const [dish, setDish] = useState('');
    const [recommendations, setRecommendations] = useState([]);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(''); // Reset error state
        setRecommendations([]); // Clear previous recommendations

        try {
            const response = await axios.post('http://localhost:5000/pairing', { dish });
            setRecommendations(response.data.recommended_pairings);
        } catch (err) {
            if (err.response) {
                // Server responded with a status other than 200 range
                setError(err.response.data.error || 'An error occurred while fetching recommendations.');
            } else if (err.request) {
                // Request was made but no response was received
                setError('No response from the server. Please try again later.');
            } else {
                // Something else happened
                setError('An error occurred. Please try again.');
            }
        }
    };

    return (
        <div>
            <h1>Food Pairing Recommender</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={dish}
                    onChange={(e) => setDish(e.target.value)}
                    placeholder="Enter a dish"
                    required
                />
                <button type="submit">Get Recommendations</button>
            </form>

            {error && <p style={{ color: 'red' }}>{error}</p>}

            {recommendations.length > 0 && (
                <div>
                    <h2>Recommended Pairings:</h2>
                    <ul>
                        {recommendations.map((pairing, index) => (
                            <li key={index}>{pairing}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default PairingForm;
