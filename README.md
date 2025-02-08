---

## **Arcadia Discord Bot** 🤖  
A powerful and flexible Discord bot for managing the **Arcadia Discord Server**, featuring moderation, welcome messages, a tester system, and priority role management.  

---

## **🌟 Features**  
✔️ **Welcome System** – Set a custom welcome channel & test it anytime.  
✔️ **Tester System** – Store and manage bot testing data dynamically.  
✔️ **Priority 1 Role** – Special unrestricted control for server owners.  
✔️ **Moderation Tools** – Commands for muting/unmuting members.  
✔️ **English-Only Chat Filter** – Auto-detects & deletes non-English messages.  
✔️ **Utility Commands** – Ping, info, and more!  

---

## **🛠️ Installation & Setup**  

### **1️⃣ Clone the Repository**  
```sh
git clone https://github.com/YourUsername/Arcadia-Bot.git
cd Arcadia-Bot
```

### **2️⃣ Install Dependencies**  
```sh
pip install -r requirements.txt
```

### **3️⃣ Set Up Configuration Files**  
- **`config.json`** – Stores tester role settings.  
- **`welcome_config.json`** – Saves welcome channel preferences.  
- **`test-data.json`** – Logs bot testing data.  

### **4️⃣ Run the Bot**  
```sh
python bot.py
```

*(Ensure you replace `"YOUR_BOT_TOKEN"` in `bot.py` with your actual bot token.)*  

---

## **📜 Commands List**  

### **👋 Welcome System**  
| Command | Description |
|---------|------------|
| `!setwelcome #channel` | Sets the welcome message channel. |
| `!welcometest` | Sends a test welcome message. |

### **🧪 Tester System**  
| Command | Description |
|---------|------------|
| `!settesterrole @role` | Sets the tester role. |
| `!adddata <key> <value>` | Adds test data. |
| `!getdata <key>` | Retrieves a test entry. |
| `!alldata` | Displays all test data. |
| `!deletedata <key>` | Deletes a test entry. |

### **🔧 Moderation**  
| Command | Description |
|---------|------------|
| `!mute @user [reason]` | Mutes a user. |
| `!unmute @user` | Unmutes a user. |

### **🔹 Utility**  
| Command | Description |
|---------|------------|
| `!ping` | Checks bot latency. |
| `!hello` | Greets the user. |
| `!info` | Provides support contact. |

---

## **🔒 Security & Permissions**  
- The **"Priority 1" role** (set manually) has **full control over the bot**.  
- Only **authorized testers** (via `!settesterrole`) can modify testing data.  
- **Admin-only** commands for setting welcome channels and tester roles.  

---

## **🛡️ License**  
📜 **Licensed under the [MIT License](LICENSE).**  
*(You are free to use, modify, and distribute this bot, but credit must be given to the original creator.)*  

---

## **👥 Contributors & Support**  
💡 Want to help improve the bot? Open an **issue** or submit a **pull request**!  
📧 Need help? Contact **[Your Discord Tag]** or join the **Arcadia Server**.  

---

🚀 **Let's make Arcadia Bot even better together!** 😎🔥  

---
