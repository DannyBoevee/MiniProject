import tkinter as tk
import datetime
from DataBase import *
from Api import *
from PIL import Image, ImageTk
from uuid import uuid4
from qrCode import qrCode

TITLE_FONT = ("Bauhaus 93", 15, "bold")
BASE_FONT = ("Tahoma", 10)
FL_BG_COLOR = "#800000"
FL_TEXT_COLOR = '#FFFFFF'
FL_TITLE_FONT = ("Bauhaus 93", 75, "bold")
FL_BASE_FONT = ("Tahoma", 10)


class ScreenController(tk.Tk):
    frames = {}

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.container = tk.Frame(self)
        self.title('ThuisBios')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.show_frame(FilmLijst)

    def show_frame(self, c, data=None):
        '''Show a frame for the given class'''
        if c in self.frames:
            frame = self.frames[c]
        else:
            frame = c(self.container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[c] = frame

        if "setData" in dir(frame):
            frame.setData(data)
        frame.tkraise()
        self.setPosSize(frame.getSize())

    def setPosSize(self, size):
        self.container.update_idletasks()
        w = self.container.winfo_screenwidth()
        h = self.container.winfo_screenheight()
        x = int(w / 2.0 - size[0] / 2.0)
        y = int(h / 2.0 - size[1] / 2.0 - 33.0)
        self.container.master.geometry("%dx%d+%d+%d" % (size + (x, y)))


class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # controller.setPosSize(200, 100, parent)
        label = tk.Label(self, text="Login", font=("Tahoma", 15, "bold"))
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
        self.error.grid(row=4, column=1, columnspan=2)

        button = tk.Button(self, text="Terug", command=lambda: self.Terug(controller), font=BASE_FONT)
        button.grid(row=3, column=2, sticky=tk.W)
        button = tk.Button(self, text="Login", command=lambda: self.Login(controller), font=BASE_FONT)
        button.grid(row=3, column=2, sticky=tk.E)

    def getSize(self):
        return (300, 130)

    def Login(self, controller):
        db = DataBase()
        if db.checkLogin(self.username.get(), self.password.get()):
            controller.show_frame(FilmLijstAanbieder)
        else:
            self.error.config(text=db.getError())

    def Terug(self, controller):
        controller.show_frame(FilmLijst)


class FilmLijst(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=FL_BG_COLOR)
        button = tk.Button(self, text="Login",
                           command=lambda: self.Login(controller), font=FL_BASE_FONT, bg="#670000",
                           fg=FL_TEXT_COLOR, relief='ridge', activebackground="#b26666")
        button.grid(row=1, column=5, columnspan=2, ipadx=100)
        label = tk.Label(self, text="Films", font=FL_TITLE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        label.grid(row=1, column=0, sticky='w', padx=25, columnspan=5)
        uitleg = tk.Label(self,
                          text="Klik op een plaatje of titel voor informatie over de film of om een kaartje te kopen.",
                          font=FL_BASE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        uitleg.grid(row=2, sticky='w', padx=25, pady=40, columnspan=5)

    def getSize(self):
        return (1370, 720)

    def Login(self, controller):
        controller.show_frame(LoginScreen)

    def details(self, controller, data):
        controller.show_frame(FilmDetails, data=data)

    def setData(self, data):
        apis = Api()
        db = DataBase()
        movie_list = apis.getMovieList(apis.getCurrentTime())
        col = 0
        date = apis.getCurrentTime()
        geenfilm = True
        for titel in movie_list:
            if db.checkFilmAanbieder(titel['titel'], date):
                images = ImageTk.PhotoImage(Image.open(str(titel['image'])))
                b1 = tk.Button(self,
                               command=lambda controller=self.controller, titel=titel: self.details(controller, titel),
                               image=images, height=290,
                               width=168)
                b1.grid(row=3, column=col, pady=25, padx=10)
                # save the button image from garbage collection!
                b1.image = images
                tijd = datetime.datetime.fromtimestamp(int(titel['starttijd']))
                titel['aanbieder'] = db.getFilmAanbieder(titel['titel'], date)
                titelbtn = tk.Button(self,
                                     command=lambda controller=self.controller, titel=titel: self.details(controller,
                                                                                                          titel),
                                     text=titel['titel'],
                                     font=("Tahoma", 10, "bold"), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR, relief="flat",
                                     activebackground=FL_BG_COLOR, activeforeground=FL_TEXT_COLOR)
                titelbtn.grid(row=4, column=col)
                starttijd = tk.Label(self, text=str(tijd), font=FL_BASE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
                starttijd.grid(row=5, column=col)
                aanbieders = tk.Label(self, text=titel['aanbieder'], font=FL_BASE_FONT, bg=FL_BG_COLOR,
                                      fg=FL_TEXT_COLOR)
                aanbieders.grid(row=6, column=col)
                col += 1
                geenfilm = False

        if geenfilm:
            if apis.getError() != '':
                label = tk.Label(self, text=apis.getError(), font=FL_BASE_FONT,
                                 bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
                label.grid(row=3, column=0, sticky='w', padx=25, columnspan=5)
            elif db.getError() != '':
                label = tk.Label(self, text=db.getError(), font=FL_BASE_FONT,
                                 bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
                label.grid(row=3, column=0, sticky='w', padx=25, columnspan=5)
            else:
                label = tk.Label(self, text="Er zijn geen aanbieders die een film aanbieden", font=FL_BASE_FONT,
                                 bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
                label.grid(row=3, column=0, sticky='w', padx=25, columnspan=5)


class FilmDetails(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=FL_BG_COLOR)
        label = tk.Label(self, text="Film Details", font=FL_TITLE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        label.grid(row=1, column=1, ipadx=25)
        button = tk.Button(self, text="Terug",
                           command=lambda: self.Terug(controller), font=FL_BASE_FONT, bg="#670000", fg=FL_TEXT_COLOR,
                           relief='ridge', activebackground="#b26666")
        button.grid(row=1, column=2, ipadx=100, sticky=tk.N)

        button = tk.Button(self, text="Aanmelden",
                           command=lambda: self.Aanmelden(controller), font=FL_BASE_FONT, bg="#670000",
                           fg=FL_TEXT_COLOR,
                           relief='ridge', activebackground="#b26666")
        button.grid(row=1, column=2, ipadx=100)

        # De titel van de film
        titel = tk.Message(self, text="Titel", width=100, font=("Tahoma", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        titel.grid(row=4, column=1)
        self.titel = tk.Message(self, width=700, text="", font=("Tahoma", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        self.titel.grid(row=4, column=2)

        # De beschrijving van de film
        beschrijving = tk.Message(self, text="Beschrijving", width=100, font=("Tahoma", 12), bg=FL_BG_COLOR,
                                  fg=FL_TEXT_COLOR)
        beschrijving.grid(row=7, column=1)
        self.beschrijving = tk.Message(self, width=700, text="", font=("Tahoma", 12), bg=FL_BG_COLOR,
                                       fg=FL_TEXT_COLOR)
        self.beschrijving.grid(row=7, column=2)

        # Het jaar van de film
        jaar = tk.Message(self, text="Jaar", width=100, font=("Tahoma", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        jaar.grid(row=10, column=1)
        self.jaar = tk.Message(self, text="", width=700, font=("Tahoma", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        self.jaar.grid(row=10, column=2)

        # De cast van de film
        cast = tk.Message(self, text="Cast", width=100, font=("Tahoma", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        cast.grid(row=13, column=1)
        self.cast = tk.Message(self, text="", width=700, font=("Tahoma", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        self.cast.grid(row=13, column=2)

        # De genre van de film
        genre = tk.Message(self, text="Genre", width=100, font=("Tahoma", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        genre.grid(row=16, column=1)
        self.genre = tk.Message(self, text="", width=700, font=("Tahoma", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        self.genre.grid(row=16, column=2)

        # De duur van de film
        duur = tk.Message(self, text="Duur", width=100, font=("Tahoma", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        duur.grid(row=19, column=1)
        self.duur = tk.Message(self, text="", width=700, font=("Tahoma", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        self.duur.grid(row=19, column=2)

        # De zender van de film
        zender = tk.Message(self, text="Zender", width=100, font=("Tahoma", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        zender.grid(row=21, column=1)
        self.zender = tk.Message(self, text="", width=700, font=("Tahoma", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        self.zender.grid(row=21, column=2)

        # De cover van de film
        foto = tk.Message(self, text="Cover", width=100, font=("Tahoma", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        foto.grid(row=26, column=1)
        self.foto = tk.Label(self, image="", height=290, width=168)
        self.foto.grid(row=26, column=2, pady=25, padx=10)

    def Terug(self, controller):
        controller.show_frame(FilmLijst)

    def Aanmelden(self, controller):
        controller.show_frame(FilmAanmelden, self.data)

    def getSize(self):
        return (1330, 800)

    def setData(self, data):
        api = Api()
        self.data = data
        images = ImageTk.PhotoImage(Image.open(str(data["image"])))
        self.foto.configure(image=images)
        self.foto.image = images
        data = api.getMovieDescription(data["titel"], api.getCurrentTime())
        self.titel['text'] = data['titel']
        self.beschrijving["text"] = data["synopsis"]
        self.jaar["text"] = data["jaar"]
        self.cast["text"] = data["cast"]
        self.genre["text"] = data["genre"]
        self.duur["text"] = data["duur"]
        self.zender["text"] = data["zender"]


class FilmLijstAanbieder(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=FL_BG_COLOR)
        button = tk.Button(self, text="Uitloggen",
                           command=lambda: self.Logout(controller), font=FL_BASE_FONT, bg="#670000",
                           fg=FL_TEXT_COLOR, relief='ridge', activebackground="#b26666",
                           activeforeground=FL_TEXT_COLOR)
        button.grid(row=1, column=5, columnspan=2, ipadx=100)
        label = tk.Label(self, text="Films", font=FL_TITLE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        label.grid(row=1, column=0, sticky='w', padx=25, columnspan=5)
        uitleg = tk.Label(self,
                          text="Klik op een plaatje of titel voor informatie over de film of om een kaartje te kopen.",
                          font=FL_BASE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        uitleg.grid(row=2, sticky='w', padx=25, pady=50, columnspan=5)
        apis = Api()
        movie_list = apis.getMovieList(apis.getCurrentTime())
        col = 0
        for titel in movie_list:
            images = ImageTk.PhotoImage(Image.open(str(titel['image'])))
            b1 = tk.Button(self, command=lambda titel=titel: self.details(controller, titel), image=images, height=290,
                           width=168)
            b1.grid(row=3, column=col, pady=25, padx=10)
            # save the button image from garbage collection!
            b1.image = images
            tijd = datetime.datetime.fromtimestamp(int(titel['starttijd']))
            titelbtn = tk.Button(self, command=lambda titel=titel: self.details(controller, titel), text=titel['titel'],
                                 font=("Tahoma", 10, "bold"), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR, relief='ridge',
                                 activebackground=FL_BG_COLOR, activeforeground=FL_TEXT_COLOR)
            titelbtn.grid(row=4, column=col)
            starttijd = tk.Label(self, text=str(tijd), font=FL_BASE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
            starttijd.grid(row=5, column=col)
            col += 1

    def getSize(self):
        return (1355, 720)

    def Logout(self, controller):
        controller.show_frame(LoginScreen)

    def details(self, controller, data):
        controller.show_frame(FilmDetailsAanbieder, data=data)


class FilmDetailsAanbieder(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=FL_BG_COLOR)
        label = tk.Label(self, text="Film Details", font=FL_TITLE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        label.grid(row=1, column=1, ipadx=25)
        button = tk.Button(self, text="Terug",
                           command=lambda: self.Terug(controller), font=FL_BASE_FONT, bg="#670000", fg=FL_TEXT_COLOR,
                           relief='ridge', activebackground="#b26666", activeforeground=FL_TEXT_COLOR)
        button.grid(row=0, column=2, ipadx=100)
        self.aanbieder = tk.Button(self, font=FL_BASE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR,
                                   relief='ridge', activebackground="#b26666", activeforeground=FL_TEXT_COLOR)
        self.aanbieder.grid(row=1, column=2, ipadx=300)

        # De titel van de film
        titel = tk.Message(self, text="Titel", width=100, font=("Tahoma", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        titel.grid(row=4, column=1)
        self.titel = tk.Message(self, width=750, text="", font=("Tahoma", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        self.titel.grid(row=4, column=2)

        # De beschrijving van de film
        beschrijving = tk.Message(self, text="Beschrijving", width=100, font=("Tahoma", 12), bg=FL_BG_COLOR,
                                  fg=FL_TEXT_COLOR)
        beschrijving.grid(row=7, column=1)
        self.beschrijving = tk.Message(self, width=750, text="", font=("Tahoma", 12), bg=FL_BG_COLOR,
                                       fg=FL_TEXT_COLOR)
        self.beschrijving.grid(row=7, column=2)

        # Het jaar van de film
        jaar = tk.Message(self, text="Jaar", width=100, font=("Tahoma", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        jaar.grid(row=10, column=1)
        self.jaar = tk.Message(self, text="", width=750, font=("Tahoma", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        self.jaar.grid(row=10, column=2)

        # De cast van de film
        cast = tk.Message(self, text="Cast", width=100, font=("Tahoma", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        cast.grid(row=13, column=1)
        self.cast = tk.Message(self, text="", width=750, font=("Tahoma", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        self.cast.grid(row=13, column=2)

        # De genre van de film
        genre = tk.Message(self, text="Genre", width=100, font=("Tahoma", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        genre.grid(row=16, column=1)
        self.genre = tk.Message(self, text="", width=750, font=("Tahoma", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        self.genre.grid(row=16, column=2)

        # De duur van de film
        duur = tk.Message(self, text="Duur", width=100, font=("Tahoma", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        duur.grid(row=19, column=1)
        self.duur = tk.Message(self, text="", width=750, font=("Tahoma", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        self.duur.grid(row=19, column=2)

        # De zender van de film
        zender = tk.Message(self, text="Zender", width=100, font=("Tahoma", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        zender.grid(row=21, column=1)
        self.zender = tk.Message(self, text="", width=750, font=("Tahoma", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        self.zender.grid(row=21, column=2)

        #De cover van de film
        foto = tk.Message(self, text="Cover", width=100, font=("Tahoma", 12), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        foto.grid(row=26, column=1)
        self.foto = tk.Label(self, image="", height=290,width=168)
        self.foto.grid(row=26, column=2, pady=25, padx=10)

    def Terug(self, controller):
        controller.show_frame(FilmLijstAanbieder)

    def getSize(self):
        return (1330, 800)

    def setData(self, data):
        api = Api()
        db = DataBase()
        images = ImageTk.PhotoImage(Image.open(str(data["image"])))
        self.foto.configure(image = images)
        self.foto.image = images
        if db.checkFilmBijAanbieder(data['titel'], api.getCurrentTime()):
            self.aanbieder.configure(text="Gasten lijst",
                                     command=lambda controller=self.controller, data=data: self.gastenlijst(controller, data))
        elif db.checkFilmAanbieder(data['titel'], api.getCurrentTime()):
            self.aanbieder.configure(text="Gereserveerd", command="")
        else:
            self.aanbieder.configure(text="Aanbieden", command=lambda: self.aanbieden(data))
        data = api.getMovieDescription(data["titel"], api.getCurrentTime())
        self.titel['text'] = data['titel']
        self.beschrijving["text"] = data["synopsis"]
        self.jaar["text"] = data["jaar"]
        self.cast["text"] = data["cast"]
        self.genre["text"] = data["genre"]
        self.duur["text"] = data["duur"]
        self.zender["text"] = data["zender"]

    def aanbieden(self, data):
        api = Api()
        db = DataBase()
        if db.saveAanbieder(data['titel'], api.getCurrentTime()):
            self.aanbieder.configure(text="Gasten lijst",
                                     command=lambda controller=self.controller: self.gastenlijst(controller, data))

    def gastenlijst(self, controller, data):
        controller.show_frame(AanbiederLijst, data=data)


class FilmAanmelden(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=FL_BG_COLOR)
        label = tk.Label(self, text="Aanmelden", font=FL_TITLE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        label.grid(row=1, column=1, ipadx=25)
        button = tk.Button(self, text="Terug",
                           command=lambda controller=controller: self.Terug(controller), font=FL_BASE_FONT,
                           bg=FL_BG_COLOR, fg=FL_TEXT_COLOR,
                           relief='flat', activebackground=FL_BG_COLOR, activeforeground=FL_TEXT_COLOR)
        button.grid(row=1, column=2, ipadx=300)

        label = tk.Label(self, text="E-Mail: ", font=("Tahoma", 16), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        label.grid(row=3, column=1)
        self.email = tk.Entry(self, width=100, font=BASE_FONT)
        self.email.grid(row=3, column=2)
        self.email.focus_set()
        label = tk.Label(self, text="Naam:", font=("Tahoma", 16), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        label.grid(row=4, column=1)
        self.naam = tk.Entry(self, width=100, font=BASE_FONT)
        self.naam.grid(row=4, column=2)
        self.error = tk.Label(self, text="", font=("Tahoma", 16), bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        self.error.grid(row=5, column=1)

        button_ok = tk.Button(self, text="Aanmelden", command=lambda: self.aanmelden(controller), bg="#670000",
                              fg=FL_TEXT_COLOR, relief='ridge', font=BASE_FONT, activebackground="#b26666")
        button_ok.grid(row=5, column=2, ipadx=100)

    def Terug(self, controller):
        controller.show_frame(FilmDetails, self.data)

    def getSize(self):
        return (1330, 350)

    def setData(self, data):
        self.error.configure(text='')
        self.data = data

    def aanmelden(self, controller):
        if self.naam.get() == '' or self.email.get() == '':
            self.error.configure(text='Vul alle gegevens in.')
        else:
            api = Api()
            db = DataBase()
            ucode = uuid4().hex
            db.saveFilm(self.data["titel"], self.data["aanbieder"], api.getCurrentTime(), ucode, self.naam.get(), self.email.get())
            controller.show_frame(qrFrame, ucode)


class AanbiederLijst(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=FL_BG_COLOR)
        label = tk.Label(self, text="Gasten", font=FL_TITLE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        label.grid(row=1, column=1, ipadx=25)
        button = tk.Button(self, text="Terug",
                           command=lambda: self.Terug(controller), font=FL_BASE_FONT, bg="#670000", fg=FL_TEXT_COLOR,
                           relief='ridge', activebackground="#b26666")
        button.grid(row=0, column=4)
        titel = tk.Label(self, text="Titel", font=("Tahoma", 10, "bold", "underline"), bg=FL_BG_COLOR,
                         fg=FL_TEXT_COLOR)
        titel.grid(row=2, column=1, pady=20)
        self.titel = tk.Label(self, text="", bg=FL_BG_COLOR)
        self.titel.grid(row=2, column=4, pady=20)
        jaar = tk.Label(self, text="Naam Gast", font=("Tahoma", 10, "bold", "underline"), bg=FL_BG_COLOR,
                        fg=FL_TEXT_COLOR)
        jaar.grid(row=2, column=2, pady=20)
        self.jaar = tk.Label(self, text="", bg=FL_BG_COLOR)
        self.jaar.grid(row=2, column=4, pady=20)
        mail = tk.Label(self, text="Mailadres Gast", font=("Helvetica", 10, "bold", "underline"), bg=FL_BG_COLOR,
                        fg=FL_TEXT_COLOR)
        mail.grid(row=2, column=3, padx=200, pady=20)
        self.mail = tk.Label(self, text="", bg=FL_BG_COLOR)
        self.mail.grid(row=2, column=4, pady=20)

    def Terug(self, controller):
        controller.show_frame(FilmDetailsAanbieder, self.data)

    def getSize(self):
        return (1330, 720)

    def setData(self, data):
        apis = Api()
        database = DataBase()
        self.data = data
        gastenlijst = database.getGastLijst(data['titel'], apis.getCurrentTime())
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


class qrFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=FL_BG_COLOR)
        label = tk.Label(self, text="QR-Code", font=FL_TITLE_FONT, bg=FL_BG_COLOR, fg=FL_TEXT_COLOR)
        label.grid(row=1, column=1, ipadx=25)
        button = tk.Button(self, text="Terug",
                           command=lambda: self.Terug(controller), font=FL_BASE_FONT, bg="#670000", fg=FL_TEXT_COLOR,
                           relief='ridge', activebackground="#b26666")
        button.grid(row=1, column=2, ipadx=100)

    def Terug(self, controller):
        controller.show_frame(FilmLijst)

    def getSize(self):
        return (900, 775)

    def setData(self, data):
        qr = qrCode(data)
        images = ImageTk.PhotoImage(Image.open(qr.getImage()))
        self.foto = tk.Label(self, image=images, height=580, width=580)
        self.foto.grid(row=2, column=0, columnspan=3, pady=25, padx=25)
        self.foto.image = images
