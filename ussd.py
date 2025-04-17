from flask import Flask, request
import africastalking
import os
import requests
import logging

app = Flask(__name__)
username = "sandbox"
api_key = "atsk_7aaff39211444cb09b2de388b27e11d43e47f68b8421c0b613523296abd27b4dcb630c38"
africastalking.initialize(username, api_key) 
sms = africastalking.SMS 

API_BASE_URL = "https://ticevents.onrender.com/api"  


logging.basicConfig(level=logging.DEBUG) 
 
@app.route('/ussd', methods=['POST', 'GET']) 
def ussd_callback():
    session_id = request.values.get("sessionId", "atsk_7aaff39211444cb09b2de388b27e11d43e47f68b8421c0b613523296abd27b4dcb630c38")
    service_code = request.values.get("serviceCode", "*384#")
    phone_number = request.values.get("phoneNumber", "+255694021848")
    text = request.values.get("text", "default")

    response = ""

    
    text_array = text.split('*')
    user_response = text_array[-1]

    if text == "":
       
        response = "CON Karibu TIC events management portal:\n"
        response += "Chagua sehemu unayotaka:\n"
        response += "1. Habari kuhusu event zijazo\n"
        response += "2. Habari kuhusu event zangu\n"
        response += "3. Huduma kwa wateja\n"

    elif text == "1":
       
        events = get_upcoming_events()
        logging.debug(f"Fetched events: {events}")
        if events:
            response = "CON Chagua jina la event unalo taka kujua taarifa zake:\n"
            for i, event in enumerate(events):
                response += f"{i + 1}. {event['title']}\n"
        else:
            response = "END Hakuna event zijazo kwa sasa.\n"

    elif text.startswith("1*"): 

        events = get_upcoming_events()
        event_index = int(user_response) - 1
        if 0 <= event_index < len(events):
            event = events[event_index]
            response = f"CON {event['title']}:\n"
            response += f"Mahali: {event['location']}\n"
            response += f"Mratibu: {event['organizer']}\n"
            response += f"Tarehe: {event['date']}\n"
            response += f"Gharama: {event['price']}\n"
            response += "1. Jisajili kwa event hii\n"
        else:
            response = "END Chaguo batili.\n"

    elif text.startswith("1*") and user_response == "1":
       
        response = "CON Ingiza jina lako:\n"

    elif text.startswith("1*") and len(text_array) == 3:
       
        response = "CON Ingiza barua pepe yako:\n"

    elif text.startswith("1*") and len(text_array) == 4:
       
        events = get_upcoming_events()
        event_index = int(text_array[1]) - 1
        if 0 <= event_index < len(events):
            event_id = events[event_index]['id']
            username = text_array[2]
            email = text_array[3]
            registration_status = register_for_event(event_id, username, email)
            if registration_status:
                response = "END Umejisajili kwa mafanikio.\n"
            else:
                response = "END Usajili umeshindikana. Tafadhali jaribu tena.\n"
        else:
            response = "END Chaguo batili.\n"

    elif text == "2":
       
        events = get_registered_events(phone_number)
        logging.debug(f"Fetched registered events: {events}")
        if events:
            response = "CON Hizi ni event ulizosajiliwa:\n"
            for i, event in enumerate(events):
                response += f"{i + 1}. {event['title']}\n"
        else:
            response = "END Hujasajiliwa kwa event yoyote.\n"

    elif text == "3":
        # Customer service
        response = "END Huduma kwa wateja: Piga simu +255123456789.\n"

    else:
        response = "END Chaguo batili.\n"

    return response

def get_upcoming_events():
    try:
        response = requests.get(f"{API_BASE_URL}/events/")
        logging.debug(f"API response: {response.status_code} - {response.text}")
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except requests.RequestException as e:
        logging.error(f"Error fetching upcoming events: {e}")
        return []

def get_registered_events(phone_number):
    try:
        response = requests.get(f"{API_BASE_URL}/events/registered/", params={"phone_number": phone_number})
        logging.debug(f"API response: {response.status_code} - {response.text}")
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except requests.RequestException as e:
        logging.error(f"Error fetching registered events: {e}")
        return []

def register_for_event(event_id, username, email):
    try:
        response = requests.post(f"{API_BASE_URL}/events/{event_id}/register/", data={"username": username, "email": email})
        logging.debug(f"API response: {response.status_code} - {response.text}")
        return response.status_code == 201
    except requests.RequestException as e:
        logging.error(f"Error registering for event: {e}")
        return False

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT"))