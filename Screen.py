import tkinter as tk
import datetime
from DataBase import *
from Api import *

TITLE_FONT = ("Helvetica", 15, "bold")
BASE_FONT = ("Helvetica", 10)
FL_BG_COLOR = "#800000"
FL_TEXT_COLOR = '#FFFFFF'
FL_TITLE_FONT = ("Helvetica", 50, "bold")
FL_BASE_FONT = ("Helvetica", 10)


class ScreenController(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginScreen, FilmLijst, FilmDetails):
            frame = F(self.container, self)
            self.frames[F] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(FilmLijst)

    def show_frame(self, c, data=None):
        '''Show a frame for the given class'''
        frame = self.frames[c]
        if "setData" in dir(frame):
            frame.setData(data)
        frame.tkraise()
        self.setPosSize(frame.getSize())

    def setPosSize(self, size):
        self.container.update_idletasks()
        w = self.container.winfo_screenwidth()
        h = self.container.winfo_screenheight()
        x = int(w / 2 - size[0] / 2)
        y = int(h / 2 - size[1] / 2)
        self.container.master.geometry("%dx%d+%d+%d" % (size + (x, y)))


class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # controller.setPosSize(200, 100, parent)
        label = tk.Label(self, text="Login", font=TITLE_FONT)
        label.grid(row=0, columnspan=4)

        label = tk.Label(self, text="Gebruikersnaam: ", font=BASE_FONT)
        label.grid(row=1, column=1)
        self.username = tk.Entry(self, font=BASE_FONT)
        self.username.grid(row=1, column=2)
        self.username.focus_set()
        label = tk.Label(self, text="Login", font=BASE_FONT)
        label.grid(row=2, column=1)
        self.password = tk.Entry(self, show="*", font=BASE_FONT)
        self.password.grid(row=2, column=2)

        self.error = tk.Label(self, text="", font=BASE_FONT)
        self.error.grid(row=3, column=1, columnspan=2)

        button = tk.Button(self, text="Login", command=lambda: self.Login(controller), font=BASE_FONT)
        button.grid(row=3, column=4)

    def getSize(self):
        return (300, 130)

    def Login(self, controller):
        db = DataBase()
        if db.checkLogin(self.username.get(), self.password.get()):
            controller.show_frame(FilmLijst)
        else:
            self.error.config(text='Gegevens zijn onjuist')


class FilmLijst(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=FL_BG_COLOR)
        label = tk.Label(self, text="Films", font=FL_TITLE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        label.grid(row=1, columnspan=1, column=0, sticky='w', padx=25)
        uitleg = tk.Label(self, text="Klik op een plaatje voor informatie over de film of om een kaartje te kopen.", font=FL_BASE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        uitleg.grid(row=2, sticky='w', padx=25, pady=25)
        button = tk.Button(self, text="Login",
                           command=lambda: self.Login(controller), font=FL_BASE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR, relief='flat', activebackground=FL_BG_COLOR, activeforeground=FL_TEXT_COLOR)
        button.grid(row=0, column=1, ipadx=820)
        apis = Api()
        movie_list = apis.getMovieList(apis.getCurrentTime())
        for titel in movie_list:
            images = tk.PhotoImage(str(titel['image']))
            b1 = tk.Button(self, image=images, height=125, width=100)
            b1.grid(pady=10)
            # save the button image from garbage collection!
            b1.image = images
            tijd = datetime.datetime.fromtimestamp(int(titel['starttijd']))
            titel = tk.Button(self, text=titel['title'], font=("Helvetica", 10, "bold"), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR, relief="flat", activebackground=FL_BG_COLOR, activeforeground=FL_TEXT_COLOR)
            titel.grid()
            starttijd = tk.Label(self, text=str(tijd), font=FL_BASE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
            starttijd.grid()

    def getSize(self):
        return (self.winfo_screenwidth(), self.winfo_screenheight())

    def Login(self, controller):
        controller.show_frame(LoginScreen)

    def details(self, controller, data):
        controller.show_frame(FilmDetails, data=data)


class FilmDetails(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=FL_BG_COLOR)
        label = tk.Label(self, text="Film Details", font=FL_TITLE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        label.grid(row=1, column=1, ipadx=25)
        button = tk.Button(self, text="Terug",
                           command=lambda: self.Terug(controller), font=FL_BASE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR,
                           relief='flat')
        button.grid(row=1, column=4, ipadx=600)
        api = Api()
        rij = 6

        for regel in api.getMovieDescription("Thunderball", api.getCurrentTime()).items():
            info = tk.Message(self, width=100, text=regel[0], font=("Helvetica", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
            info.grid(row=rij, column=1)
            info = tk.Message(self, width=750, text=regel[1], font=("Helvetica", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
            info.grid(row=rij, column=4)
            rij += 9

    def Terug(self, controller):
        controller.show_frame(FilmLijst)
        pass

    def getSize(self):
        return (self.winfo_screenwidth(), self.winfo_screenheight())
