import requests
import json
import time
import random
import string
from websocket import create_connection
from utils import objects

class Client:

    def __init__ (self, email: str, password: str, access_token: str = None, websocket: bool = True):
        self.access_token = access_token
        self.api = "https://monopoly-one.com/api/"
        if email:
            self.sign_in(email, password)
        if websocket:
            self.create_connection()

    def generate_captcha(self):
        return "".join(random.choices(string.ascii_uppercase + string.ascii_lowercase + "_-", k=462)).replace("--", "-")

    def create_connection(self, subs: str = "rooms"):
        self.ws = create_connection(f"wss://monopoly-one.com/ws?subs={subs}&access_token={self.access_token}")

    def listen(self):
        while True:
            data_string = self.ws.recv()
            event = data_string[0]
            data = json.loads(data_string[data_string.find("{"):])
            data["type"] = data_string[1:data_string.find("{")]
            if event != 1:
                return objects.Event(data).Event
            continue

    def sign_up(self, email: str, nickname: str, password: str):
        data = {
            "email": email,
            "password": password,
            "sct": int(time.time()),
            "nick": nickname,
            "recaptcha_token": self.generate_captcha()
        }
        response = requests.post(f"{self.api}auth.signup", json=data).json()
        if response["code"] == 0:
            self.access_token = response["data"]["access_token"]
            return objects.GetSession(response["data"]).GetSession
        return response

    def sign_in(self, email: str, password: str):
        data = {
            "email": email,
            "password": password,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}auth.signin", json=data).json()
        if response["code"] == 0:
            self.access_token = response["data"]["access_token"]
            return objects.GetSession(response["data"]).GetSession
        raise Exception(response)

    def get_profile(self, user_id: int):
        data = {
            "user_id": user_id,
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}execute.profile", json=data).json()
        return response

    def users_get(self, user_ids: str, type: str = "short"):
        data = {
            "user_ids": user_ids,
            "type": type,
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}users.get", json=data).json()
        return response

    def get_info(self):
        data = {
            "logged_in": 1,
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}execute.games", json=data).json()
        return response

    def get_friends(self, offset: int = 0, count: int = 30):
        data = {
            "add_user_info": 1,
            "offset": offset,
            "count": count,
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}friends.get", json=data).json()
        return response

    def get_dialogs(self, offset: int = 0, count: int = 30):
        data = {
            "id_last": 419729250000,
            "offset": offset,
            "count": count,
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}im.dialogsGet", json=data).json()
        return response

    def get_history(self, user_id: int, offset: int = 0, count: int = 30):
        data = {
            "id_last": 419729250000,
            "offset": offset,
            "count": count,
            "user_id": user_id,
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}im.historyGet", json=data).json()
        return response

    def global_chat_send(self, message: str):
        data = {
            "message": message,
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}gchat.send", json=data).json()
        return response

    def room_create(self, maxplayers: int = 5, option_private: bool = False, game_submode: int = 0, option_autostart: bool = True):
        data = {
            "maxplayers": maxplayers,
            "option_private": int(option_private),
            "game_submode": game_submode,
            "option_autostart": int(option_autostart),
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}rooms.create", json=data).json()
        return response

    def games_get_live(self, offset: int = 0, count: int = 30):
        data = {
            "offset": offset,
            "count": count,
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}games.getLive", json=data).json()
        return response

    def games_my(self, offset: int = 0, count: int = 30):
        data = {
            "offset": offset,
            "count": count,
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}games.my", json=data).json()
        return response

    def games_get_live(self):
        data = {
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}streams.getLive", json=data).json()
        return response

    def games_resolve(self, gs_game_id: str, gs_id: int = 28):
        data = {
            "gs_game_id": gs_game_id,
            "gs_id": gs_id,
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}games.resolve", json=data).json()
        return response

    def room_join(self, room_id: str):
        data = {
            "room_id": room_id,
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}rooms.join", json=data).json()
        return response

    def room_leave(self):
        data = {
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}rooms.leave", json=data).json()
        return response