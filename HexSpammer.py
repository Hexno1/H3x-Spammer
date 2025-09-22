# This Gui Was CodedBy Hex
# Any Question Contact ME On Discord : ki9f

import tkinter as tk
from tkinter import font, messagebox, ttk
import requests
import threading
import time
import os
import datetime
import webbrowser
import re
from colorama import Fore, init

init(autoreset=True)

class HexSpammer:
    def __init__(self, root):
        self.root = root
        self.root.title("Hex -  WebhookSpammer / Deleter / Info")
        self.root.geometry("1300x900")
        self.root.configure(bg="#000000")
        self.root.resizable(True, True)


        self.custom_font = font.Font(family="Segoe UI", size=10)
        self.bold_font = font.Font(family="Segoe UI", size=10, weight="bold")


        self.webhook_url = tk.StringVar()
        self.spam_message = tk.StringVar(value="Spam message")
        self.spam_delay_ms = tk.StringVar(value="1000") 
        self.running = False
        self.spam_thread = None


        self.root.columnconfigure(0, weight=1)
        for i in range(4):
            self.root.rowconfigure(i, weight=1 if i == 2 else 0)


        self.create_widgets()

    def create_widgets(self):

        title_frame = tk.Frame(self.root, bg="#1a1a1a")
        title_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        title_frame.columnconfigure(1, weight=1)

        logo = tk.Label(title_frame, text="H", font=("Arial", 24), bg="#1a1a1a", fg="#FF0000")
        logo.grid(row=0, column=0, padx=5, sticky="w")

        title_label = tk.Label(
            title_frame,
            text="Hex - Webhook Spammer",
            font=("Segoe UI", 16, "bold"),
            bg="#1a1a1a",
            fg="#ffffff"
        )
        title_label.grid(row=0, column=1, sticky="w", padx=5)


        notebook_frame = tk.Frame(self.root, bg="#1a1a1a")
        notebook_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        notebook_frame.columnconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background="#1a1a1a", borderwidth=0)
        style.configure("TNotebook.Tab", 
                       background="#2d2d2d", 
                       foreground="#ffffff",
                       font=self.custom_font,
                       padding=[15, 8])
        style.map("TNotebook.Tab", 
                 background=[("selected", "#FF0000")],
                 foreground=[("selected", "white")])

        self.tab_control = ttk.Notebook(notebook_frame)
        self.tab_control.grid(row=0, column=0, sticky="ew")

        self.info_frame = tk.Frame(self.tab_control, bg="#1a1a1a")
        self.spammer_frame = tk.Frame(self.tab_control, bg="#1a1a1a")
        self.remover_frame = tk.Frame(self.tab_control, bg="#1a1a1a")
        

        self.tab_control.add(self.info_frame, text="Info")
        self.tab_control.add(self.spammer_frame, text="Spammer")
        self.tab_control.add(self.remover_frame, text="Remover")


        self.create_spammer_tab()
        self.create_remover_tab()
        self.create_info_tab()

        log_frame = tk.Frame(self.root, bg="#1a1a1a")
        log_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=5)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        self.log_text = tk.Text(
            log_frame, 
            bg="#2d2d2d", 
            fg="#ffffff", 
            font=("Consolas", 9),
            wrap=tk.WORD, 
            height=6,
            relief="flat"
        )
        self.log_text.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        self.log_text.config(state="disabled")

        scrollbar = tk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log_text.config(yscrollcommand=scrollbar.set)

        status_frame = tk.Frame(self.root, bg="#1a1a1a", height=20)
        status_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=5)
        status_frame.columnconfigure(0, weight=1)

        self.status_label = tk.Label(
            status_frame, 
            text="Hex Log", 
            bg="#1a1a1a", 
            fg="#888888", 
            font=("Segoe UI", 8)
        )
        self.status_label.grid(row=0, column=0, sticky="e")

    def create_spammer_tab(self):
        frame = self.spammer_frame
        card = tk.Frame(frame, bg="#2d2d2d", padx=30, pady=30, relief="solid", bd=1)
        card.pack(expand=True, fill="both", padx=20, pady=20)
        card.columnconfigure(0, weight=1)

        tk.Label(card, text="Webhook URL", bg="#2d2d2d", fg="#ffffff", font=self.custom_font).pack(pady=5)
        url_entry = tk.Entry(card, textvariable=self.webhook_url, width=60, bg="#3a3a3a", fg="white", insertbackground="white", font=self.custom_font)
        url_entry.pack(pady=5)


        view_info_btn = tk.Button(
            card,
            text="🔍 View Webhook Info",
            command=self.view_webhook_info,
            bg="#0400fd",
            fg="white",
            relief="flat",
            font=self.custom_font
        )
        view_info_btn.pack(pady=10)


        self.info_display = tk.Text(card, height=8, width=60, bg="#3a3a3a", fg="#00ff99", font=("Consolas", 9), wrap=tk.WORD)
        self.info_display.pack(pady=10)
        self.info_display.insert(tk.END, "Paste a webhook and click 'View Info' to see details.")
        self.info_display.config(state="disabled")

        tk.Label(card, text="Message to Spam", bg="#2d2d2d", fg="#ffffff", font=self.custom_font).pack(pady=5)
        message_entry = tk.Entry(card, textvariable=self.spam_message, width=60, bg="#3a3a3a", fg="white", font=self.custom_font)
        message_entry.pack(pady=5)

        tk.Label(card, text="Delay (ms)", bg="#2d2d2d", fg="#ffffff", font=self.custom_font).pack(pady=(15, 5))
        delay_entry = tk.Entry(card, textvariable=self.spam_delay_ms, width=10, bg="#3a3a3a", fg="white", font=self.custom_font, justify="center")
        delay_entry.pack(pady=5)


        start_btn = tk.Button(
            card,
            text="🚀 START SPAMMING",
            command=self.start_spamming,
            bg="#00ff00",
            fg="white",
            relief="flat",
            font=("Segoe UI", 12, "bold"),
            padx=20,
            pady=10
        )
        start_btn.pack(pady=(15, 5))


        stop_btn = tk.Button(
            card,
            text="⏹️ STOP SPAMMING",
            command=self.stop_spamming,
            bg="#ff0033",
            fg="white",
            relief="flat",
            font=("Segoe UI", 12, "bold"),
            padx=20,
            pady=10
        )
        stop_btn.pack(pady=(5, 15))

        self.spam_status_label = tk.Label(card, text="Status: Idle", bg="#2d2d2d", fg="#888888", font=self.custom_font)
        self.spam_status_label.pack(pady=5)

    def create_remover_tab(self):
        frame = self.remover_frame
        card = tk.Frame(frame, bg="#2d2d2d", padx=30, pady=30, relief="solid", bd=1)
        card.pack(expand=True, fill="both", padx=20, pady=20)
        card.columnconfigure(0, weight=1)

        tk.Label(card, text="Webhook URL to Delete", bg="#2d2d2d", fg="#ffffff", font=self.custom_font).pack(pady=5)
        delete_url_entry = tk.Entry(card, textvariable=self.webhook_url, width=60, bg="#3a3a3a", fg="white", insertbackground="white", font=self.custom_font)
        delete_url_entry.pack(pady=5)

        delete_btn = tk.Button(
            card,
            text="🗑️ DELETE WEBHOOK",
            command=self.delete_webhook,
            bg="#dc143c",
            fg="white",
            relief="flat",
            font=("Segoe UI", 12, "bold"),
            padx=20,
            pady=10
        )
        delete_btn.pack(pady=15)

        self.delete_status_label = tk.Label(card, text="", bg="#2d2d2d", fg="#ffcc00", font=self.custom_font)
        self.delete_status_label.pack(pady=5)

    def create_info_tab(self):
        frame = self.info_frame
        center_frame = tk.Frame(frame, bg="#1a1a1a")
        center_frame.pack(expand=True, fill="both", padx=20, pady=20)
        center_frame.columnconfigure(0, weight=1)

        card = tk.Frame(center_frame, bg="#2d2d2d", padx=30, pady=30, relief="solid", bd=1)
        card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        card.columnconfigure(0, weight=1)

        info_text = (
            "Hex WebhookSpammer v1.0\n"
            "\n"
            "Full Access To HexSpammer\n"
            "\n"
            "Features:\n"
            "- Spam until you press STOP (red button)\n"
            "- Instantly delete webhooks\n"
            "- View webhook info (name, channel, guild, avatar, token*)\n"
            "- Real-time logging & status updates\n"
            "- Modern, responsive dark UI\n"
            "- Customizable delay between messages (in ms)\n\n"
            "Github: "
        )

        info_label = tk.Label(
            card,
            text=info_text,
            bg="#2d2d2d",
            fg="#ffffff",
            justify="left",
            wraplength=550,
            font=self.custom_font
        )
        info_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        discord_link = tk.Label(
            card,
            text="Github.com/hexno1",
            bg="#2d2d2d",
            fg="#1A81C5",
            font=self.custom_font,
            cursor="hand2"
        )
        discord_link.grid(row=1, column=0, sticky="w", padx=30, pady=2)
        discord_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/hexno1"))

    def validate_webhook(self, url):
        pattern = r'^https://discord\.com/api/webhooks/[0-9]+/[a-zA-Z0-9_-]+$'
        return re.match(pattern, url) is not None

    def log(self, message):
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        full_message = f"[{timestamp}] {message}"
        print(full_message)

        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, full_message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def stop_spamming(self):
        if self.running:
            self.running = False
            self.spam_status_label.config(text="Status: Stopping...", fg="#ffcc00")
            self.log("[STOP] User requested to stop spamming")
        else:
            self.log("[INFO] Spamming is not currently running")

    def start_spamming(self):
        url = self.webhook_url.get().strip()
        message = self.spam_message.get().strip()

        if not url:
            messagebox.showerror("Error", "❌ Webhook URL is required")
            self.log("[ERROR] Webhook URL is empty")
            return
        if not self.validate_webhook(url):
            messagebox.showerror("Error", "❌ Invalid Webhook URL")
            self.log("[ERROR] Invalid Webhook URL format")
            return
        if not message:
            messagebox.showerror("Error", "❌ Message cannot be empty")
            self.log("[ERROR] Spam message is empty")
            return


        try:
            delay_ms = int(self.spam_delay_ms.get())
            if delay_ms < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "❌ Delay must be a positive number (in milliseconds)")
            self.log("[ERROR] Invalid delay value")
            return

        if self.running:
            messagebox.showinfo("Warning", "⚠️ Spamming is already in progress")
            return

        self.running = True
        self.spam_status_label.config(text="Status: Running...", fg="#00ff00")

        self.spam_thread = threading.Thread(target=self.spam_loop, args=(url, message, delay_ms), daemon=True)
        self.spam_thread.start()
        self.log(f"[START] Spamming started with {delay_ms}ms delay. Press STOP to halt.")

    def spam_loop(self, url, message, delay_ms):  
        sent_count = 0

        while self.running:
            try:
                response = requests.post(
                    url,
                    json={"content": message},
                    params={'wait': True}
                )
                if response.status_code in (200, 204):
                    sent_count += 1
                    self.log(f"[SUCCESS] Message #{sent_count} sent")
                elif response.status_code == 429:
                    retry_after = response.json().get('retry_after', 1)
                    self.log(f"[RATELIMIT] Waiting {retry_after}s")
                    time.sleep(retry_after)
                    continue
                else:
                    self.log(f"[ERROR] HTTP {response.status_code}")
            except Exception as e:
                self.log(f"[EXCEPTION] {str(e)}")

            time.sleep(delay_ms / 1000.0)


        self.root.after(0, self.spam_status_label.config, {"text": f"Status: Stopped ({sent_count} sent)", "fg": "#ff6b6b"})
        self.log(f"[STOPPED] Spamming halted. Total messages sent: {sent_count}")

    def delete_webhook(self):
        url = self.webhook_url.get().strip()
        if not url:
            messagebox.showerror("Error", "❌ Webhook URL is required")
            self.log("[ERROR] No URL provided for deletion")
            return
        if not self.validate_webhook(url):
            messagebox.showerror("Error", "❌ Invalid Webhook URL")
            self.log("[ERROR] Invalid URL for deletion")
            return

        confirm = messagebox.askyesno("Confirm", "⚠️ Are you sure you want to DELETE this webhook? This cannot be undone.")
        if not confirm:
            return

        try:
            response = requests.delete(url)
            if response.status_code == 204:
                self.delete_status_label.config(text="✅ Webhook Deleted Successfully", fg="#00ff00")
                self.log("[SUCCESS] Webhook deleted")
                messagebox.showinfo("Success", "✅ Webhook has been deleted!")
            else:
                self.delete_status_label.config(text=f"❌ Failed (Status: {response.status_code})", fg="#ff0000")
                self.log(f"[ERROR] Failed to delete webhook. Status: {response.status_code}")
                messagebox.showerror("Error", f"❌ Failed to delete webhook. Status: {response.status_code}")
        except Exception as e:
            self.delete_status_label.config(text=f"❌ Error: {str(e)}", fg="#ff0000")
            self.log(f"[EXCEPTION] Error deleting webhook: {str(e)}")
            messagebox.showerror("Error", f"❌ An error occurred: {str(e)}")

    def view_webhook_info(self):
        url = self.webhook_url.get().strip()
        if not url:
            messagebox.showerror("Error", "❌ Please enter a webhook URL")
            self.log("[ERROR] No URL for info fetch")
            return

        if not self.validate_webhook(url):
            messagebox.showerror("Error", "❌ Invalid Webhook URL")
            self.log("[ERROR] Invalid URL format for info")
            return

        try:
            self.log(f"[INFO] Fetching webhook info...")
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()

                info_lines = [
                    f"Name: {data.get('name', 'N/A')}",
                    f"ID: {data.get('id', 'N/A')}",
                    f"Channel ID: {data.get('channel_id', 'N/A')}",
                    f"Guild ID: {data.get('guild_id', 'N/A')}",
                    f"Avatar Hash: {data.get('avatar', 'None')}",
                    f"Token: {data.get('token', 'N/A')}",
                    f"Type: {'Incoming' if data.get('type') == 1 else 'Unknown'}",
                    f"Application ID: {data.get('application_id', 'None')}"
                ]

                display_text = "\n".join(info_lines)

                self.info_display.config(state="normal")
                self.info_display.delete(1.0, tk.END)
                self.info_display.insert(tk.END, display_text)
                self.info_display.config(state="disabled")

                self.log("[SUCCESS] Webhook info fetched and displayed")
            else:
                self.log(f"[ERROR] Failed to fetch info. Status: {response.status_code}")
                messagebox.showerror("Error", f"❌ Failed to fetch info. HTTP {response.status_code}")
        except Exception as e:
            self.log(f"[EXCEPTION] Error fetching info: {str(e)}")
            messagebox.showerror("Error", f"❌ An error occurred: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = HexSpammer(root)
    root.mainloop()