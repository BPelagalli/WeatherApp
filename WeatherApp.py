import sys
import requests
from  PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                               QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase, QFont

class WeatherApp(QWidget):
	def __init__(self):
		super().__init__()
		self.city_label = QLabel("Enter city name:", self)
		self.city_input = QLineEdit(self)
		self.get_weather_button = QPushButton("Get Weather", self)
		self.temperature_label = QLabel(self)
		self.high_label = QLabel(self)
		self.low_label = QLabel(self)
		self.uv_label = QLabel(self)
		self.emoji_label = QLabel(self)
		self.description_label = QLabel(self)
		self.initUI()

	def initUI(self):
		self.setWindowTitle("BP Weather App")

		vbox = QVBoxLayout()

		vbox.addWidget(self.city_label)
		vbox.addWidget(self.city_input)
		vbox.addWidget(self.get_weather_button)
		vbox.addWidget(self.temperature_label)

		# nested veritcal layout in horizontal layout in vertical layout
		high_low_layout = QVBoxLayout()
		high_low_layout.addWidget(self.high_label)
		high_low_layout.addWidget(self.low_label)

		hbox = QHBoxLayout()

		h_l_uv_layout = QHBoxLayout()
		h_l_uv_layout.addLayout(high_low_layout)
		h_l_uv_layout.addWidget(self.uv_label)

		vbox.addLayout(h_l_uv_layout)

		vbox.addWidget(self.emoji_label)
		vbox.addWidget(self.description_label)

		self.setLayout(vbox)

		hbox.setContentsMargins(0, 0, 0, 0)

	
		self.setMinimumWidth(420)

		
		self.city_label.setAlignment(Qt.AlignCenter)
		self.city_input.setAlignment(Qt.AlignCenter)
		self.temperature_label.setAlignment(Qt.AlignCenter)
		self.high_label.setAlignment(Qt.AlignCenter)
		self.low_label.setAlignment(Qt.AlignCenter)
		self.uv_label.setAlignment(Qt.AlignCenter)
		self.emoji_label.setAlignment(Qt.AlignCenter)
		self.description_label.setAlignment(Qt.AlignCenter)

		self.city_label.setObjectName("city_label")
		self.city_input.setObjectName("city_input")
		self.get_weather_button.setObjectName("get_weather_button")
		self.temperature_label.setObjectName("temperature_label")
		self.high_label.setObjectName("high_label")
		self.low_label.setObjectName("low_label")
		self.uv_label.setObjectName("uv_label")
		self.emoji_label.setObjectName("emoji_label")
		self.description_label.setObjectName("description_label")

		self.city_input.setMinimumHeight(40)
		self.get_weather_button.setMinimumHeight(40)

		# Load custom font
		font_id = QFontDatabase.addApplicationFont("/Users/brettonpelagalli/Documents/VSC Projects/Python/ComicNeue-Regular.TTF")
		font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
		my_font = QFont(font_family)
		



		

	
		self.setStyleSheet("""

			QLabel, QPushButton{
				font-family: "Comic Neue";
					 					 
			}
								
			QLabel#city_label{
				font-size: 35px;
				font-style: italic;
						
			}

			QLineEdit#city_input{
				font-size: 28px;
				padding: 5px;
				border-radius: 22px;
				border: 1px solid;	
			}
			
			QPushButton#get_weather_button{
				font-size: 25px;
				font-weight: bold;
				border-radius: 22px;
				background-color: hsl(217, 81%, 80%);
				border: 1px solid;
				padding: 8px;
				min-width: 100px;
			}

			QPushButton#get_weather_button:hover{
				background-color: hsl(217, 81%, 85%); 
			}
			
			QPushButton#get_weather_button:pressed{
				background-color: hsl(217, 81%, 90%); 
			}

			QLabel#temperature_label{
				font-size: 65px;				 
			}	
					 
			QLabel#high_label, QLabel#low_label, QLabel#uv_label {
				font-size: 18px;
			}

			QLabel#emoji_label{
				font-size: 150px;
				font-family: Apple Color Emoji;	
				margin: 0			 
			}

			QLabel#description_label{
				font-size: 35px;							 
			}

			QLabel#temperature_label[state="error"] {
				font-size: 30px;
				color: hsl(354, 59%, 38%);
			}					 							
										 
		""")

		self.get_weather_button.clicked.connect(self.get_weather)
		self.city_input.returnPressed.connect(self.get_weather)

	def get_weather(self):
		api_key = "b70878f5ad7de678f59da5cc0ab06fce"
		city = self.city_input.text()
		url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

		
		try:
			# First API call: get city coordinates
			response = requests.get(url)
			response.raise_for_status()
			data = response.json()

			if data["cod"] == 200: 
				lat = data["coord"]["lat"]
				lon = data["coord"]["lon"]

				# Second API call: get extended weather details
				one_call_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}"

				one_call_response = requests.get(one_call_url)
				one_call_response.raise_for_status()
				daily_data = one_call_response.json()

				self.display_weather(data, daily_data)
		
		except requests.exceptions.HTTPError as http_error:
			match response.status_code:
				case 400:
					self.display_error("Bad Request:\n\nPlease check\nyour input")
				case 401:
					self.display_error("Unauthorized:\n\nInvalid API key")
				case 403:
					self.display_error("Forbidden:\nAccess is denied")
				case 404:
					self.display_error("Not found:\n\nCity not found")
				case 500:
					self.display_error("Internal server error:\n\nPlease try again later")
				case 502:
					self.display_error("Bad Gateway:\n\nInvalid response from the server")
				case 503:
					self.display_error("Service Unavailable:\n\nServer is down")
				case 504:
					self.display_error("Gateway Timeout:\n\nNo response from the server")
				case _:	
					self.display_error(f"HTTP error occured:\n\n{http_error}")	
		
		except requests.exceptions.ConnectionError: 
			self.display_error("Connection error:\n\nPlease check your\ninternet connection")
		except requests.exceptions.Timeout:
			self.display_error("Timeout error:\n\nThe request timed out")
		except requests.exceptions.TooManyRedirects:
			self.display_error("Too many redirects:\n\nPlease check the URL")
		except requests.exceptions.RequestException as req_error:
			self.display_error(f"Request error:\n\n{req_error}")			


	def display_error(self, message):
		self.temperature_label.setText(message)
		self.temperature_label.setStyleSheet("font-size: 30px; color: hsl(354, 59%, 38%);")
		self.high_label.clear()
		self.low_label.clear()
		self.uv_label.clear()
		self.emoji_label.clear()
		self.description_label.clear()
		self.city_input.styleSheet()
		self.get_weather_button.styleSheet()


	def display_weather(self, data, daily_data):
		self.city_input.styleSheet()
		self.get_weather_button.styleSheet()
		self.temperature_label.setStyleSheet("font-size: 65px;")

		# current temp
		temperature_k = data["main"]["temp"]
		temperature_f = (temperature_k * 9/5) - 459.67
		self.temperature_label.setText(f"{temperature_f:.0f}°F")

		# daily high and low
		high_k = daily_data["daily"][0]["temp"]["max"]
		low_k = daily_data["daily"][0]["temp"]["min"]
		high_f = (high_k * 9/5) - 459.67
		low_f = (low_k * 9/5) - 459.67
		self.high_label.setText(f"High: {high_f:.0f}℉")
		self.low_label.setText(f"Low: {low_f:.0f}℉")

		# Current UV Index
		uv_index = daily_data["current"]["uvi"]
		self.uv_label.setText(f"UV Index: {round(uv_index)}")

		# Set color based on index
		if uv_index <= 2:
			color = "hsl(120, 70%, 50%)"  # green
		elif uv_index <= 5:
			color = "hsl(47, 85%, 60%)"   # yellow
		elif uv_index <= 7:
			color = "hsl(30, 85%, 55%)"   # orange
		elif uv_index <= 10:
			color = "hsl(0, 80%, 55%)"    # red
		else:
			color = "hsl(278, 43%, 49%)"  # purple

		self.uv_label.setStyleSheet(f"color: {color};")

		# ID for emoji
		weather_id = data["weather"][0]["id"]
		weather_description = data["weather"][0]["description"]
		self.emoji_label.setText(self.get_weather_emoji(weather_id))
		self.description_label.setText(weather_description)
		self.city_input.styleSheet()
		self.get_weather_button.styleSheet()
		
		#print()
		#print()
		#print(data)
		#print()
		#print()
		#print(daily_data)
	
	@staticmethod
	def get_weather_emoji(weather_id):

		if 200 <= weather_id <= 232:
			return "⛈️"
		elif 300 <= weather_id <= 321:
			return "🌦️"
		elif 500 <= weather_id <= 531:
			return "🌧️"
		elif 600 <= weather_id <= 622:
			return "❄️"
		elif 701 <= weather_id <= 741:
			return "🌁"
		elif weather_id == 762:
			return "🌋"
		elif weather_id == 771:
			return "💨"
		elif weather_id == 781:
			return "🌪️"
		elif weather_id == 800:
			return "☀️"
		elif 801 <= weather_id <= 802:
			return "⛅️"
		elif 803 <= weather_id <= 804:
			return "☁️"
		else:
			return ""
		
		
if __name__ == "__main__":
	app = QApplication(sys.argv)
	weather_app = WeatherApp()
	weather_app.show()
	sys.exit(app.exec_())