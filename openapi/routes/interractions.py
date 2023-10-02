from typing import List
from flask import Blueprint, request, session, jsonify, Response
import openai
from openapi.utils import get_current_analytics, handle_check_credits
from openai.error import RateLimitError
from collections import defaultdict
import os

conversation = Blueprint("interraction", __name__, url_prefix="/api/chat")

chat_log = defaultdict(list)
def generate_chat_completion(message: str, chat_logs: List[str]) -> str:
    """
    Generates a chat completion using the GPT-3.5-turbo model from OpenAI.

    Args:
        message (str): The user input message for the chat completion.
        chat_logs (List[str]): A list of chat logs containing previous messages.

    Returns:
        str: The content of the generated response as a string.
    """
    messages = [
        {"role": "system", "content": "\n".join(chat_logs)},
        {"role": "user", "content": message}
    ]

    current_analytics = get_current_analytics()
    daily_limit = int(os.getenv("DAILY_LIMIT"))

    if current_analytics.openai_requests < daily_limit:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.5,
            max_tokens=200
        )

        current_analytics.openai_requests += 1
        current_analytics.update()

        return response["choices"][0]["message"]["content"].strip("\n").strip()

    return "Daily limit reached, please try again tomorrow"


#  completion route that handles user inputs and GPT-4 API interactions.
@conversation.route("/completions", methods=["POST"])
@handle_check_credits(session)
def interractions(user):
    """
    Process user input using the GPT-4 API and return the response as a JSON object.

    :param user: The user object containing information about the current user.
    :return: JSON object with the response from the GPT-4 API
    """
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        req = request.get_json()
        if "user_input" and "history" not in req:
            return (
                jsonify({"message": "Invalid request! Missing 'user_input' or 'history' key."}),
                400,
            )
        history = req.get("history")
        user_input = req.get("user_input")
    else:
        return jsonify({"message": "Content-Type not supported!"}), 406
    
    if not isinstance(history, list) and not isinstance(user_input, str): 
        return (
            jsonify({"message": "Invalid data type for 'history' or 'user_input' field. Must be a valid array or string."}),
            400,
        )
    
    converse = chat_log.__getitem__(user.id)
    converse.clear()
    converse.append(history)
    
    try:
        result= generate_chat_completion(message=user_input, chat_logs=history)
        # converse.append(f"AI: {result}")
        user.credits -= 1
        user.update()
        return jsonify({"message":result}), 201
    except RateLimitError:
        return (
            jsonify(
                content="The server is experiencing a high volume of requests. Please try again later."
            ),
            400,
        )
    except Exception as e:
        return jsonify(content="An unexpected error occurred. Please try again later."), 500


@conversation.route("/", methods=["GET"])
def cron():
    return {"hello":"world"}
