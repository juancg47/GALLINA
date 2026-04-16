# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

# --- TRUCO PARA EVITAR EL ERROR EN WINDOWS ---
try:
    import RPi.GPIO as GPIO
    LECTURA_REAL = True
except (ImportError, RuntimeError):
    # Si no encuentra RPi.GPIO (estás en Windows), creamos una clase falsa
    LECTURA_REAL = False
    class GPIO_Mock:
        BCM = 'BCM'
        IN = 'IN'
        PUD_DOWN = 'PUD_DOWN'
        HIGH = 1
        LOW = 0
        def setmode(self, mode): pass
        def setup(self, pin, mode, pull_up_down=None): pass
        def input(self, pin): 
            # Simulamos un cambio de estado cada vez que se lee (opcional)
            import time
            return 1 if int(time.time()) % 2 == 0 else 0
        def cleanup(self): pass
    GPIO = GPIO_Mock()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 438)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        
        # TÍTULO [cite: 4, 13, 22]
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 0, 461, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        # STATIC TEXT PARA ESTADO (Punto B4) 
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(90, 80, 581, 91))
        font_estado = QtGui.QFont()
        font_estado.setPointSize(20)
        font_estado.setBold(True)
        self.label_5.setFont(font_estado)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        
        # DATOS INTEGRANTES [cite: 26]
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(30, 200, 301, 111))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        
        # LOGO UNIVERSIDAD [cite: 26, 37]
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(380, 210, 381, 161))
        self.label_7.setObjectName("label_7")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)

        # --- CONFIGURACIÓN GPIO ---
        self.PIN_LECTURA = 17
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIN_LECTURA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # --- TIMER PARA LECTURA (Tiempo Real) ---
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.leer_gpio)
        self.timer.start(100)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Punto B4 - Universidad ECCI"))
        self.label.setText(_translate("MainWindow", "Lectura de puertos digitales"))
        self.label_6.setText(_translate("MainWindow", "Marlly Johanna Rodriguez - 114061\n"
"Jean Pierre Fajardo Malagon - 113807\n"
"Juan Esteban Carrillo Galindo - 119042\n"
"Diego Alejandro Arellano - 110847"))
        self.label_7.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/newPrefix/images.png\"/></p></body></html>"))

    def leer_gpio(self):
        estado = GPIO.input(self.PIN_LECTURA)
        
        if estado == GPIO.HIGH: # [cite: 23]
            self.label_5.setText("ALTO")
            self.label_5.setStyleSheet("background-color: red; color: white; border: 2px solid black;")
        else: # [cite: 24]
            self.label_5.setText("BAJO")
            self.label_5.setStyleSheet("background-color: blue; color: white; border: 2px solid black;")

import imagen_rc

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    try:
        sys.exit(app.exec_())
    finally:
        GPIO.cleanup()