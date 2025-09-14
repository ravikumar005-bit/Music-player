import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import os

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 My Music Player")
        self.root.geometry("400x300")

        pygame.init()
        pygame.mixer.init()

        self.playing = False
        self.paused = False

        # Song list
        self.playlist = []

        # GUI Components
        self.song_label = tk.Label(self.root, text="No song loaded", font=("Arial", 12))
        self.song_label.pack(pady=10)

        self.listbox = tk.Listbox(self.root, bg="lightgray", width=50)
        self.listbox.pack(pady=10)

        # Buttons
        controls = tk.Frame(self.root)
        controls.pack(pady=10)

        tk.Button(controls, text="▶ Play", width=8, command=self.play_song).grid(row=0, column=0, padx=5)
        tk.Button(controls, text="⏸ Pause", width=8, command=self.pause_song).grid(row=0, column=1, padx=5)
        tk.Button(controls, text="⏹ Stop", width=8, command=self.stop_song).grid(row=0, column=2, padx=5)
        tk.Button(self.root, text="📂 Load Songs", command=self.load_songs).pack(pady=10)

    def load_songs(self):
        folder = filedialog.askdirectory()
        if not folder:
            return

        self.playlist = []
        self.listbox.delete(0, tk.END)

        for file in os.listdir(folder):
            if file.endswith(".mp3"):
                full_path = os.path.join(folder, file)
                self.playlist.append(full_path)
                self.listbox.insert(tk.END, file)

        if self.playlist:
            self.song_label.config(text="Songs loaded. Select a song to play.")

    def play_song(self):
        try:
            selected_index = self.listbox.curselection()
            if not selected_index:
                messagebox.showinfo("No song selected", "Please select a song to play.")
                return

            song_path = self.playlist[selected_index[0]]
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            self.song_label.config(text=f"Now Playing: {os.path.basename(song_path)}")
            self.paused = False
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def pause_song(self):
        if pygame.mixer.music.get_busy():
            if not self.paused:
                pygame.mixer.music.pause()
                self.paused = True
                self.song_label.config(text="Paused")
            else:
                pygame.mixer.music.unpause()
                self.paused = False
                self.song_label.config(text="Resumed")

    def stop_song(self):
        pygame.mixer.music.stop()
        self.song_label.config(text="Stopped")

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
