import os
from json import dumps
from PIL import Image, ImageTk
from platform import system
from requests import get, post
from tkinter import Tk, font
from tkinter.ttk import Button, Label, Frame, Style
from urllib.request import urlretrieve

from src.init.const import (
    LOGO,
    AGENTDICT
)
from src.tools.search import (
    grabToken
)
from src.tools.pregame import (
    checkGame
)
from src.tools.findmap import (
    findMap
)


class Window:
    def __init__(self, localUrl = f"https://127.0.0.1:", onlineUrl = f"https://glz-na-1.na.a.pvp.net"):
        # System type
        self.system = system()
        self.local = localUrl
        self.baseUrl = onlineUrl

        # Create window
        self.window = Tk()
        self.window.withdraw()
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() - self.window.winfo_reqwidth()) / 16
        y = (self.window.winfo_screenheight() - self.window.winfo_reqheight()) / 16
        self.window.geometry("+%d+%d" % (x, y))
        self.window.deiconify()

        self.window.focus_force()
        self.window.minsize(500, 500)
        self.window.title("Instalock | Tahmid Ahmed | https://0pengu.in")
        #Global Font
        if self.system == "Windows":
            self.GF = font.Font(family = "Courier", size = "10", weight = "normal")
        else:
            self.GF = font.Font(family = "SF Pro", size = "10", weight = "normal")

        # Button States
        self.button_states = {}
        self.active_button_id = None

    def startup(self):
        # Create startup frame
        self.frame = Frame(self.window)
        self.frame.config
        self.frame.pack(side = "top", expand = True, fill = "both")

        LF = font.Font(family = "Courier", size = "4", weight = "bold")
        Label(
            self.frame,
            text = LOGO,
            font = LF
        ).pack()

        self.Wait()

        # Initiate window
        self.window.mainloop()

    def WaitCheck(self, i = 0):
        if i < 4:
            self.initialLabel.config(text = "Waiting for Valorant game to be detected" + "." * i)
            i += 1
        elif self.system != "Windows":
            self.initialLabel.config(text = "Error: Valorant is only supported on Windows! Closing in 5 seconds...")
            self.window.after(5000, self.window.destroy)  # Close the window after 5 seconds
            return
        else:
            i = 0
            # Do the actual logic here
            bool, iter = grabToken(self.local)
            if bool:
                self.iter = iter
                self.Queue()
                return  # Exit the update loop

        # Schedule this function to be called again after 400 milliseconds
        self.window.after(400, self.WaitCheck, i)

    def Wait(self):
        self.initialLabel = Label(self.frame, text="Waiting for Valorant to be detected", font=self.GF)
        self.initialLabel.pack()
        self.WaitCheck()

    def QueueCheck(self, i = 0):
        if i < 4:
            self.initialLabel.config(text = "Success, Riot Client/Valorant detected! Waiting for match" + "." * i)
            i += 1
        else:
            i = 0
            # Do the actual logic here
            iter = checkGame(self.baseUrl, self.iter['puuid'], self.iter['eT'], self.iter['aT'])
            if not("errorCode" in iter):
                self.matchID = iter['MatchID']
                self.SelectAgent()
                return

        # Schedule this function to be called again after 400 milliseconds
        self.window.after(400, self.QueueCheck, i)

    def Queue(self):
        self.initialLabel.config(text = "Success, Riot Client/Valorant detected! Waiting for match")
        self.QueueCheck()

    def create_button_grid(self):

        self.GridF = Frame(self.window)
        self.GridF.config
        self.GridF.pack(side = "top", expand = True, fill = "both")

        active_style = Style()
        active_style.configure("Active.TButton", background = "blue", border = "10")

        for row in range(3):
            for column in range(8):
                self.window.update()
                # Resize image first 
                if row == 2 and column == 7:
                    break
                else:
                    AGENTID = AGENTDICT[f'{row}{column}'][1]
                    AGENTNAME = AGENTDICT[f'{row}{column}'][0]
                    urlretrieve(f"https://media.valorant-api.com/agents/{AGENTDICT[f'{row}{column}'][1]}/displayicon.png", "OnlineImg")
                    with Image.open("OnlineImg") as img:
                        Im = img.resize((50, 50))  # Resize the image

                    # Load your image here
                    img = ImageTk.PhotoImage(Im)

                    button = Button(self.GridF, image = img)
                    button.image = img  
                    button.grid(row = row, column = column, padx = 5, pady = 5)

                    button['command'] = lambda btn = button, AID = AGENTID, NAME = AGENTNAME: self.toggle_button(btn, self.matchID, AID, NAME)

                    self.button_states[AGENTID] = button

    def SelectAgent(self):
        self.frame.destroy()

        self.frame = Frame(self.window)
        self.frame.config
        self.frame.pack(side = "top", expand = True, fill = "both")

        Title = Label(
            self.frame,
            text = "Select an Agent",
            font = font.Font(family = "Helvetica", size = "36", weight = "bold")
        )
        Title.pack(pady = 15)

        map = Label(
            self.frame,
            text = f"{findMap(f'{self.baseUrl}/pregame/v1/matches', self.matchID, self.iter['eT'], self.iter['aT'])}",
            font = font.Font(family = "Helvetica", size = "20", weight = "bold")
        )
        map.pack()

        self.create_button_grid()

        self.outputText = Label(
            self.frame,
            text = "",
            font = self.GF
        )
        self.outputText.pack(pady = 10)

        self.lockF = Frame(self.window)
        self.lockF.config
        self.lockF.pack(side = "top", expand = True, fill = "both")

        self.lock = Button(
            self.lockF,
            text = "Lock agent",
            command = self.lock_agent
        )
        self.lock.pack(pady = 10)

    def toggle_button(self, button, MATCHID, AGENTID, AGENTNAME):
        # Deactivate the currently active button if it's not the one being clicked
        if self.active_button_id and self.active_button_id != AGENTID:
            active_button = self.button_states[self.active_button_id]
            active_button.config(style='TButton')

        # Toggle the state of the clicked button
        if self.active_button_id != AGENTID:
            button.config(style='Active.TButton')
            self.active_button_id = AGENTID  # Update the active button reference
            try:
                Return = post(url = f"{self.baseUrl}/pregame/v1/matches/{MATCHID}/select/{AGENTID}", headers = {"X-Riot-Entitlements-JWT": f"{self.iter['eT']}", "Authorization": f"Bearer {self.iter['aT']}"})
                for player in Return.json()["AllyTeam"]["Players"]:
                    if player['Subject'] == self.iter['puuid']:
                        if player['CharacterSelectionState'] == "":
                            self.outputText.config(text = "Failed to select agent.")
                        else:
                            self.outputText.config(text = f"{AGENTNAME} selected")
            except BaseException as e:
                self.outputText.config(text = f"Error {e}")
        else:
            button.config(style='TButton')
            self.active_button_id = None  # No button is active

    def lock_agent(self):
        if self.active_button_id == None:
            self.outputText.cconfig(text = "Select an agent first!")
        else:
            try:
                Return = post(url = f"{self.baseUrl}/pregame/v1/matches/{self.matchID}/lock/{self.active_button_id}",  headers = {"X-Riot-Entitlements-JWT": f"{self.iter['eT']}", "Authorization": f"Bearer {self.iter['aT']}"})
                for player in Return.json()["AllyTeam"]["Players"]:
                    if player['Subject'] == self.iter['puuid']:
                        if player['CharacterSelectionState'] == 'locked':
                            self.lock.config(text = "Quit", command = self.window.destroy)
                            self.outputText.config(text = "Lock successful!")
                        else:
                            self.outputText.config(text = "Failed to select agent.")
            except BaseException as e:
                self.outputText.config(text = f"Error {e}")



def main():
    Window().startup()

main()
