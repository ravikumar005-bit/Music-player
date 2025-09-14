import os
import pygame
import tkinter as tk
from tkinter import filedialog, messagebox

# Initialize mixer and event system
pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_endevent(pygame.USEREVENT)

# Main window
root = tk.Tk()
root.title("🎵 Minimal Music Player")
root.geometry("320x360")
root.resizable(False, False)

# Global state
playlist = []
current_index = 0
is_playing = False

# Functions
def load_folder():
    global playlist, current_index
    folder = filedialog.askdirectory()
    if folder:
        playlist = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.mp3')]
        playlist.sort()
        playlist_box.delete(0, tk.END)
        for song in playlist:
            playlist_box.insert(tk.END, os.path.basename(song))
        if playlist:
            current_index = 0
            playlist_box.select_set(current_index)
            play_song()

def play_song():
    global is_playing
    try:
        pygame.mixer.music.load(playlist[current_index])
        pygame.mixer.music.play()
        is_playing = True
        update_label(f"▶️ {os.path.basename(playlist[current_index])}")
        playlist_box.select_clear(0, tk.END)
        playlist_box.select_set(current_index)
    except Exception as e:
        update_label("❌ Error playing file")
        messagebox.showerror("Playback Error", f"Could not play:\n{playlist[current_index]}\n\n{e}")

def toggle_play_pause():
    global is_playing
    if is_playing:
        pygame.mixer.music.pause()
        is_playing = False
        update_label("⏸️ Paused")
    else:
        pygame.mixer.music.unpause()
        is_playing = True
        update_label(f"▶️ {os.path.basename(playlist[current_index])}")

def next_song():
    global current_index
    if playlist:
        current_index = (current_index + 1) % len(playlist)
        play_song()

def prev_song():
    global current_index
    if playlist:
        current_index = (current_index - 1) % len(playlist)
        play_song()

def update_label(text):
    song_label.config(text=text)

def set_volume(val):
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)

def select_song(event):
    global current_index
    selection = playlist_box.curselection()
    if selection:
        current_index = selection[0]
        play_song()

def check_music_event():
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            next_song()
    root.after(1000, check_music_event)

# UI Elements
song_label = tk.Label(root, text="📂 Load music folder", wraplength=280, font=("Arial", 11))
song_label.pack(pady=10)

playlist_box = tk.Listbox(root, height=6, width=40)
playlist_box.pack(pady=5)
playlist_box.bind("<<ListboxSelect>>", select_song)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="⏮️", font=("Arial", 14), width=4, command=prev_song).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="▶️/⏸️", font=("Arial", 14), width=6, command=toggle_play_pause).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="⏭️", font=("Arial", 14), width=4, command=next_song).grid(row=0, column=2, padx=5)

tk.Button(root, text="📂 Load Folder", command=load_folder).pack(pady=10)

volume_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="🔊 Volume", command=set_volume)
volume_slider.set(70)
volume_slider.pack(pady=5)

# Start event loop
check_music_event()
root.mainloop()