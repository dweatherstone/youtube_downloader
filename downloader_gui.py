import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from Helper import *

class DownloaderApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Youtube Video Downloader')
        self.DEFAULT_IMAGE = 'images/youtube-1495277_1280.png'
        self.DEFAULT_ICON = 'images/youtube-logo-png-large.ico'
        self.MAX_IMG_HEIGHT = 768
        self.MAX_IMG_WIDTH = 1024
        self.iconbitmap(self.DEFAULT_ICON)

        tab_names = ['Single', 'Playlist']
        self.notebook = self.create_notebook(tab_names)

        self.helper = YouTubeHelper()

    def resize_img(self, img):
        h, w = img.size
        if h > self.MAX_IMG_HEIGHT or w > self.MAX_IMG_WIDTH:
            factor = max((h / self.MAX_IMG_HEIGHT, w / self.MAX_IMG_WIDTH))
            new_x, new_y = int(round(h / factor)), int(round(w / factor))
            new_img = img.resize((new_x, new_y))
            return new_img
        else:
            return img

    def toggle_button_state(self, entry, button):
        if entry.var.get():
            button['state'] = tk.NORMAL
        else:
            button['state'] = tk.DISABLED

    def create_notebook(self, names):
        nb = DownloaderNotebook(self, names)
        nb.pack(side="top", fill=tk.BOTH, expand=True)

        def add_label(parent, text, row, column, padx=10, pady=10, rowspan=1):
            label = tk.Label(parent, text=text, anchor=tk.W)
            label.grid(row=row, column=column, padx=padx, pady=pady, rowspan=rowspan, sticky=tk.W+tk.E)
            return label

        def add_entry(parent, row, column, width=75, padx=10, pady=10, rowspan=1):
            entry = tk.Entry(parent, width=width)
            entry.grid(row=row, column=column, padx=padx, pady=pady, rowspan=rowspan)
            return entry

        def add_button(parent, text, command, row, column, padx=10, pady=10, state=tk.NORMAL, rowspan=1, anchor=None, sticky=None):
            button = tk.Button(parent, text=text, command=command, state=state, anchor=anchor)
            button.grid(row=row, column=column, padx=padx, pady=pady, rowspan=rowspan, sticky=sticky)
            return button

        def add_image(parent, url, row, column, padx=10, pady=10, columnspan=1):
            my_img = Image.open(url)
            my_img = self.resize_img(my_img)
            image = ImageTk.PhotoImage(my_img)
            image_label = tk.Label(parent, image=image)
            image_label.grid(row=row, column=column, padx=padx, pady=pady, columnspan=columnspan)
            return image, image_label

        def add_dropdown(parent, options, variable, row, column, default=0, padx=10, pady=10):
            variable.set(options[default])
            dropdown = ttk.Combobox(parent, textvariable=variable, values=options)
            dropdown.grid(row=row, column=column, padx=padx, pady=pady)

        tab = nb.tabs['Single']
        channel_frame = tk.LabelFrame(tab)
        channel_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W+tk.E)
        add_label(parent=channel_frame, text="Channel Name:", row=0, column=0)
        self.channel_name_entry = add_entry(parent=channel_frame, row=1, column=0)
        add_button(parent=channel_frame, text="Check", command=self.check_channel_name, row=0, column=1, rowspan=2)
        
        video_frame = tk.LabelFrame(tab)
        video_frame.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W+tk.E)
        add_label(parent=video_frame, text="Video Name:", row=0, column=0)
        self.video_name_entry = add_entry(parent=video_frame, row=1, column=0)
        add_button(parent=video_frame, text="Check", command=self.check_video_name, row=0, column=1, rowspan=2)

        thumbnail_frame = tk.LabelFrame(tab)
        thumbnail_frame.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W+tk.E)
        self.thumbnail_image, self.thumbnail_image_label = add_image(parent=thumbnail_frame, url=self.DEFAULT_IMAGE, row=0, column=0)

        download_frame = tk.LabelFrame(tab)
        download_frame.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W+tk.E)
        resolution_options = [
            "1080p",
            "720p",
            "480p",
            "360p",
            "240p",
            "144p"
        ]
        self.resolution = tk.StringVar()
        add_dropdown(parent=download_frame, options=resolution_options, variable=self.resolution, default=1, row=0, column=0)
        add_button(parent=download_frame, text="Download", command=self.download_video, row=0, column=1)
        add_button(parent=download_frame, text="Exit", command=self.quit, row=0, column=2, sticky=tk.W+tk.E, anchor=tk.E)

        tab = nb.tabs['Playlist']
        add_label(parent=tab, text="Lets dive into the world of computers!", row=0, column=0, padx=30, pady=30)

        return nb

    def check_channel_name(self):
        channel_name = self.channel_name_entry.get().strip()
        channel_id = self.helper.get_channel_id(channel_name)
        if channel_id is None:
            print("Validation Failed!!")
        else:
            print("Validation Success!!")

    def check_video_name(self):
        return

    def download_video(self):
        return

class DownloaderNotebook(ttk.Notebook):
    '''A customised Notebook that remember it's tabs in a dictionary.'''
    def __init__(self, master, names):
        super().__init__(master)

        self.tabs = {}
        for name in names:
            self.tabs[name] = tab = ttk.Frame(self)
            # tab.pack(fill=tk.BOTH, expand=True)
            self.add(tab, text=name)
            # canvas1 = tk.Canvas(tab)
            # scroll = ttk.Scrollbar(tab, command=canvas1.yview)
            # canvas1.configure(yscrollcommand=scroll.set)
            # canvas1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            # scroll.pack(side=tk.RIGHT, fill=tk.Y)

            # my_frame = ttk.Frame(canvas1, width=800, height=450)
            # canvas1.create_window((0, 0), window=my_frame, anchor="nw")

if __name__ == "__main__":
    app = DownloaderApplication()
    # app.pack(side="top", fill="both", expand=True)
    app.mainloop()
    # root.destroy()