import tkinter as tk
import datetime
from DataBase import *
from Api import *
from PIL import Image, ImageTk
from uuid import uuid4

TITLE_FONT = ("Helvetica", 15, "bold")
BASE_FONT = ("Helvetica", 10)
FL_BG_COLOR = "#800000"
FL_TEXT_COLOR = '#FFFFFF'
FL_TITLE_FONT = ("Helvetica", 75, "bold")
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
        for F in (LoginScreen, FilmLijst, FilmDetails, FilmAanmelden, AanbiederLijst, qrFrame):
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
        if "Show" in dir(frame):
            frame.Show()
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

        button = tk.Button(self, text="Terug", command=lambda: self.Terug(controller), font=BASE_FONT)
        button.grid(row=3, column=3)
        button = tk.Button(self, text="Login", command=lambda: self.Login(controller), font=BASE_FONT)
        button.grid(row=3, column=4)

    def getSize(self):
        return (300, 130)

    def Login(self, controller):
        db = DataBase()
        if db.checkLogin(self.username.get(), self.password.get()):
            controller.show_frame(AanbiederLijst)
        else:
            self.error.config(text='Gegevens zijn onjuist')

    def Terug(self, controller):
        controller.show_frame(FilmLijst)


class FilmLijst(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=FL_BG_COLOR)
        button = tk.Button(self, text="Login",
                           command=lambda: self.Login(controller), font=FL_BASE_FONT, bg=FL_BG_COLOR,
                           fg=FL_TEXT_COLOR, relief='flat', activebackground=FL_BG_COLOR,
                           activeforeground=FL_TEXT_COLOR)
        button.grid(row=0, column=6)
        label = tk.Label(self, text="Films", font=FL_TITLE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        label.grid(row=1, column=0, sticky='w', padx=25, columnspan=5)
        uitleg = tk.Label(self,
                          text="Klik op een plaatje of titel voor informatie over de film of om een kaartje te kopen.",
                          font=FL_BASE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        uitleg.grid(row=2, sticky='w', padx=25, pady=40, columnspan=5)
        apis = Api()
        movie_list = apis.getMovieList(apis.getCurrentTime())
        col = 0
        namen = ['Jan', 'Pieter', 'Henk', 'Flip', 'Kees', 'Gerrit', 'Mike']
        i = 0
        for titel in movie_list:
            images = ImageTk.PhotoImage(Image.open(str(titel['image'])))
            b1 = tk.Button(self, command=lambda titel=titel: self.details(controller, titel), image=images, height=290,
                           width=168)
            b1.grid(row=3, column=col, pady=25, padx=10)
            # save the button image from garbage collection!
            b1.image = images
            tijd = datetime.datetime.fromtimestamp(int(titel['starttijd']))
            titel['aanbieder'] = namen[i]
            titelbtn = tk.Button(self, command=lambda titel=titel: self.details(controller, titel), text=titel['titel'],
                                 font=("Helvetica", 10, "bold"), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR, relief="flat",
                                 activebackground=FL_BG_COLOR, activeforeground=FL_TEXT_COLOR)
            titelbtn.grid(row=4, column=col)
            starttijd = tk.Label(self, text=str(tijd), font=FL_BASE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
            starttijd.grid(row=5, column=col)
            col += 1
            if i is len(namen) - 1:
                i = 0
            else:
                i += 1
        aanbiedcol = 0
        for aanbiedernamen in namen:
            aanbieders = tk.Label(self, text=aanbiedernamen, font=FL_BASE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
            aanbieders.grid(row=6, column=aanbiedcol)
            aanbiedcol += 1

    def getSize(self):
        return (self.winfo_screenwidth(), self.winfo_screenheight())

    def Login(self, controller):
        controller.show_frame(LoginScreen)

    def details(self, controller, data):
        controller.show_frame(FilmDetails, data=data)


class FilmDetails(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg=FL_BG_COLOR)
        label = tk.Label(self, text="Film Details", font=FL_TITLE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        label.grid(row=1, column=1, ipadx=25)
        button = tk.Button(self, text="Terug",
                           command=lambda: self.Terug(controller), font=FL_BASE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR,
                           relief='flat')
        button.grid(row=1, column=2, ipadx=300)
        aanmelden = tk.Button(self, text="Aanmelden",
                              command=lambda: self.aanmelden(controller),
                              font=FL_BASE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR,
                              relief='flat')
        aanmelden.grid(row=0, column=2, ipadx=300)

        # De titel van de film
        titel = tk.Message(self, text="Titel", width=100, font=("Helvetica", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        titel.grid(row=4, column=1)
        self.titel = tk.Message(self, width=750, text="", font=("Helvetica", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        self.titel.grid(row=4, column=2)

        # De beschrijving van de film
        beschrijving = tk.Message(self, text="Beschrijving", width=100, font=("Helvetica", 12), bg=FL_BG_COLOR,
                                  fg=FL_TEXT_COLOR)
        beschrijving.grid(row=7, column=1)
        self.beschrijving = tk.Message(self, width=750, text="", font=("Helvetica", 12), bg=FL_BG_COLOR,
                                       fg=FL_TEXT_COLOR)
        self.beschrijving.grid(row=7, column=2)

        # Het jaar van de film
        jaar = tk.Message(self, text="Jaar", width=100, font=("Helvetica", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        jaar.grid(row=10, column=1)
        self.jaar = tk.Message(self, text="", width=750, font=("Helvetica", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        self.jaar.grid(row=10, column=2)

        # De cast van de film
        cast = tk.Message(self, text="Cast", width=100, font=("Helvetica", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        cast.grid(row=13, column=1)
        self.cast = tk.Message(self, text="", width=750, font=("Helvetica", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        self.cast.grid(row=13, column=2)

        # De genre van de film
        genre = tk.Message(self, text="Genre", width=100, font=("Helvetica", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        genre.grid(row=16, column=1)
        self.genre = tk.Message(self, text="", width=750, font=("Helvetica", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        self.genre.grid(row=16, column=2)

        # De duur van de film
        duur = tk.Message(self, text="Duur", width=100, font=("Helvetica", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        duur.grid(row=19, column=1)
        self.duur = tk.Message(self, text="", width=750, font=("Helvetica", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        self.duur.grid(row=19, column=2)

        # De zender van de film
        zender = tk.Message(self, text="Zender", width=100, font=("Helvetica", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        zender.grid(row=21, column=1)
        self.zender = tk.Message(self, text="", width=750, font=("Helvetica", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        self.zender.grid(row=21, column=2)

    def Terug(self, controller):
        controller.show_frame(FilmLijst)

    def getSize(self):
        return (self.winfo_screenwidth(), self.winfo_screenheight())

    def aanmelden(self, controller):
        controller.show_frame(FilmAanmelden, self.data)

    def setData(self, data):
        api = Api()
        aanbieder = data['aanbieder']
        data = api.getMovieDescription(data["titel"], api.getCurrentTime())
        data['aanbieder'] = aanbieder
        self.data = data
        self.titel['text'] = data['titel']
        self.beschrijving["text"] = data["synopsis"]
        self.jaar["text"] = data["jaar"]
        self.cast["text"] = data["cast"]
        self.genre["text"] = data["genre"]
        self.duur["text"] = data["duur"]
        self.zender["text"] = data["zender"]


class FilmAanmelden(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=FL_BG_COLOR)
        label = tk.Label(self, text="Aanmelden", font=FL_TITLE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        label.grid(row=1, column=1, ipadx=25)
        button = tk.Button(self, text="Terug",
                           command=lambda controller=controller: self.Terug(controller), font=FL_BASE_FONT,
                           bg=FL_BG_COLOR, fg=FL_TEXT_COLOR,
                           relief='flat')
        button.grid(row=1, column=2, ipadx=300)

        label = tk.Label(self, text="E-Mail: ", font=("Helvetica", 16), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        label.grid(row=3, column=1)
        self.email = tk.Entry(self, width=100, font=BASE_FONT)
        self.email.grid(row=3, column=2)
        self.email.focus_set()
        label = tk.Label(self, text="Naam:", font=("Helvetica", 16), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        label.grid(row=4, column=1)
        self.naam = tk.Entry(self, width=100, font=BASE_FONT)
        self.naam.grid(row=4, column=2)

        button_ok = tk.Button(self, text="Aanmelden", command=lambda: self.aanmelden(controller), font=BASE_FONT)
        button_ok.grid(row=5, column=2)

    def Terug(self, controller):
        controller.show_frame(FilmDetails, self.data)

    def getSize(self):
        return (self.winfo_screenwidth(), self.winfo_screenheight())

    def setData(self, data):
        self.data = data

    def aanmelden(self, controller):
        api = Api()
        db = DataBase()
        ucode = uuid4().hex
        db.saveFilm(self.data["titel"], self.data["aanbieder"], api.getCurrentTime(), ucode, self.naam.get(),
                    self.email.get())
        controller.show_frame(qrFrame, ucode)


class AanbiederLijst(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=FL_BG_COLOR)
        label = tk.Label(self, text="Gasten", font=FL_TITLE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        label.grid(row=1, column=1, ipadx=25)
        button = tk.Button(self, text="Uitloggen",
                           command=lambda: self.Terug(controller), font=FL_BASE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR,
                           relief='flat')
        button.grid(row=0, column=4)
        titel = tk.Label(self, text="Titel", font=("Helvetica", 10, "bold", "underline"), bg=FL_BG_COLOR,
                         fg=FL_TEXT_COLOR)
        titel.grid(row=2, column=1, pady=20)
        self.titel = tk.Label(self, text="", bg=FL_BG_COLOR)
        self.titel.grid(row=2, column=4, pady=20)
        jaar = tk.Label(self, text="Naam Gast", font=("Helvetica", 10, "bold", "underline"), bg=FL_BG_COLOR,
                        fg=FL_TEXT_COLOR)
        jaar.grid(row=2, column=2, pady=20)
        self.jaar = tk.Label(self, text="", bg=FL_BG_COLOR)
        self.jaar.grid(row=2, column=4, pady=20)
        mail = tk.Label(self, text="Mailadres Gast", font=("Helvetica", 10, "bold", "underline"), bg=FL_BG_COLOR,
                        fg=FL_TEXT_COLOR)
        mail.grid(row=2, column=3, padx=200, pady=20)
        self.mail = tk.Label(self, text="", bg=FL_BG_COLOR)
        self.mail.grid(row=2, column=4, pady=20)

    def Show(self):
        apis = Api()
        database = DataBase()
        gastenlijst = database.getGastLijst(apis.getCurrentTime())
        if not gastenlijst:
            for cc in range(1, 4):
                geengasten = tk.Label(self, text='Geen gasten', font=FL_BASE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
                geengasten.grid(row=3, column=cc)
        else:
            for titels in gastenlijst:
                gasttitel = tk.Label(self, text=titels['film'], font=FL_BASE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
                gasttitel.grid(row=3, column=1)
            for namen in gastenlijst:
                naam_gast = tk.Label(self, text=namen['naam'], font=FL_BASE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
                naam_gast.grid(row=3, column=2)
            for mails in gastenlijst:
                mail_gast = tk.Label(self, text=mails['email'], font=FL_BASE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
                mail_gast.grid(row=3, column=3)

    def Terug(self, controller):
        controller.show_frame(LoginScreen)
        pass

    def getSize(self):
        return (self.winfo_screenwidth(), self.winfo_screenheight())


class qrFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=FL_BG_COLOR)
        label = tk.Label(self, text="QR-Code", font=FL_TITLE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        label.grid(row=1, column=1, ipadx=25)
        button = tk.Button(self, text="Terug",
                           command=lambda: self.Terug(controller), font=FL_BASE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR,
                           relief='flat')
        button.grid(row=1, column=4, ipadx=600)
        images = ImageTk.PhotoImage(Image.open("./images/mb8jciqcde.jpg"))
        foto = tk.Label(self, image=images, height=290, width=168)
        foto.grid(row=3, column=2, pady=320, padx=320)
        foto.image = images

    def Terug(self, controller):
        controller.show_frame(LoginScreen)
        pass

    def getSize(self):
        return (self.winfo_screenwidth(), self.winfo_screenheight())

    def setData(self, data):
        self.data = data
