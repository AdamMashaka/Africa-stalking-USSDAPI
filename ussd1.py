from flask import Flask, request
import africastalking
import os

app = Flask(__name__)


username = "sandbox"  
api_key = os.getenv("AT_API_KEY")  
africastalking.initialize(username, api_key) 
sms = africastalking.SMS 


students = {} 

@app.route('/ussd', methods=['POST', 'GET'])
def ussd_callback():

    session_id = request.values.get("sessionId", "")
    service_code = request.values.get("serviceCode", "*123#")
    phone_number = request.values.get("phoneNumber", "")
    text = request.values.get("text", "")

    response = ""

    if text == "":

        response = "CON Welcome to School Attendance System:\n"
        response += "1. Register Student\n"
        response += "2. Mark Attendance\n"
        response += "3. View Attendance\n"

    elif text == "1":
  
        response = "CON Enter the student's name to register:"

    elif text.startswith("1*"):

        student_name = text.split('*')[1]
        students[phone_number] = {"name": student_name, "attendance": []}
        response = f"END {student_name} has been successfully registered."

    elif text == "2":
    
        if phone_number in students:
            student_name = students[phone_number]["name"]
            students[phone_number]["attendance"].append("Present")
            response = f"END Attendance marked for {student_name}."
        else:
            response = "END You are not registered. Please register first."

    elif text == "3":
     
        if phone_number in students:
            student_name = students[phone_number]["name"]
            attendance_count = len(students[phone_number]["attendance"])
            response = f"END {student_name} has attended {attendance_count} classes."
        else:
            response = "END You are not registered. Please register first."

    else:
      
        response = "END Invalid input. Please try again."

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))