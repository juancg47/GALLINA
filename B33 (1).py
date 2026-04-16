# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import time
import random 

# Intentar importar librerías del sensor BMP280
try:
    import board
    import busio
    import adafruit_bmp280
    SENSORS_AVAILABLE = True
except ImportError:
    SENSORS_AVAILABLE = False

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 495)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # --- TÍTULO ---
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 0, 461, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        # --- ÁREA DE LECTURA (label_5) ---
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(260, 80, 301, 91))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter) # Alineado a la derecha para que pegue con °C
        self.label_5.setStyleSheet("color: green;")
        self.label_5.setObjectName("label_5")

        # --- NUEVO LABEL UNIDAD (label_3) ---
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(580, 100, 61, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        
        # --- DATOS ESTUDIANTES ---
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(30, 270, 301, 111))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        
        # --- LOGO UNIVERSIDAD ---
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(380, 280, 381, 161))
        self.label_7.setObjectName("label_7")
        
        # --- ENTRADA DE TIEMPO ---
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(430, 210, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(360, 220, 71, 31))
        self.label_2.setObjectName("label_2")
        
        # --- BOTÓN DE ACCIÓN ---
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(220, 220, 93, 28))
        self.pushButton.setObjectName("pushButton")
        
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # --- CONEXIÓN DE EVENTOS ---
        self.pushButton.clicked.connect(self.iniciar_lectura_i2c)
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.leer_sensor)
        self.tiempo_restante = 0

        # Inicialización del sensor BMP280
        self.bmp_sensor = None
        if SENSORS_AVAILABLE:
            try:
                i2c = busio.I2C(board.SCL, board.SDA)
                self.bmp_sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)
            except Exception as e:
                print("Sensor no detectado, usando simulación.")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ECCI - Comunicación I2C"))
        self.label.setText(_translate("MainWindow", "SENSOR CON I2C"))
        self.label_5.setText(_translate("MainWindow", "---"))
        self.label_3.setText(_translate("MainWindow", "°C"))
        self.label_6.setText(_translate("MainWindow", "Marlly Johanna Rodriguez - 114061\n"
"Jean Pierre Fajardo Malagon - 113807\n"
"Juan Esteban Carrillo Galindo - 119042\n"
"Diego Alejandro Arellano - 110847"))
        self.label_7.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/newPrefix/images.png\"/></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "TIEMPO (s) ="))
        self.pushButton.setText(_translate("MainWindow", "LEER VALOR"))

    def iniciar_lectura_i2c(self):
        try:
            texto_tiempo = self.textEdit.toPlainText()
            self.tiempo_restante = int(texto_tiempo) * 2 # Muestreo cada 500ms
            
            if self.tiempo_restante > 0:
                self.pushButton.setEnabled(False)
                self.label_5.setStyleSheet("color: blue;")
                self.timer.start(500) 
            else:
                self.label_5.setText("Error")
        except ValueError:
            self.label_5.setText("?")

    def leer_sensor(self):
        """Realiza la lectura del sensor BMP280 o simulación"""
        if self.tiempo_restante > 0:
            if self.bmp_sensor:
                try:
                    valor = self.bmp_sensor.temperature
                    valor_mostrar = f"{valor:.2f}" # Solo el número con 2 decimales
                except:
                    valor_mostrar = "Error"
            else:
                # Simulación sin símbolo de porcentaje
                valor_mostrar = f"{random.uniform(20.0, 30.0):.2f}"
            
            self.label_5.setText(valor_mostrar)
            self.tiempo_restante -= 1
        else:
            self.timer.stop()
            self.pushButton.setEnabled(True)
            self.label_5.setStyleSheet("color: green;")

import imagen_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())