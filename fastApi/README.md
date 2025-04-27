# 📱 USSD Demo Service using FastAPI

This is a simple USSD application demo built with FastAPI.  
It shows developers how to structure multi-level USSD menus (Main Menu, Submenus) and handle user navigation.

---

## 🚀 How to Run

1. Install FastAPI and Uvicorn:

   ```bash
   pip install fastapi uvicorn
   ```

2. Start the server:

   ```bash
   uvicorn FastApi_ussd:app --host 0.0.0.0 --port 8000
   ```

3. Your USSD endpoint will be available at:

   ```
   POST http://your-server/ussd
   ```

4. use ngrok or ddeploy to a server for publick access.

---

# 🧠 Developer Notes:

### How menu levels work:

| Level            | Meaning                                                |
| :--------------- | :----------------------------------------------------- |
| `text = ""`      | **Main Menu** (no input yet)                           |
| `text = "1"`     | User selected **Option 1** from Main Menu              |
| `text = "2"`     | User selected **Option 2** and waiting to enter amount |
| `text = "2*500"` | User entered amount **500**                            |
| `text = "3"`     | User selected **Option 3** Support Menu                |
| `text = "3*1"`   | User selected **Call Support** inside Support Menu     |
| `text = "3*2"`   | User selected **SMS Support**                          |
| `text = "3*3"`   | User selected **Back to Main Menu**                    |

---

# 🎯 Important:

- Always check **how deep** you are in the `text_array` (how many `*` parts).
- Always use `CON` if you want to **keep user in session**.
- Always use `END` if you want to **end the session** after action.

---

# 📈 Example USSD Flow

```mermaid
flowchart TD
    A(User dials USSD code) --> B{Main Menu}
    B -->|1| C[Check Balance -> END Your balance]
    B -->|2| D[Buy Airtime -> Ask for Amount]
    D --> E[User enters Amount -> END Confirm purchase]
    B -->|3| F{Support Menu}
    F -->|1| G[Call Support -> END Call message]
    F -->|2| H[SMS Support -> END SMS message]
    F -->|3| B
    B -->|4| I[Exit -> END Thank you message]


---

# 🙌 Contribution

Feel free to fork and extend it!
This template is made for any developers wanting to understand USSD flows faster.

```

---

### 🔥 Quick Summary:

- YES ✅ your format is README-ready.
- Just add a title, maybe a "How to Run", and you're perfect.
- Emojis and formatting are good and professional now.
- Markdown tables and bullet points — excellent for documentation.

---

```

```
