from flask import Flask, request, jsonify
from flask_cors import CORS
from config import collection, logger
from utils.mongo_ops import save_user_data, save_chat_message


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
CORS(app)

@app.route('/')
def index():
    return "Hello World"

@app.route("/register_user", methods=["POST"])
def register_user():
    try:
        data = request.json
        address_data = data.get('address')
        monthly_bill = data.get('monthly_bill')
        
        payload = {
            "address_data": address_data,
            "monthly_bill": monthly_bill,
        }
        user = save_user_data(collection, payload)
        logger.info(f"User registered with user_id {user.inserted_id}")
        return jsonify({"status": True, "user_id": str(user.inserted_id)}), 200
    except Exception as e:
        error_message = f"Error in register_user: {str(e)}"
        logger.error(error_message)
        return jsonify({"status": False, "message": "Internal server error", "error": str(e)}), 500

@app.route("/save_chat", methods=["POST"])
def save_chat():
    try:
        data = request.json
        user_id = data.get('user_id')
        message = data.get('message')
        
        if not user_id or not message:
            return jsonify({"status": False, "message": "user_id and message are required"}), 400
        
        payload = {
            "user_id": user_id,
            "message": message,
        }
        result = save_chat_message(collection, payload)
        logger.info(f"Chat saved for user_id {user_id}")
        return jsonify({"status": True, "message": "Chat saved successfully"}), 200
    except Exception as e:
        error_message = f"Error in save_chat: {str(e)}"
        logger.error(error_message)
        return jsonify({"status": False, "message": "Internal server error", "error": str(e)}), 500

# def add_message_to_chat(user_id, msg):
#     update_chat(collection, user_id, msg)

# def get_stream_chat_completion(user_id):
#     messages = get_chat_history(user_id, collection)
#     messages.insert(0, {"role": "system", "content": instructions})

#     openai_stream = client.chat.completions.create(
#         model="gpt-4o",
#         messages=messages,
#         temperature=0.01,
#         stream=True
#     )
#     final_text = ""
#     token_number = 0
#     for event in openai_stream:
#         if hasattr(event.choices[0].delta, "content"):
#             current_response = event.choices[0].delta.content
#             if current_response:
#                 final_text += current_response
#                 token_number += 1
#                 yield json.dumps({
#                     "token_number": token_number,
#                     "data": current_response,
#                     "last_token": False,
#                 }).encode('utf-8') + b'\n\n'
#     add_message_to_chat(user_id, {"role": "assistant", "content": final_text})
#     yield json.dumps({
#         "token_number": token_number,
#         "last_token": True,
#         "final_text": final_text
#     }).encode('utf-8') + b'\n\n'

# @app.route("/chat_sunny", methods=["POST"])
# def chat_sunny():
#     try:
#         data = request.json
#         user_msg = data.get('content', '')
#         user_id = data.get('userId')
#         context = {"role": "user", "content": user_msg}
#         add_message_to_chat(user_id, context)
#         logger.info(f"Chat context for user_id {user_id}: {context}")
#         return Response(get_stream_chat_completion(user_id), content_type='text/event-stream')
#     except Exception as e:
#         error_message = f"Error in stream_chat_completion for user_id {user_id}: {str(e)}"
#         logger.error(error_message)
#         return jsonify({"status": False, "message": "Internal server error", "error": str(e)}), 500


if __name__ == '__main__':
    print("WebSocket Server is running with Redis")
    Flask.run(app, host='0.0.0.0', port=80, debug=True)
    print("WebSocket Server is running with Redis")