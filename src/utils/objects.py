class GetSession:

	def __init__ (self, data:dir):
		self.json = data
		self.access_token = None
		self.expires = None
		self.refresh_token = None
		self.user_id = None

	@property
	def GetSession(self):
		self.access_token = self.json["access_token"]
		self.expires = self.json["expires"]
		self.refresh_token = self.json["refresh_token"]
		self.user_id = self.json["user_id"]
		return self

class UserData:

	def __init__ (self, data:dir):
		self.json = data
		self.user_id = None
		self.nickname = None
		self.nicks_old = []
		self.gender = None
		self.avatar = None
		self.avatar_key = None
		self.online = None
		self.rank = None
		self.games = None
		self.games_wins = None
		self.xp = None
		self.xp_level = None
		self.admin_rights = None
		self.penalties = None

	@property
	def UserData(self):
		self.user_id = self.json["user_id"]
		self.nickname = self.json["nick"]
		self.nicks_old = self.json["nicks_old"]
		self.gender = self.json["gender"]
		self.avatar = self.json["avatar"]
		self.avatar_key = self.json["avatar_key"]
		self.online = self.json["online"]
		self.rank = self.json["rank"]
		self.games_wins = self.json["games_wins"]
		self.games = self.json["games"]
		self.xp = self.json["xp"]
		self.xp_level = self.json["xp_level"]
		self.admin_rights = self.json["admin_rights"]
		self.penalties = self.json["penalties"]
		return self
	
class Counters:

	def __init__ (self, data:dir):
		self.json = data
		self.vip_expires = None
		self.balance = None
		self.friends_requests = None
		self.messages_new = None
		self.invites = None
		self.trades_new = None
		self.email_verified = None

	@property
	def Counters(self):
		self.vip_expires = self.json["vip_expires"]
		self.balance = self.json["balance"]
		self.friends_requests = self.json["friends_requests"]
		self.messages_new = self.json["messages_new"]
		self.invites = self.json["invites"]
		self.trades_new = self.json["trades_new"]
		self.email_verified = self.json["email_verified"]
		return self

class Event:

	def __init__ (self, data:dir):
		self.json = data
		self.type = None
		self.data = None

	@property
	def Event(self):
		self.type = self.json["type"]
		if self.type == "status": self.data = Status(self.json["status"]).Status
		elif self.type == "auth": self.data = Auth(self.json).Auth
		elif self.type == "events": self.data = Events(self.json).Events
		return self

class Status:

	def __init__ (self, data:dir):
		self.json = data
		self.time = None
		self.online = None
		self.streams = None
		self.sct = None
		self.emotes_restricted = None

	@property
	def Status(self):
		self.time = self.json["time"]
		self.online = self.json["online"]
		self.streams = self.json["streams"]
		self.sct = self.json["sct"]
		self.emotes_restricted = self.json["emotes_restricted"]
		return self

class Auth:

	def __init__ (self, data:dir):
		self.json = data
		self.status = None
		self.user_data = None
		self.counters = None

	@property
	def Auth(self):
		self.status = self.json["status"]
		self.user_data = UserData(self.json["user_data"]).UserData
		self.counters = Counters(self.json["counters"]).Counters
		return self

class Message:

	def __init__ (self, data:dir):
		self.json = data
		self.msg_id = None
		self.text = None
		self.ts = None
		self.type = None
		self.user_id = None

	@property
	def Message(self):
		self.msg_id = self.json["msg_id"]
		self.text = self.json["text"]
		self.ts = self.json["ts"]
		self.type = self.json["type"]
		self.user_id = self.json["user_id"]
		return self

class Events:

	def __init__ (self, data:dir):
		self.json = data
		self.events = []
		self.rooms = []
		self.users_data = []
		self.messages = []

	@property
	def Events(self):
		for event in self.json["events"]:
			if event["type"] in ["room.delete", "room.set"]: self.events.append(RoomDeleteOrSet(event).RoomDeleteOrSet)
			elif event["type"] == "im.sync": self.events.append(ImSync(event).ImSync)
			elif event["type"] == "room.patch": self.events.append(RoomPatch(event).RoomPatch)
			elif event["type"] == "gchat.add":
				self.events.append(GlobalChatAdd(event).GlobalChatAdd)
				for message in self.json.get("messages"):
					self.messages.append(Message(message).Message)
		for user in self.json.get("users_data", []):
			self.users_data.append(UsersData(user).UsersData)
		return self

class UsersData:

	def __init__ (self, data:dir):
		self.json = data
		self.avatar = None
		self.gender = None
		self.nick = None
		self.online = None
		self.rank = {}
		self.user_id = None
		self.vip = None

	@property
	def UsersData(self):
		self.avatar = self.json["avatar"]
		self.gender = self.json["gender"]
		self.nick = self.json["nick"]
		self.online = self.json.get("online")
		self.rank = self.json["rank"]
		self.user_id = self.json["user_id"]
		self.vip = self.json.get("vip")
		return self

class RoomDeleteOrSet:

	def __init__ (self, data:dir):
		self.json = data
		self.id = None
		self.type = None
		self.room_id = None

	@property
	def RoomDeleteOrSet(self):
		self.id = self.json["id"]
		self.type = self.json["type"]
		self.room_id = self.json["room_id"]
		return self

class ImSync:

	def __init__ (self, data:dir):
		self.json = data
		self.id = None
		self.type = None
		self.id_last = None

	@property
	def ImSync(self):
		self.id = self.json["id"]
		self.type = self.json["type"]
		self.id_last = self.json["id_last"]
		return self

class RoomPatch:

	def __init__ (self, data:dir):
		self.json = data
		self.id = None
		self.patches = []
		self.room_id = None
		self.type = None
		self.v = None

	@property
	def RoomPatch(self):
		self.id = self.json["id"]
		self.patches = self.json["patches"]
		self.room_id = self.json["room_id"]
		self.type = self.json["type"]
		self.v = self.json["v"]
		return self

class GlobalChatAdd:

	def __init__ (self, data:dir):
		self.json = data
		self.id = None
		self.msg_id = None
		self.type = None

	@property
	def GlobalChatAdd(self):
		self.id = self.json["id"]
		self.msg_id = self.json["msg_id"]
		self.type = self.json["type"]
		return self