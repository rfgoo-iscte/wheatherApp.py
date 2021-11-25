import sys

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import PyQt5.QtWidgets as qt
from PyQt5.QtGui import QImage, QPixmap


def driver_select(option):
    print(option)
    # TODO Message: 'operadriver' executable needs to be in PATH. Please see https://sites.google.com/a/chromium.org/chromedriver/home

    #if option == "Opera":
    #    return webdriver.Opera()
    if option == "Safari":
        return webdriver.Safari()
    #elif option == "Chrome":
    #    return webdriver.Chrome()
    #elif option == "Firefox":  TODO Downlowad mozilla webriver
    #    return webdriver.Firefox()

def action(loc, option = "Safari"):

    url = "https://www.google.com"
    driver = driver_select(option)
    driver.get(url)

    cookies = driver.find_element_by_id("L2AGLb")
    cookies.send_keys(Keys.RETURN)

    search_bar = driver.find_element_by_name("q")
    search_bar.send_keys(loc)
    search_bar.send_keys(Keys.RETURN)

    try:
        weather = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "wob_tm"))
        )
    except:
        driver.quit()
        
    weather = driver.find_element_by_id("wob_tm").text

    img_src = driver.find_element_by_id("wob_tci").get_attribute("src")
    print(img_src)

    extra_info = driver.find_element_by_class_name("wtsRwe")

    mid_start = extra_info.text.find("%") + 1
    mid_end = extra_info.text.find("%V") + 1
    end_end = extra_info.text.find("h") + 1

    pre = extra_info.text[:mid_start]

    hum = extra_info.text[mid_start:mid_end]

    wind = extra_info.text[mid_end:end_end]

    print(weather + "ºC\n")
    print(pre)
    print(hum)
    print(wind)

    local = driver.find_element_by_id("wob_loc").text.split(", ")

    time = driver.find_element_by_id("wob_dts").text
    print(time)
    weather_desc = driver.find_element_by_id("wob_dc").text
    print(weather_desc)

    driver.delete_all_cookies()
    driver.quit()

    info = [img_src, weather, pre, hum, wind, local, time, weather_desc]
    print(info)
    return info


class Window(qt.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('WeatherApp')
        self.setGeometry(0, 0, 300, 150)

        # self.setFixedSize(300, 150)
        self.local_label = qt.QLabel(self)
        self.local_label.move(150, 6)
        self.local_label.resize(250, 15)

        self.image = QImage()
        self.image_label = qt.QLabel(self)

        self.time_label = qt.QLabel(self)
        self.time_label.move(150, 25)
        self.time_label.resize(160, 15)

        self.weather_desc = qt.QLabel(self)
        self.weather_desc.move(150, 45)
        self.weather_desc.resize(160, 15)

        self.temperature_label = qt.QLabel(self)
        self.temperature_label.move(5, 64)
        self.temperature_label.resize(160, 15)

        self.precipitation_label = qt.QLabel(self)
        self.precipitation_label.move(5, 84)
        self.precipitation_label.resize(160, 15)

        self.humidity_label = qt.QLabel(self)
        self.humidity_label.move(5, 104)
        self.humidity_label.resize(160, 15)

        self.wind_label = qt.QLabel(self)
        self.wind_label.move(5, 124)
        self.wind_label.resize(160, 15)

        def labels(info):

            # image
            self.image.loadFromData(requests.get(info[0]).content)
            self.image_label.setPixmap(QPixmap(self.image))
            self.image_label.resize(self.image.width(), self.image.height())
            self.image_label.move(30, 0)

            # local
            self.local_label.setText((info[5][0] + ",  " + info[5][1]) if len(info[5]) >= 2 else info[5][0])

            # time
            self.time_label.setText(info[6])

            # weather_desc
            self.weather_desc.setText(info[7])

            # Temperature
            self.temperature_label.setText("Temperature: "+info[1]+" ºC")

            # Precipitation
            self.precipitation_label.setText(info[2])

            # humidity
            self.humidity_label.setText(info[3])

            # wind
            self.wind_label.setText(info[4])

            self.show()


        # input dialog
        def search():
            # global info
            city, done = qt.QInputDialog.getText(self, 'WeatherApp', 'Enter the city')
            location = "tempo em " + city

            if done:

                driver, done2 = qt.QInputDialog.getText(self, "WeatherApp", "Please select your browser (opera, chrome, safari, Firefox):")
                if done2:
                    info = action(location, str(driver.capitalize()))
                    labels(info)

        search()

        # Button
        self.button = qt.QPushButton("Back", self, clicked=lambda: search())
        self.button.move(150, 104)
        self.button.show()


app = qt.QApplication([])
window = Window()
sys.exit(app.exec_())
