# 🚀 Hex WebhookSpammer — GUI Tool for Discord Webhooks

> **Coded by Hex** | Contact: `ki9f` on Discord  
> GitHub: [github.com/hexno1](https://github.com/hexno1)

---

## 📌 Overview

**Hex WebhookSpammer** is a sleek, modern, and powerful **GUI-based tool** built with Python and Tkinter for interacting with **Discord webhooks**. Whether you want to spam messages, delete webhooks, or fetch detailed webhook info — this tool has you covered.

Designed with a **dark-themed UI**, real-time logging, customizable delays, and intuitive controls, it’s perfect for developers, testers, or anyone needing full control over Discord webhooks — all from a desktop application.

---

## ✨ Features

✅ **Spam Messages**  
- Send unlimited messages until manually stopped  
- Customizable message content and delay (in milliseconds)  
- Real-time status & log updates  
- Automatic rate-limit handling (429 retry-after support)

✅ **Delete Webhooks**  
- Permanently delete any valid Discord webhook  
- Confirmation dialog to prevent accidents  
- Instant feedback on success/failure

✅ **View Webhook Info**  
- Fetch and display detailed webhook metadata:  
  - Name, ID, Channel ID, Guild ID  
  - Avatar hash, Token, Type, Application ID  
- Validate webhook URL format before fetching

✅ **Modern UI & UX**  
- Responsive dark theme with red accent highlights  
- Tabbed interface: `Spammer`, `Remover`, `Info`  
- Real-time console-style logging with timestamps  
- Clean, card-based layout with hover effects and visual feedback

✅ **Safety & Validation**  
- URL format validation using regex  
- Input sanitization and error handling  
- Threaded spamming to avoid UI freezing  
- Graceful stop mechanism

---

## 🖥️ Requirements

- Python 3.8+
- Required Libraries:
  ```bash
  pip install requests colorama
