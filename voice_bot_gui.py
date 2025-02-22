import tkinter as tk
from tkinter import scrolledtext
from speech_to_text import listen_and_transcribe
from nlu import extract_intent, extract_entities
from response_generator import generate_response
from text_to_speech import speak_text
from backend import init_db, log_interaction
import threading
import time
from PIL import Image, ImageTk
import os

init_db()

class VoiceBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 Intelligent Voice Bot")
        self.root.geometry("720x600")
        self.root.configure(bg="#1e1e1e") 

        # Colors
        self.bg_color = "#1e1e1e"
        self.text_color = "#ffffff"
        self.bot_color = "#4CAF50" 
        self.user_color = "#1E88E5" 
        self.placeholder_color = "#888888"  

        # Title Label
        self.title_label = tk.Label(root, text="🤖 Intelligent Voice Bot", font=("Arial", 18, "bold"), bg=self.bg_color, fg=self.text_color)
        self.title_label.pack(pady=10)

        # Conversation Display (Scrollable)
        self.text_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=18, font=("Arial", 12), bg="#2b2b2b", fg=self.text_color, bd=0)
        self.text_display.pack(pady=10)
        self.text_display.config(state=tk.DISABLED)

        # Input Frame (Text Box + Send Button)
        self.input_frame = tk.Frame(root, bg=self.bg_color)
        self.input_frame.pack(pady=5, fill=tk.X, padx=20)

        # User Input Field with Placeholder
        self.user_input = tk.Entry(self.input_frame, font=("Arial", 14), width=50, bg="#333333", fg=self.placeholder_color, insertbackground="white", bd=2, relief="flat")
        self.user_input.insert(0, "Type your message here...")
        self.user_input.bind("<FocusIn>", self.clear_placeholder)
        self.user_input.bind("<FocusOut>", self.add_placeholder)
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Load icons
        self.send_icon = self.load_resized_image("assets/send_icon.png", (30, 30))
        self.mic_icon = self.load_resized_image("assets/mic_icon.png", (40, 40))  
        self.exit_icon = self.load_resized_image("assets/exit_icon.png", (30, 30))

        # Send Button (Inside Input Field)
        self.send_button = tk.Button(self.input_frame, image=self.send_icon, bg="#4CAF50", activebackground="#388E3C", bd=0, command=self.process_text_input)
        self.send_button.pack(side=tk.RIGHT, padx=5)

        # Buttons Frame (Mic + Exit)
        self.button_frame = tk.Frame(root, bg=self.bg_color)
        self.button_frame.pack(pady=10)

        # Mic Button (With Animation)
        self.speak_button = tk.Button(self.button_frame, image=self.mic_icon, text=" Speak", compound=tk.LEFT, font=("Arial", 12),
                                      bg="#1E88E5", fg="white", command=self.process_voice_input, activebackground="#1565C0", bd=0)
        self.speak_button.grid(row=0, column=0, padx=5)
        self.speak_button.bind("<Enter>", lambda e: self.speak_button.config(bg="#1976D2"))
        self.speak_button.bind("<Leave>", lambda e: self.speak_button.config(bg="#1E88E5"))

        self.exit_button = tk.Button(self.button_frame, image=self.exit_icon, text=" Exit", compound=tk.LEFT, font=("Arial", 12),
                                     bg="red", fg="white", command=root.quit, activebackground="#D32F2F", bd=0)
        self.exit_button.grid(row=0, column=1, padx=5)
        self.exit_button.bind("<Enter>", lambda e: self.exit_button.config(bg="#B71C1C"))
        self.exit_button.bind("<Leave>", lambda e: self.exit_button.config(bg="red"))

        # Typing Indicator
        self.typing_label = tk.Label(root, text="", font=("Arial", 12, "italic"), bg=self.bg_color, fg="lightgray")
        self.typing_label.pack()

    def load_resized_image(self, file_path, size):
        """Load and resize image safely."""
        if os.path.exists(file_path):
            img = Image.open(file_path)
            img = img.resize(size, Image.LANCZOS)  
            return ImageTk.PhotoImage(img)
        else:
            print(f"Warning: {file_path} not found.")
            return None  

    def clear_placeholder(self, event):
        """Clears placeholder text when the user clicks the entry."""
        if self.user_input.get() == "Type your message here...":
            self.user_input.delete(0, tk.END)
            self.user_input.config(fg=self.text_color)

    def add_placeholder(self, event):
        """Adds placeholder text if the entry is empty."""
        if not self.user_input.get():
            self.user_input.insert(0, "Type your message here...")
            self.user_input.config(fg=self.placeholder_color)

    def process_text_input(self):
        """Processes user input from the text box"""
        user_text = self.user_input.get().strip()
        if not user_text or user_text == "Type your message here...":
            return

        self.display_message("You: " + user_text, self.user_color)
        self.user_input.delete(0, tk.END)
        self.add_placeholder(None) 

        self.process_response(user_text)

    def process_voice_input(self):
        """Processes user input via voice with animation"""
        self.speak_button.config(bg="red") 
        self.speak_button.after(500, lambda: self.speak_button.config(bg="#1E88E5"))  

        self.display_message("🎤 Listening...", "#FFD700")  
        threading.Thread(target=self.handle_voice_input, daemon=True).start()

    def handle_voice_input(self):
        """Handles voice input in a separate thread"""
        user_text = listen_and_transcribe()
        if user_text:
            self.display_message("You (Voice): " + user_text, self.user_color)
            self.process_response(user_text)
        else:
            self.display_message("Bot: Sorry, I didn't catch that. Try again.", "red")

    def process_response(self, user_text):
        """Processes the bot's response with animated typing effect"""
        self.typing_label.config(text="🤖 Bot is typing")
        self.root.update()

        for _ in range(3): 
            self.typing_label.config(text=self.typing_label.cget("text") + ".")
            self.root.update()
            time.sleep(0.4)

        intent = extract_intent(user_text)
        response_text = generate_response(user_text)


        self.typing_label.config(text="")
        self.display_message("Bot: " + response_text, self.bot_color)
        log_interaction(user_text, intent, response_text)

        threading.Thread(target=speak_text, args=(response_text,), daemon=True).start()

    def display_message(self, message, color):
        """Displays messages in the chat window with color styling"""
        self.text_display.config(state=tk.NORMAL)
        self.text_display.insert(tk.END, message + "\n", message)  
        self.text_display.tag_config(message, foreground=color)
        self.text_display.config(state=tk.DISABLED)
        self.text_display.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceBotGUI(root)
    root.mainloop()
