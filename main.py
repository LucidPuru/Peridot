from tkinter import filedialog
import customtkinter as ctk
from pathlib import Path
from SpotiFLAC import SpotiFLAC
import threading
from PIL import Image
import webbrowser
import os
import sys


# Packager Path Helper
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# App Themeing
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

# App Config.
app = ctk.CTk()
app.title("Peridot Desktop vr.1.0")
app.geometry("800x800")
app.iconbitmap(resource_path("icon.ico"))
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=0)
app.grid_rowconfigure(2, weight=0)
app.grid_rowconfigure(3, weight=0)
app.grid_rowconfigure(4, weight=1)
app.grid_columnconfigure(0, weight=1)


# Location
downloads_path = Path.home() / "Downloads"
def locollect():
    global downloads_path
    folder = filedialog.askdirectory()

    if not folder:
        return
    path = Path(folder)

    if not path.exists():
        popupspawn("Folder Error", "Please enter a valid folder.")
        return
    
    downloads_path = path
    path_label.configure(text = str(path))

# Download
def trackcollect(url):
    try:
        print("Downloading:", url)
        print("Saving to:", downloads_path)

        SpotiFLAC(
            url = url,
            output_dir = str(downloads_path),
            services = ["qobuz", "amazon", "tidal", "spoti", "youtube"],
            filename_format = "{artist} - {title}",
            use_track_numbers = True,
            use_artist_subfolders = True,
            use_album_subfolders = True
        )
    
    except Exception as e:
        app.after(0, lambda: popupspawn("Download Failed", str(e)))

    finally:
        app.after(0, progresskill)
        app.after(0, lambda: status.configure(text = "Status: Done"))
        app.after(0, lambda: popupspawn("Download Successful", "The required tracks have been successfully downloaded. Have fun listening!"))


# Download Initiation
def downloadthread():
    url = urlentry.get()
    if "spotify.com" not in url:
        popupspawn("URL Error", "Please enter a valid Spotify URL.")
        return

    downloadbutton.configure(text = "Downloading...", state = "disabled")
    progress.start()
    status.configure(text = "Status: Downloading...")

    thread = threading.Thread(target = trackcollect, args = (url,), daemon = True)
    thread.start()


# Progress Control
def progresskill():
    progress.stop()
    progress.set(0)
    downloadbutton.configure(state = "normal", text = "Download")


# Popup
def popupspawn(name, message):
    popup = ctk.CTkToplevel(app)
    popup.title(name)
    popup.geometry("300x150")
    popup.resizable(False, False)

    popup.grab_set()

    errortext = ctk.CTkLabel(popup, text = message, wraplength = 250, justify = "center")
    errortext.pack(padx = 20, pady = 20)

    errorbutton = ctk.CTkButton(popup, text = "OK", command = popup.destroy)
    errorbutton.pack(padx = 20, pady = 20)


# About
def aboutpage():
    apopup = ctk.CTkToplevel(app)
    apopup.title("About Me")
    apopup.geometry("300x300")
    apopup.resizable(False, False)

    about = ctk.CTkLabel(apopup, text = "Peridot Music Downloader\nVr.1.0.0\nMade with love by Puru\n\nI am a student passionate about programming and creating things that give me satisfaction. This was a short passion project. Its main goal was to learn something new.\n\nThis app is not officially assiciated with Spotify. I do not host any copyrighted material on my server. It simply uses 3rd party APIs to download tracks off of Tidal.", wraplength = 250, justify = "center")
    about.grid(row = 0, column = 0, padx = 20, pady = 20)
    gitbutt = ctk.CTkButton(apopup, text = "Github", command = github)
    gitbutt.grid(row = 1, column = 0, padx = 10, pady = 20)


# Github
def github():
    webbrowser.open("https://github.com/LucidPuru")



# UI
# Main Frame
mainframe = ctk.CTkFrame(app)
mainframe.grid(row = 2, column = 0, padx = 20)
mainframe.grid_columnconfigure((0,1), weight = 1)

# Logo
logo = ctk.CTkImage(
    light_image = Image.open(resource_path("logo.png")),
    dark_image = Image.open(resource_path("logo.png")),
    size = (600, 240)
)
logotext = ctk.CTkLabel(app, image = logo, text = "")
logotext.grid(row = 1, column = 0)

# URL Entry
urlabel = ctk.CTkLabel(mainframe, text = "Enter Spotify URL:")
urlabel.grid(row = 1, column = 0, padx = 20, pady = 20, sticky = "nsew")
urlentry = ctk.CTkEntry(mainframe)
urlentry.grid(row = 1, column = 1, padx = 20, pady = 20, sticky = "nsew")

# Location Entry
loclabel = ctk.CTkLabel(mainframe, text = "Select Download Location:")
loclabel.grid(row = 2, column = 0, padx = 20, pady = 20, sticky = "nsew")
locentry = ctk.CTkButton(mainframe, text = "Browse", command = locollect)
locentry.grid(row = 2, column = 1, padx = 20, pady = 20, sticky = "nsew")

# Selected Path
path_label = ctk.CTkLabel(mainframe, text=str(downloads_path), anchor="w")
path_label.grid(row = 3, column = 0, columnspan = 2, padx = 20, pady = 20, sticky = "ew")

# Download
downloadbutton = ctk.CTkButton(mainframe, text = "Download", command = downloadthread)
downloadbutton.grid(row = 4, column = 0, padx = 20, pady = 20, columnspan = 2, sticky = "ew")

# Progress Bar
progress = ctk.CTkProgressBar(mainframe)
progress.grid(row = 5, column = 0, columnspan = 2, padx = 20, pady = 20, sticky = "ew")
progress.set(0)

# Status Report
status = ctk.CTkLabel(mainframe, text = "Status: Idle")
status.grid(row = 6, column = 0, columnspan = 2)

# Credits
footer = ctk.CTkLabel(app, text = "Peridot Desktop vr.1.0", cursor = "hand2")
footer.grid(row = 3, pady = 30, column = 0)
footer.bind("<Button-1>", lambda e: aboutpage())


app.mainloop()
