from datetime import datetime
import pytz

class TimeManager:
	def __init__(self, h_r=(6,22), dh=1, m_r=(0,60), dm=10, tz="Europe/Paris"):
		self.previous_hm = ""
		self.tz = pytz.timezone(tz)
		self.list = [f"{h}:{m}" if len(str(m))==2 else f"{h}:0{m}"
				for h in range(h_r[0], h_r[1], dh) 
				for m in range(m_r[0], m_r[1], dm)]
		self.list += f"{h_r[1]+1}:00"

	def current(self):
		if self.previous_hm == "":
			return datetime.now(self.tz).strftime("%H:%M")
		return self.previous_hm
	
	def execute(self):
		hours_minutes = datetime.now(self.tz).strftime("%H:%M")
		if hours_minutes != self.previous_hm and hours_minutes in self.list:
			self.previous_hm = hours_minutes
			return True
		return False