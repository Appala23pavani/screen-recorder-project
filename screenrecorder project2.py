import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
import pyautogui
import threading
import time
from PIL import ImageGrab
from datetime import datetime

recording = False
paused = False
rec_thread = None

def record_screen():
    global recording, paused
    screen_size = pyautogui.size()
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    filename = f"Recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.avi"
    out = cv2.VideoWriter(filename, fourcc, 20.0, screen_size)

    while recording:
        if not paused:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)
        time.sleep(1/20)

    out.release()
    messagebox.showinfo("Screen Recorder", f"Recording saved as {filename}")

def start_recording():
    global recording, paused, rec_thread
    if not recording:
        recording = True
        paused = False
        rec_thread = threading.Thread(target=record_screen)
        rec_thread.start()

def pause_recording():
    global paused
    if recording and not paused:
        paused = True
        messagebox.showinfo("Screen Recorder", "Recording Paused")

def resume_recording():
    global paused
    if recording and paused:
        paused = False
        messagebox.showinfo("Screen Recorder", "Recording Resumed")

def stop_recording():
    global recording, paused
    if recording:
        recording = False
        paused = False

def take_screenshot():
    img = ImageGrab.grab()
    filename = f"Screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    img.save(filename)
    messagebox.showinfo("Screenshot", f"Screenshot saved as {filename}")

# GUI
root = tk.Tk()
root.title("Screen Recorder with Screenshot")
root.geometry("300x280")

tk.Label(root, text="Screen Recorder", font=("Arial", 16)).pack(pady=10)

tk.Button(root, text="Start Recording", command=start_recording, width=25).pack(pady=5)
tk.Button(root, text="Pause Recording", command=pause_recording, width=25).pack(pady=5)
tk.Button(root, text="Resume Recording", command=resume_recording, width=25).pack(pady=5)
tk.Button(root, text="Stop Recording", command=stop_recording, width=25).pack(pady=5)
tk.Button(root, text="Take Screenshot", command=take_screenshot, width=25).pack(pady=10)

root.mainloop()