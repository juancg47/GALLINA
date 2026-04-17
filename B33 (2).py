# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import random

# --- INTENTO DE IMPORTACIÓN SEGURO ---
try:
    import board
    import busio
    import adafruit_bmp280
    SENSOR_LIB_INSTALLED = True
except (ImportError, AttributeError, ProcessLookupError):
    # Esto ocurre si estás en Windows o te faltan librerías
    SENSOR_LIB_INSTALLED = False
    print("Aviso: Librerías de hardware no detectadas. Se usará modo diagnóstico.")

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 495)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        
        # --- TÍTULO ---
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 0, 461, 71))
        font = QtGui.QFont(); font.setPointSize(16); font.setBold(True)
        self.label.setFont(font)
        self.label.setText("SENSOR CON I2C (BMP280)")
        
        # --- LECTURA (label_5) ---
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(260, 80, 301, 91))
        font = QtGui.QFont(); font.setPointSize(24); font.setBold(True)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label_5.setStyleSheet("color: green;")
        self.label_5.setText("---")

        # --- UNIDAD (label_3) ---
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(580, 100, 61, 71))
        font = QtGui.QFont(); font.setPointSize(16); font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setText("°C")
        
        # --- DATOS ESTUDIANTES ---
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(30, 270, 301, 111))
        self.label_6.setText("Marlly Johanna Rodriguez - 114061\nJean Pierre Fajardo Malagon - 113807\nJuan Esteban Carrillo Galindo - 119042\nDiego Alejandro Arellano - 110847")
        
        # --- EDIT TEXT Y BOTÓN ---
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(430, 210, 221, 41))
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(360, 220, 71, 31))
        self.label_2.setText("TIEMPO =")
        
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(220, 220, 93, 28))
        self.pushButton.setText("VALOR")
        
        MainWindow.setCentralWidget(self.centralwidget)
        
        # --- LOGICA ---
        self.pushButton.clicked.connect(self.iniciar)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.leer_datos)
        self.muestras = 0
        self.sensor = None

        # Inicialización del sensor solo si las librerías existen
        if SENSOR_LIB_INSTALLED:
            try:
                self.i2c = busio.I2C(board.SCL, board.SDA)
                self.sensor = adafruit_bmp280.Adafruit_BMP280_I2C(self.i2c, address=0x76)
            except:
                try:
                    self.sensor = adafruit_bmp280.Adafruit_BMP280_I2C(self.i2c, address=0x77)
                except:
                    print("Sensor no encontrado físicamente.")

    def iniciar(self):
        try:
            val = int(self.textEdit.toPlainText())
            self.muestras = val * 2
            self.pushButton.setEnabled(False)
            self.timer.start(500)
        except:
            self.label_5.setText("Error")

    def leer_datos(self):
        if self.muestras > 0:
            if self.sensor:
                self.label_5.setText(f"{self.sensor.temperature:.2f}")
            else:
                # Si estamos en la PC o no hay sensor, ponemos un aviso
                self.label_5.setText("NO SENS")
            self.muestras -= 1
        else:
            self.timer.stop()
            self.pushButton.setEnabled(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())