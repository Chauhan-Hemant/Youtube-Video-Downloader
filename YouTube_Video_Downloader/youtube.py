import pafy
from tkinter import *
from threading import *
from tkinter import messagebox


# Start the thread
def startThread():
    th = Thread(target=getInfo, daemon=True)
    th.start()


# To get the details of the video
def getInfo():
    video_info_variable.set("Getting Video Information, Please wait...")
    url = url_entered.get()
    video = pafy.new(url)
    video_info_variable.set("Video Information : ")
    label_title_variable.set("Title: " + str(video.title))
    label_channel_variable.set("Channel: " + str(video.author))
    label_rating_variable.set("Rating: " + str(video.rating))
    label_views_variable.set("Views: " + str(video.viewcount))
    label_likes_variable.set("Likes: " + str(video.likes))
    label_dislikes_variable.set("Dislikes: " + str(video.dislikes))

    # video resolution List
    label_quality = Label(root, text="Select the video resolution :", font="Helvetica 10 bold").grid(row=9, column=0, padx=16, pady=8, sticky=W)

    streams = video.streams
    i = 1
    for quality in streams:
        listbox.insert(i, quality)
        i = i + 1
    listbox.grid(row=10, column=0, padx=16, sticky=W)
    listbox.select_set(0)

    download_btn.grid(row=11, column=0, pady=8, padx=2)
    download_mp3_btn.grid(row=11, column=0, padx=16, pady=8, sticky=W)


# start the downloading thread
def DownloadingThread():
    th = Thread(target=Download, daemon=True)
    th.start()


# In case for audio
def DownloadingMp3Thread():
    th = Thread(target=DownloadMp3, daemon=True)
    th.start()


# main download function
def Download():
    download_btn.configure(state=DISABLED)
    download_var = StringVar()
    Label(root, textvariable=download_var).grid(row=12, column=0, padx=16, pady=16, sticky=W)

    download_var.set("Downloading....")
    url = url_entered.get()
    video = pafy.new(url)
    streams = video.streams
    for i in streams:
        print(i)

    if "360p" in str(listbox.get(ACTIVE)):
        best = video.getbest(preftype="3gp")
        best.download()
    elif "webm" in str(listbox.get(ACTIVE)):
        best = video.getbest(preftype="webm")
        best.download()
    elif "mp4" in str(listbox.get(ACTIVE)):
        best = video.getbest(preftype="mp4")
        best.download()
    else:
        download_var.set("Please select the video resolution.")
    download_var.set("Download Completed.")


def DownloadMp3():
    download_var = StringVar()
    Label(root, textvariable=download_var).grid(row=12, column=0, padx=16, pady=16, sticky=W)
    download_var.set("Downloading...")
    url = url_entered.get()
    video = pafy.new(url)
    best_audio = video.getbestaudio()
    best_audio.download()
    download_var.set("Download Completed.")


def About():
    message = "Youtube Video Downloader \nDesigned Using Tkinter package Python\n- by Hemant Chauhan"
    messagebox.showinfo("About", message)

def on_closing():
    from tkinter import messagebox
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

# GUI
root = Tk()
root.geometry("720x720")
root.minsize(720, 720)
root.title("Youtube Video Downloader")

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="About", command=About)
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Help", menu=filemenu)
root.config(menu=menubar)

paste = Label(root, text="Paste the video url here : ", font='Helvetica12').grid(row=0, column=0, padx=16, pady=16)

url_entered = StringVar()
url_enter = Entry(root, width=50, textvariable=url_entered).grid(row=1, column=0, padx=26, sticky=W)

video_info_variable = StringVar()
info = Label(root, textvariable=video_info_variable, font='Helvetica 10 bold').grid(row=2, column=0, padx=16, pady=8, sticky=W)

label_title_variable = StringVar()
label_title = Label(root, textvariable=label_title_variable).grid(row=3, column=0, padx=16, sticky=W)

label_channel_variable = StringVar()
label_channel = Label(root, textvariable=label_channel_variable).grid(row=4, column=0, padx=16, sticky=W)

label_rating_variable = StringVar()
label_rating = Label(root, textvariable=label_rating_variable).grid(row=5, column=0, padx=16, sticky=W)

label_views_variable = StringVar()
label_views = Label(root, textvariable=label_views_variable).grid(row=6, column=0, padx=16, sticky=W)

label_likes_variable = StringVar()
label_likes = Label(root, textvariable=label_likes_variable).grid(row=7, column=0, padx=16, sticky=W)

label_dislikes_variable = StringVar()
label_dislikes = Label(root, textvariable=label_dislikes_variable).grid(row=8, column=0, padx=16, sticky=W)

listbox = Listbox(root, height=6, width=35)
download_btn = Button(root, text="Download Video", command=DownloadingThread)
download_mp3_btn = Button(root, text="Download Mp3", command=DownloadingMp3Thread)

go_btn = Button(root, text="Go", command=startThread).grid(row=1, column=2, padx=2)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()