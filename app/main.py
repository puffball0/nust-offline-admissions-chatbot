import sys
import subprocess
import os

def install_dependencies():
    package_map = {
        "sentence_transformers": "sentence-transformers",
        "faiss": "faiss-cpu",
        "numpy": "numpy",
        "torch": "torch"
    }
    for module_name, package_name in package_map.items():
        try:
            __import__(module_name)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

install_dependencies()

import tkinter as tk
import threading

engine = None
base_dir = os.path.dirname(os.path.abspath(__file__))

root = tk.Tk()
root.title("NUST Offline Admissions Chatbot")

try:
    icon_image_path = os.path.join(base_dir, "..", "assests", "nust_logo.png")
    icon_img = tk.PhotoImage(file=icon_image_path)
    root.iconphoto(False, icon_img)
except:
    pass

root.geometry("1000x800")
root.state('zoomed')
root.configure(bg="#F0F4F9")
root.minsize(800, 600)

is_chat_mode = False

start_frame = tk.Frame(root, bg="#F0F4F9")
start_frame.pack(fill=tk.BOTH, expand=True)

inner_start = tk.Frame(start_frame, bg="#F0F4F9")
inner_start.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

brand_frame = tk.Frame(inner_start, bg="#F0F4F9")
brand_frame.pack(pady=(0, 20))

try:
    logo_path = os.path.join(base_dir, "..", "assests", "nust_logo.png")
    logo_img = tk.PhotoImage(file=logo_path)
    logo_label = tk.Label(brand_frame, image=logo_img, bg="#F0F4F9")
    logo_label.image = logo_img 
except:
    logo_label = tk.Label(brand_frame, text="NUST", font=("Segoe UI", 52, "bold"), fg="#0E2E5D", bg="#F0F4F9")

logo_label.pack(side="left", padx=(0, 15))
tk.Label(brand_frame, text="Offline Admissions Chatbot", font=("Segoe UI", 32, "bold"), fg="#0E2E5D", bg="#F0F4F9").pack(side="left")

status_label = tk.Label(inner_start, text="System Initializing...", 
                        font=("Segoe UI", 12), fg="#5F6368", bg="#F0F4F9")
status_label.pack()

prompt_label = tk.Label(inner_start, text="How can I help you?", font=("Segoe UI", 20), fg="#202124", bg="#F0F4F9")

start_input_frame = tk.Frame(inner_start, bg="white", highlightbackground="#DADCE0", highlightcolor="#0E2E5D", highlightthickness=2, padx=15, pady=10)
start_input = tk.Entry(start_input_frame, width=50, font=("Segoe UI", 15), relief="flat", bg="white")
start_input.pack(side="left", fill="x", expand=True)

start_ask_btn = tk.Button(start_input_frame, text="Send", font=("Segoe UI", 12, "bold"), 
                          bg="#0E2E5D", fg="white", relief="flat", cursor="hand2", 
                          activebackground="#1a4c9c", activeforeground="white", padx=15,
                          command=lambda: handle_submit(start_input))
start_ask_btn.pack(side="right", padx=(10,0))

chat_frame = tk.Frame(root, bg="#F0F4F9")

header_frame = tk.Frame(chat_frame, bg="white", height=60, bd=1, relief="ridge")
header_frame.pack(fill="x", side="top")

try:
    logo_path = os.path.join(base_dir, "..", "assests", "nust_logo.png")
    chat_logo_img = tk.PhotoImage(file=logo_path).subsample(3, 3)
    chat_logo_lbl = tk.Label(header_frame, image=chat_logo_img, bg="white")
    chat_logo_lbl.image = chat_logo_img
except:
    chat_logo_lbl = tk.Label(header_frame, text="NUST", font=("Segoe UI", 18, "bold"), fg="#0E2E5D", bg="white")

chat_logo_lbl.pack(side="left", padx=(20, 10), pady=10)
tk.Label(header_frame, text="Offline Admissions Chatbot", font=("Segoe UI", 14, "bold"), fg="#202124", bg="white").pack(side="left", pady=10)

bottom_input_area = tk.Frame(chat_frame, bg="#F0F4F9", height=90, pady=15)
bottom_input_area.pack(side="bottom", fill="x")

inner_bottom = tk.Frame(bottom_input_area, bg="white", highlightbackground="#DADCE0", highlightthickness=2, padx=15, pady=8)
inner_bottom.pack(padx=80, fill="x", expand=True)

chat_input = tk.Entry(inner_bottom, font=("Segoe UI", 15), relief="flat", bg="white")
chat_input.pack(side="left", fill="x", expand=True)
chat_ask_btn = tk.Button(inner_bottom, text="Send", font=("Segoe UI", 12, "bold"), 
                         bg="#0E2E5D", fg="white", relief="flat", cursor="hand2", 
                         activebackground="#1a4c9c", activeforeground="white", padx=20,
                         command=lambda: handle_submit(chat_input))
chat_ask_btn.pack(side="right", padx=(10,0))

canvas = tk.Canvas(chat_frame, bg="#F0F4F9", highlightthickness=0)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(chat_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

scrollable_frame = tk.Frame(canvas, bg="#F0F4F9")
canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

def on_canvas_configure(event):
    canvas.itemconfig(canvas_window, width=event.width)
canvas.bind("<Configure>", on_canvas_configure)

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
scrollable_frame.bind("<Configure>", on_frame_configure)

def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
root.bind_all("<MouseWheel>", _on_mousewheel)

def scroll_to_bottom():
    canvas.update_idletasks()
    canvas.yview_moveto(1.0)

def add_user_message(text):
    row_frame = tk.Frame(scrollable_frame, bg="#F0F4F9")
    row_frame.pack(fill=tk.X, padx=80, pady=(15, 5))
    
    bubble = tk.Frame(row_frame, bg="#D2E3FC", padx=20, pady=12, bd=0)
    bubble.pack(side=tk.RIGHT, anchor="e")
    
    lbl = tk.Label(bubble, text=text, bg="#D2E3FC", font=("Segoe UI", 14), 
                   fg="#202124", wraplength=550, justify="left")
    lbl.pack()
    scroll_to_bottom()

def add_bot_message(text, cred):
    row_frame = tk.Frame(scrollable_frame, bg="#F0F4F9")
    row_frame.pack(fill=tk.X, padx=80, pady=(10, 15))
    
    bubble = tk.Frame(row_frame, bg="#FFFFFF", padx=20, pady=15, 
                      highlightbackground="#DADCE0", highlightthickness=1)
    bubble.pack(side=tk.LEFT, anchor="w")
    
    lbl = tk.Label(bubble, text=text, bg="#FFFFFF", font=("Segoe UI", 13), 
                   fg="#202124", wraplength=650, justify="left")
    lbl.pack(anchor="w")
    
    if cred:
        cred_btn = tk.Label(bubble, text="Analyze Source ▼", bg="#FFFFFF", fg="#0E2E5D", 
                            font=("Segoe UI", 10, "bold"), cursor="hand2")
        cred_btn.pack(anchor="w", pady=(15,0))
        
        cred_frame = tk.Frame(bubble, bg="#F8F9FA", padx=15, pady=10, 
                              highlightbackground="#E8EAED", highlightthickness=1)
        cred_lbl = tk.Label(cred_frame, text=cred, bg="#F8F9FA", fg="#5F6368", 
                            font=("Segoe UI", 11, "italic"), wraplength=600, justify="left")
        cred_lbl.pack(anchor="w")
        
        def toggle_credibility(e):
            if cred_frame.winfo_ismapped():
                cred_frame.pack_forget()
                cred_btn.config(text="Analyze Source ▼")
            else:
                cred_frame.pack(anchor="w", pady=(8,0), fill="x")
                cred_btn.config(text="Hide Source ▲")
                scroll_to_bottom()
                
        cred_btn.bind("<Button-1>", toggle_credibility)
    
    scroll_to_bottom()

def add_thinking_bubble():
    row_frame = tk.Frame(scrollable_frame, bg="#F0F4F9")
    row_frame.pack(fill=tk.X, padx=80, pady=10)
    
    bubble = tk.Frame(row_frame, bg="#FFFFFF", padx=20, pady=12, 
                      highlightbackground="#DADCE0", highlightthickness=1)
    bubble.pack(side=tk.LEFT, anchor="w")
    
    lbl = tk.Label(bubble, text="Searching...", bg="#FFFFFF", font=("Segoe UI", 13, "italic"), fg="#5F6368")
    lbl.pack(anchor="w")
    
    scroll_to_bottom()
    return row_frame

def handle_submit(input_widget):
    global is_chat_mode
    query = input_widget.get().strip()
    if not query: return
    
    input_widget.delete(0, tk.END)
    
    if not is_chat_mode:
        start_frame.pack_forget()
        chat_frame.pack(fill="both", expand=True)
        root.bind('<Return>', lambda e: handle_submit(chat_input))
        chat_input.focus()
        is_chat_mode = True
        
    add_user_message(query)
    thinking_frame = add_thinking_bubble()
    
    def process():
        try:
            response = engine.handle_query(query)
            ans = response["answer"]
            cred = response["credibility"]
        except Exception as e:
            ans = f"System Error executing local models: {e}"
            cred = "Engine Offline"
            
        def display():
            thinking_frame.destroy()
            add_bot_message(ans, cred)
            
        root.after(0, display)
        
    threading.Thread(target=process, daemon=True).start()

def initialize_engine_bg():
    global engine
    
    import chatbot as eng
    eng.init_engine()
    engine = eng
    
    def on_ready():
        status_label.pack_forget()
        prompt_label.pack(pady=(0, 20))
        start_input_frame.pack(pady=10)
        root.bind('<Return>', lambda e: handle_submit(start_input))
        start_input.focus()
        
    root.after(0, on_ready)

threading.Thread(target=initialize_engine_bg, daemon=True).start()

root.mainloop()