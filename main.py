import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


class AplikacjaPogodowa(QWidget):
    def __init__(self):
        super().__init__()

        # --- WIDŻETY ---
        self.lokalizacja = QLabel("Miasto:", self)
        self.podaj_miasto = QLineEdit(self)
        self.wyszukaj = QPushButton("Szukaj", self)
        self.temperatura = QLabel(self)
        self.emoji = QLabel(self)
        self.pogoda = QLabel(self)

        self.initUI()

    def initUI(self):
        self.setFixedSize(600, 500)
        self.setWindowTitle("Aplikacja pogodowa")
        self.setWindowIcon(QIcon("pogoda.png"))

        # Layout główny (wertykalny)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Layout horyzontalny dla pola tekstowego i przycisku
        hbox_search = QHBoxLayout()
        hbox_search.addWidget(self.lokalizacja)
        hbox_search.addWidget(self.podaj_miasto)
        hbox_search.addWidget(self.wyszukaj)

        main_layout.addLayout(hbox_search)
        main_layout.addWidget(self.temperatura, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.emoji, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.pogoda, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

        # Placeholder w polu tekstowym
        self.podaj_miasto.setPlaceholderText("Wpisz nazwę miasta...")

        # Obsługa przycisku "Enter" w QLineEdit
        self.podaj_miasto.returnPressed.connect(self.przycisk_szukaj)

        # Nadanie obiektów nazw (dla selektorów #...)
        self.lokalizacja.setObjectName("lokalizacja")
        self.podaj_miasto.setObjectName("podaj_miasto")
        self.wyszukaj.setObjectName("wyszukaj")
        self.temperatura.setObjectName("temperatura")
        self.emoji.setObjectName("emoji")
        self.pogoda.setObjectName("pogoda")

        # TŁO + WYGLĄD
        self.setStyleSheet("""
            QWidget {
                background-color: #FAF0E6;
            }

            QLabel, QPushButton {
                font-family: Ubuntu;
                font-size: 14px;
                color: #333;
            }
            QLabel#lokalizacja {
                font-size: 18px;
                font-weight: bold;
                color: #444;
            }
            QLineEdit#podaj_miasto {
                font-size: 16px;
                background-color: white;
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton#wyszukaj {
                font-size: 16px;
                font-weight: bold;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 15px;
            }
            QPushButton#wyszukaj:hover {
                background-color: #45A049;
            }
            QLabel#temperatura {
                font-size: 50px;
                color: #333;
            }
            QLabel#emoji {
                font-size: 120px;
                font-family: "Segoe UI Emoji";
            }
            QLabel#pogoda {
                font-size: 30px;
                color: #666;
            }
        """)

        self.wyszukaj.clicked.connect(self.przycisk_szukaj)

    def przycisk_szukaj(self):
        klucz_api = "21b0986593db342638c9f2fc7b102d51"
        miasto = self.podaj_miasto.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={miasto}&appid={klucz_api}"

        try:
            odpowiedz = requests.get(url)
            odpowiedz.raise_for_status()
            wartosci = odpowiedz.json()

            if wartosci["cod"] == 200:
                self.wyswietl_pogode(wartosci)

        except requests.exceptions.HTTPError as http_error:
            match odpowiedz.status_code:
                case 400:
                    self.pokaz_bledy("Błąd zapytania:\nSpróbuj ponownie!")
                case 401:
                    self.pokaz_bledy("Błąd API")
                case 403:
                    self.pokaz_bledy("Brak dostępu")
                case 404:
                    self.pokaz_bledy("Nie znaleziono takiego miasta")
                case 500:
                    self.pokaz_bledy("Błąd servera")
                case 502:
                    self.pokaz_bledy("Błąd bramki")
                case 503:
                    self.pokaz_bledy("Serwer został wyłączony")
                case 504:
                    self.pokaz_bledy("Serwer nie odpowiada")
                case _:
                    self.pokaz_bledy(f"Wystąpił błąd:\n{http_error}")

    def pokaz_bledy(self, info):

        self.temperatura.setStyleSheet("font-size: 18px; color: red;")
        self.temperatura.setText(info)
        self.emoji.clear()
        self.pogoda.clear()

    def wyswietl_pogode(self, wartosci):
        self.temperatura.setStyleSheet("font-size: 50px; color: #333;")
        temperatura_k = wartosci["main"]["temp"]
        temperatura_c = temperatura_k - 273.15

        jaka_pogoda = wartosci["weather"][0]["description"]
        pogoda_id = wartosci["weather"][0]["id"]

        self.temperatura.setText(f"{temperatura_c:.0f}°C")
        self.emoji.setText(self.emoji_pogody(pogoda_id))
        self.pogoda.setText(jaka_pogoda)

    @staticmethod
    def emoji_pogody(pogoda_id):
        if 200 <= pogoda_id <= 232:
            return "⛈️"
        elif 300 <= pogoda_id <= 321:
            return "🌦️"
        elif 500 <= pogoda_id <= 521:
            return "🌧️"
        elif 600 <= pogoda_id <= 622:
            return "🌨️"
        elif 701 <= pogoda_id <= 741:
            return "🌫️"
        elif pogoda_id == 781:
            return "🌪️"
        elif pogoda_id == 800:
            return "☀️"
        elif 801 <= pogoda_id <= 803:
            return "🌤️"
        elif pogoda_id == 804:
            return "☁️"
        else:
            return ""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = AplikacjaPogodowa()
    weather_app.show()
    sys.exit(app.exec_())
