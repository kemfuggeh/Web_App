from flask import Flask, render_template, request, session
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session security

# Load dorm data from Excel file
dorms_df = pd.read_excel('dorms_data.xlsx')

# Path to the historical ratings CSV file
historical_ratings_path = 'C:/Users/K/Desktop/Dormitory/historical_ratings.csv'

# Check if the historical ratings file exists
if os.path.exists(historical_ratings_path):
    # Load historical ratings from the CSV file
    historical_ratings_df = pd.read_csv(historical_ratings_path, index_col='User')
    historical_ratings = historical_ratings_df.to_dict(orient='index')
else:
    # If the file doesn't exist, create an empty dictionary
    historical_ratings = {}

def is_valid_budget(budget):
    return 500 <= budget <= 999999  # Adjust the range as needed

def calculate_similarity(user_preferences, dorm):
    # Calculate similarity based on current preferences
    distance = sum((user_preferences[feature] - dorm[feature])**2
                   for feature in user_preferences
                   if feature in dorm and isinstance(user_preferences[feature], (int, float)) and isinstance(dorm[feature], (int, float)))

    # Collaborative filtering part - incorporate historical ratings
    for user, ratings in historical_ratings.items():
        if user_preferences['budget'] >= dorm['budget'] and dorm['name'] in ratings:
            distance += (user_preferences['ratings'].get(dorm['name'], 0.0) - ratings[dorm['name']])**2

    similarity = 1 / (1 + distance)
    return similarity

def recommend_dorms(user_preferences, top_n=3):
    valid_dorms = [dorm for dorm in dorms_df.to_dict('records') if user_preferences['budget'] >= dorm['budget']]
    valid_dorms = sorted(valid_dorms, key=lambda x: x['budget'])

    if not valid_dorms:
        return []  # No valid dorms

    scores = []
    for dorm in valid_dorms:
        # Check if 'barangay' is present in dorm details
        barangay = dorm.get('barangay', 'N/A')

        similarity_rating = calculate_similarity(user_preferences, dorm)
        scores.append({'dorm': dorm['name'], 'rating': similarity_rating, 'location': dorm['location'],
                       'barangay': barangay,  # Add Barangay to the recommendation
                       'distance': dorm['distance'], 'rides': dorm['rides'],
                       'details': dorm})

    recommended_dorms = sorted(scores, key=lambda x: x['rating'], reverse=True)[:top_n]

    # Save the user input and dorm information to an Excel file
    user_data = pd.DataFrame([user_preferences])
    dorms_data = pd.DataFrame(recommended_dorms)
    user_and_dorms_data = pd.concat([user_data, dorms_data], axis=1)
    user_and_dorms_data.to_excel('C:/Users/K/Desktop/Dormitory/dataset.xlsx', index=False)

    return recommended_dorms
@app.route('/homepage.html')
def homepage():
    return render_template('homepage.html')
@app.route('/')
def index():
    try:
        # Load the most recently saved user and dorm information from the Excel file
        user_and_dorms_data = pd.read_excel('C:/Users/K/Desktop/Dormitory/dataset.xlsx')

        # Check if the DataFrame is not empty and has the expected structure
        if not user_and_dorms_data.empty and 'dorm' in user_and_dorms_data.columns:
            dorm_data = user_and_dorms_data.to_dict('records')
        else:
            dorm_data = []

    except (FileNotFoundError, IndexError, KeyError):
        dorm_data = []

    return render_template('index.html', dorm_data=dorm_data)

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    user_preferences = {
        'budget': float(request.form['budget']),
        'location': request.form['location'],
        'room_size': request.form['room_size'],
        'bathroom': request.form['bathroom'],
        'environment': request.form['environment'],
        'barangay': request.form.get('barangay', 'N/A'),
        'near school': request.form.get('near school', 'N/A'),
        'ratings': {}  # Add an empty dictionary for storing user ratings
    }

    # Extract dorm ratings from the form data
    for dorm_name in dorms_df['name']:
        rating = request.form.get(f'rating_{dorm_name}', None)
        if rating is not None:
            user_preferences['ratings'][dorm_name] = float(rating)

    if not is_valid_budget(user_preferences['budget']):
        return render_template('no_recommendation.html')

    recommended_dorms = recommend_dorms(user_preferences, top_n=3)

    if not recommended_dorms:
        return render_template('no_recommendation.html')

    # Save user input in the session
    session['user_preferences'] = user_preferences

    return render_template('recommendations.html', recommended_dorms=recommended_dorms)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
