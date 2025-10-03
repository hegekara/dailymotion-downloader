import tkinter as tk
from tkinter import messagebox
import yt_dlp

def download_video():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Hata", "Lütfen bir Dailymotion bağlantısı girin.")
        return

    try:
        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'format': 'best'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Başarılı", "Video başarıyla indirildi.")
    except Exception as e:
        messagebox.showerror("İndirme Hatası", str(e))

app = tk.Tk()
app.title("Dailymotion Video İndirici")
app.geometry("400x150")
app.resizable(False, False)

tk.Label(app, text="Dailymotion Video Linki:").pack(pady=10)
url_entry = tk.Entry(app, width=50)
url_entry.pack()

tk.Button(app, text="Videoyu İndir", command=download_video, bg="green", fg="white").pack(pady=20)

app.mainloop()
