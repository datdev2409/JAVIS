import os
import json
import boto3
import urllib3
from urllib.parse import urlencode
import google.generativeai as genai
from dynamodb import db_create_transactions
from prompts import system_prompts


def get_model_response(message):
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_prompts,
    )

    response = model.generate_content(
        message,
        generation_config=genai.types.GenerationConfig(
            temperature=0,
            response_mime_type="application/json",
        ),
    )
    return response


def send_message(recipient_id, message):
    access_token = os.environ.get("FB_MESSENGER_ACCESS_TOKEN")
    query_params = urlencode(
        {
            "recipient": json.dumps({"id": recipient_id}),
            "message": json.dumps({"text": message}),
            "messaging_type": "RESPONSE",
            "access_token": access_token,
        }
    )
    response = urllib3.request(
        "POST",
        f"https://graph.facebook.com/v21.0/222579127613583/messages?" + query_params,
    )
    print(response.data)


def lambda_handler(event, context):
    print(event)
    http = event.get("requestContext", {}).get("http", {})

    request_path = http.get("path", "")
    request_method = http.get("method", "")

    print(request_path, request_method)

    # Handle Webhook Verification Request
    if request_path == "/webhooks" and request_method == "GET":
        query_string = event.get("queryStringParameters")
        if query_string.get("hub.mode", "") == "subscribe":
            challenge = query_string.get("hub.challenge", "")
            token = query_string.get("hub.verify_token", "")

            if token == os.environ.get("FB_MESSENGER_VERIFY_TOKEN"):
                return {"statusCode": 200, "body": challenge}
            else:
                return {"statusCode": 403, "body": "Invalid Token"}

    # Handle Webhook Event Notification
    if request_path == "/webhooks" and request_method == "POST":
        body = json.loads(event.get("body", "{}").replace("'", '"'))

        message = body.get("entry")[0]["messaging"][0]["message"].get(
            "text", "Send attachment"
        )
        sender_id = body.get("entry")[0]["messaging"][0]["sender"].get("id")

        model_output = get_model_response(message)
        print(model_output)

        transactions = json.loads(model_output.candidates[0].content.parts[0].text).get(
            "transactions"
        )
        print(transactions)
        db_create_transactions(transactions)

        response = json.loads(model_output.text).get(
            "message", "Something went wrong!!"
        )

        send_message(sender_id, response)

        return {"statusCode": 200, "body": "Received Message: " + message}

    return {"statusCode": 200, "body": json.dumps("Hello from Lambda!")}
