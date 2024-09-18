import os
from flask import Flask, request, jsonify
from google.generativeai import generate  # Adjust import according to the library you're using

app = Flask(__name__)

# Load environment variables
API_KEY = os.getenv('API_KEY')

# Define basic pricing logic
BASE_PRICE = 100  # Set a base price for the product
DISCOUNT_RANGE = 20  # Max discount

def negotiate_price(user_price):
    if user_price >= BASE_PRICE:
        return "Thank you for your offer! We can proceed with that price."
    elif user_price < BASE_PRICE - DISCOUNT_RANGE:
        return f"Unfortunately, we cannot accept that price. Our best offer is ${BASE_PRICE - DISCOUNT_RANGE}."
    else:
        counter_offer = BASE_PRICE - (BASE_PRICE - user_price) // 2
        return f"We appreciate your offer of ${user_price}. How about ${counter_offer} instead?"

def generate_response(user_message):
    # Use Google Generative AI to generate a response
    response = generate(prompt=user_message, model="YOUR_MODEL_NAME", key=API_KEY)  # Adjust parameters as needed
    return response['output']  # Modify according to the response structure

@app.route('/negotiate', methods=['POST'])
def negotiate():
    user_input = request.json.get('input')
    if user_input:
        # Check for user pricing input
        if "price" in user_input.lower():
            try:
                price = float(user_input.split("price")[-1].strip())
                negotiation_response = negotiate_price(price)
                return jsonify({"response": negotiation_response})
            except ValueError:
                return jsonify({"error": "Invalid price format."}), 400
        
        # Generate response from AI model
        ai_response = generate_response(user_input)
        return jsonify({"response": ai_response})

    return jsonify({"error": "No input provided."}), 400

if __name__ == '__main__':
    app.run(debug=True)
