from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.post("/ussd", response_class=PlainTextResponse)
async def ussd_callback(request: Request):
    """
    USSD Menu Demo for Developers
    - Handle multi-level menu navigation
    - Differentiate Main Menu and Submenus
    - Use CON (continue) and END (end session) properly
    """

    try:
        # Extract USSD form data
        form_data = await request.form()
        session_id = form_data.get("sessionId", "")
        phone_number = form_data.get("phoneNumber", "")
        text = form_data.get("text", "")
    except Exception:
        # Handle invalid request format
        return PlainTextResponse("END Error: Invalid request data", status_code=400)

    try:
        # Parse input into menu levels
        text_array = text.split("*") if text else []
        response = ""

        # ========== MAIN MENU ==========
        if not text_array or text_array == [""]:
            response = (
                "CON Welcome to the Demo USSD Service\n"
                "1. Check Balance\n"
                "2. Buy Airtime\n"
                "3. Contact Support\n"
                "4. Exit"
            )

        # ========== OPTION 1: Check Balance ==========
        elif text_array[0] == "1":
            if len(text_array) == 1:
                # User selected 1 from Main Menu
                response = "END Your balance is KES 1,000. Thank you."

        # ========== OPTION 2: Buy Airtime ==========
        elif text_array[0] == "2":
            if len(text_array) == 1:
                # SUBMENU LEVEL 1: Ask user to enter amount
                response = "CON Enter amount to buy:"
            elif len(text_array) == 2:
                # SUBMENU LEVEL 2: Process amount
                amount = text_array[1]
                if amount.isdigit():
                    response = f"END You have bought airtime worth KES {amount}. Thank you."
                else:
                    response = "END Invalid amount. Please enter numbers only."

        # ========== OPTION 3: Contact Support ==========
        elif text_array[0] == "3":
            if len(text_array) == 1:
                # SUBMENU LEVEL 1: Show support options
                response = (
                    "CON Support Menu:\n"
                    "1. Call Support\n"
                    "2. SMS Support\n"
                    "3. Back to Main Menu"
                )
            elif len(text_array) == 2:
                # SUBMENU LEVEL 2: Handle support choices
                if text_array[1] == "1":
                    response = "END Our support team will call you shortly."
                elif text_array[1] == "2":
                    response = "END We have sent you a support SMS."
                elif text_array[1] == "3":
                    # Going back to Main Menu manually
                    response = (
                        "CON Welcome to the Demo USSD Service\n"
                        "1. Check Balance\n"
                        "2. Buy Airtime\n"
                        "3. Contact Support\n"
                        "4. Exit"
                    )
                else:
                    response = "END Invalid support option. Please try again."

        # ========== OPTION 4: Exit ==========
        elif text_array[0] == "4":
            response = "END Thank you for using our service."

        # ========== INVALID INPUT ==========
        else:
            response = "END Invalid option. Please try again."

    except Exception:
        response = "END Error: Unable to process request. Please try again."

    return PlainTextResponse(response, status_code=200)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
