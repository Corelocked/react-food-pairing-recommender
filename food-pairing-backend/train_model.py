import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import OneHotEncoder
import joblib

# Load your dataset
data = pd.read_csv('zomato_data.csv')  # Adjust this path as necessary

# Display the first few rows of the dataset (for verification)
print("Data Loaded:")
print(data.head())

# Manually define pairings for the dishes
pairings = {
    'Pasta': 'Red Wine',
    'Steak': 'Red Wine',
    'Salad': 'White Wine',
    'Chocolate Cake': 'Dessert Wine',
    'Pizza': 'Beer',
    'Sushi': 'Sake'
}

# Create a DataFrame from the pairings
pairing_data = []
for dish, pairing in pairings.items():
    pairing_data.append({'dish': dish, 'pairing': pairing})

df = pd.DataFrame(pairing_data)

# Create a unique list of dishes and pairings
unique_dishes = df['dish'].unique()
unique_pairings = df['pairing'].unique()

# Create a mapping from dishes to indices
dish_to_index = {dish: index for index, dish in enumerate(unique_dishes)}
pairing_to_index = {pairing: index for index, pairing in enumerate(unique_pairings)}

# Create a DataFrame to represent dish-pairing relationships
pairing_matrix = pd.DataFrame(0, index=unique_dishes, columns=unique_pairings)

# Populate the pairing matrix
for _, row in df.iterrows():
    pairing_matrix.loc[row['dish'], row['pairing']] = 1

# Reset the index for encoding
pairing_matrix.reset_index(inplace=True)
pairing_matrix.rename(columns={'index': 'dish'}, inplace=True)  # Ensure the index is named 'dish'

# Debugging: Print the columns of pairing_matrix
print("Columns in pairing_matrix:", pairing_matrix.columns)

# Use One-Hot Encoding for the dishes
encoder = OneHotEncoder(sparse_output=False)  # Updated to use sparse_output
X = encoder.fit_transform(pairing_matrix[['dish']])  # Now this should work

# Check the shape of X and contents
print("Shape of X:", X.shape)
print("Encoded Features:")
print(X)

# Train the Nearest Neighbors model
model = NearestNeighbors(n_neighbors=1)  # Adjust n_neighbors as needed
model.fit(X)

# Save the trained model to a file
joblib.dump(model, 'pairing_model.pkl')
print("Model trained and saved as 'pairing_model.pkl'!")

# Optionally, save the mapping dictionaries to use them later for recommendations
joblib.dump(dish_to_index, 'dish_to_index.pkl')
joblib.dump(pairing_to_index, 'pairing_to_index.pkl')
print("Dish and pairing index mappings saved!")
