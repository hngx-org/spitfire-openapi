from flask import Blueprint, request, session, jsonify
import openai
from ..utils import chaaracter_validation, requires_auth
from openai.error import RateLimitError
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage


conversation = Blueprint("interraction", __name__, url_prefix="/api/chat")


#  gpt4 route that handles user inputs and GPT-4 API interactions.
@conversation.route('/completions', methods=[ 'POST'])
# @requires_auth(session)
def interractions():
    """
    Process user input using the GPT-4 API and return the response as a JSON object.

    :return: JSON object with the response from the GPT-4 API
    """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        req = request.get_json()
        prompt = req['user_input']
    else:
        return jsonify({"message": "Content-Type not supported!"}), 406

    text = chaaracter_validation(prompt)



    messages = [
        {"role": "user", 
         "content": text
         }, 
         {"role": "system",
          "content": "you are a professional in this field"
          }
          ]
    # this would be where the validation for the user character limit according to their credit score would be implemented


    try:
        print("response")
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            messages=messages,
            temperature=0.6,
            stream = True
        ) 
        content = response.choices[0]["message"]["content"].strip("\n").strip()

        for res in response:
            print(res)
    except RateLimitError as Exc:
        print(str(Exc))
        return jsonify(content = "The server is experiencing a high volume of requests. Please try again later."), 400

    return jsonify(content=content),201


# @conversation.route("/query", methods=["POST"])
# def query_gpt():
#     llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

#     print(llm( [HumanMessage(content="what is 2+2")]))
#     return {"message": "success"}, 200