import tkinter as tk
from tkinter import messagebox, filedialog
import yt_dlp
import os
import threading

def download_video():
    """Tek video indirme fonksiyonu"""
    url = url_entry.get()
    if not url:
        messagebox.showerror("Hata", "Lütfen bir bağlantı girin.")
        return

    save_path = filedialog.askdirectory(title="İndirilen dosyayı nereye kaydetmek istiyorsunuz?")
    if not save_path:
        messagebox.showwarning("İptal", "İndirme iptal edildi.")
        return

    thread = threading.Thread(target=perform_download, args=(url, save_path, False))
    thread.start()


def download_playlist():
    """Playlist indirme fonksiyonu"""
    url = url_entry.get()
    if not url:
        messagebox.showerror("Hata", "Lütfen bir bağlantı girin.")
        return

    save_path = filedialog.askdirectory(title="Playlistin nereye kaydedilmesini istiyorsunuz?")
    if not save_path:
        messagebox.showwarning("İptal", "İndirme iptal edildi.")
        return

    thread = threading.Thread(target=perform_download, args=(url, save_path, True))
    thread.start()


def perform_download(url, save_path, is_playlist):
    """İndirme işlemini gerçekleştiren fonksiyon"""
    try:
        if is_playlist:
            ydl_opts_check = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts_check) as ydl:
                info = ydl.extract_info(url, download=False)
                playlist_title = info.get('title', 'playlist')
            
            playlist_folder = os.path.join(save_path, playlist_title)
            os.makedirs(playlist_folder, exist_ok=True)
            final_path = playlist_folder
        else:
            final_path = save_path

        ydl_opts = {
            'outtmpl': os.path.join(final_path, '%(title)s.%(ext)s'),
            'format': 'best',
            'quiet': False,
            'no_warnings': False
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        messagebox.showinfo("Başarılı", f"İndirme başarıyla tamamlandı!\n\nKayıt Konumu: {final_path}")
        url_entry.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("İndirme Hatası", f"Bir hata oluştu:\n\n{str(e)}")


app = tk.Tk()
app.title("Dailymotion Video İndirici")
app.geometry("450x250")
app.resizable(False, False)

title_label = tk.Label(app, text="Dailymotion Video/Playlist İndirici", font=("Arial", 14, "bold"))
title_label.pack(pady=15)

url_label = tk.Label(app, text="Video veya Playlist Linki:")
url_label.pack()
url_entry = tk.Entry(app, width=55)
url_entry.pack(pady=10)

button_frame = tk.Frame(app)
button_frame.pack(pady=20)

video_button = tk.Button(button_frame, text="📹 Videoyu İndir", command=download_video, 
                         bg="#FF6B6B", fg="white", width=20, height=2, font=("Arial", 10))
video_button.pack(side=tk.LEFT, padx=5)

playlist_button = tk.Button(button_frame, text="📋 Playlistini İndir", command=download_playlist, 
                            bg="#4ECDC4", fg="white", width=20, height=2, font=("Arial", 10))
playlist_button.pack(side=tk.LEFT, padx=5)

info_label = tk.Label(app, text="Video: Tek videoyu indir | Playlist: Tüm videoları klasör içinde indir", 
                     font=("Arial", 9), fg="gray")
info_label.pack(pady=10)

app.mainloop()