from flask import Blueprint, request, session,jsonify
import openai
from ..utils import chaaracter_validation
from openai.error import RateLimitError
# import os
# from dotenv import load_dotenv

# load_dotenv(".env")




conversation = Blueprint("interraction", __name__, url_prefix="/api/conversation")


# gpt4 route that handles user inputs and GPT-4 API interactions.
@conversation.route('/prompt', methods=['GET', 'POST'])
def gpt4():
    """
    Process user input using the GPT-4 API and return the response as a JSON object.

    :return: JSON object with the response from the GPT-4 API
    # """
    # user_input = request.args.get('user_input') if request.method == 'GET' else request.form['user_input']
    
    req = request.get_json()
    user_input = chaaracter_validation(user_input= req.get("user_input"))
    messages = [{"role": "user", "content": user_input}]
    # this would be where the validation for the user character limit according to their credit score would be implemented

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=1
        )  #THIS IS WHERE GPT-4 BRINGS THE RESPONSE
        content = response.choices[0].message["content"]
    except RateLimitError:
        content = "The server is experiencing a high volume of requests. Please try again later."

    return jsonify(content=content)