from flask import Blueprint, request, session, jsonify, Response
import openai
from ..utils import chaaracter_validation, requires_auth, query_one_filtered
from openai.error import RateLimitError
from collections import defaultdict

conversation = Blueprint("interraction", __name__, url_prefix="/api/chat")

chat_log = defaultdict(list)
def generate_chat_completion(message):
    """
    Generates a chat completion using the GPT-3.5-turbo model from OpenAI.

    Args:
        message (str): The user input message for the chat completion.

    Returns:
        str: The content of the generated response as a string.

    Example:
        message = "Hello, how are you?"
        response = generate_chat_completion(message)
        print(response)

        Expected Output:
        "Fine, thank you!"
    """
    messages = [
        # {
        #     "role": "system",
        #     "content": "for context puposes my previous : what is Javascript?"
        # },
        {
            "role": "user",
            "content": message
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.5,
        max_tokens=200
    )
    return response["choices"][0]["message"]["content"].strip("\n").strip()




#  completion route that handles user inputs and GPT-4 API interactions.
@conversation.route('/completions', methods=[ 'POST'])
@requires_auth(session)
def interractions(user_id):
    """
    Process user input using the GPT-4 API and return the response as a JSON object.

    :return: JSON object with the response from the GPT-4 API
    """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        req = request.get_json()
        if 'user_input' not in req:
            return jsonify({"message": "Invalid request! Missing 'user_input' key."}), 400
        prompt = req['user_input']
    else:
        return jsonify({"message": "Content-Type not supported!"}), 406
    
    
    converse = chat_log.__getitem__(user_id)  # if this doesn't exist it will initialize a new entry in the cache memory chat_log
    converse.append(f"user: {prompt }")
    text_prompt = "\n".join(converse)
    
    
    try:
        result= generate_chat_completion(message=text_prompt)
        converse.append(f"AI: {result}")
        return Response(result, content_type="text/plain"), 201
    except RateLimitError:
        return jsonify(content="The server is experiencing a high volume of requests. Please try again later."), 400
    except Exception as e:
        # print(e)
        return jsonify(content="An unexpected error occurred. Please try again later."), 500
