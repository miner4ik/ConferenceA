import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from PyQt5.Qt import QVBoxLayout, QLabel, QDialog, QDialogButtonBox
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation
import requests
from datetime import datetime

appearance = ''


class BeautifulButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(BeautifulButton, self).__init__(*args, **kwargs)
        effect = QGraphicsColorizeEffect(self)
        self.setGraphicsEffect(effect)

        self.animation = QPropertyAnimation(effect, b"color")

        self.animation.setStartValue(QColor(Qt.cyan))
        self.animation.setEndValue(QColor(255, 255, 255))

        self.animation.setLoopCount(9)
        self.animation.setDuration(5000)


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()
        self.last_msg_time = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.load_messages)
        self.timer.start(1000)

    def load_messages(self):
        try:
            response = requests.get(
                'http://127.0.0.1:5000/history',
                params={'after': self.last_msg_time})
        except:
            return

        data = response.json()
        for message in data['messages']:
            beauty_time = datetime.fromtimestamp(message['time'])
            beauty_time = beauty_time.strftime('%d/%m/%Y %H:%M:%S')
            self.textBrowser.append(beauty_time + ' ' + message['username'])
            self.textBrowser.repaint()
            self.textBrowser.append(message['text'])
            self.textBrowser.repaint()
            self.textBrowser.append('')
            self.textBrowser.repaint()
            self.last_msg_time = message['time']

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        global appearance
        # Фон окна
        appearance = self.palette()
        appearance.setColor(QPalette.Normal, QPalette.Window, QColor("white"))
        self.setPalette(appearance)

        # Кнопка "Выход" в меню
        exitAction = QAction(QIcon('exit.png'), '&Выход', self)
        exitAction.setShortcut('Esc')
        exitAction.setStatusTip('Выход из приложения')
        exitAction.triggered.connect(qApp.quit)

        # Кнопка "Настройки" в меню
        settingAction = QAction(QIcon('settings.png'), '&Настройки', self)
        settingAction.setShortcut('Ctrl+Q')
        settingAction.setStatusTip('Настройки')
        settingAction.triggered.connect(self.Sett)

        # Кнопка меню
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Меню')
        fileMenu.addAction(settingAction)
        fileMenu.addAction(exitAction)

        # Кнопка "Отправить", для отправки сообщения в лог
        self.btn = BeautifulButton(self)
        self.btn.setIcon(QIcon('image.jpg'))
        self.btn.setIconSize(QSize(150, 150))
        # Кнопка будет неактивна, пока не введем ник
        # self.btn.setEnabled(False)
        self.btn.resize(150, 40)
        self.btn.move(303, 258)
        self.btn.clicked.connect(self.buttonClicked)

        # Окно лог с сообщениями
        self.textBrowser = QTextBrowser(self)
        self.textBrowser.move(50, 70)
        self.textBrowser.resize(255, 190)

        # Инициализируем статус бар
        self.statusBar()

        # Строка для ввода сообщения, сразу предлагает ввести "Hello world"
        self.textEdit = QLineEdit(self)
        self.textEdit.resize(255, 37)
        self.textEdit.move(50, 260)
        self.textEdit.setText("")

        # # Кнопка войти
        # self.login = BeautifulButton('Войти', self)
        # self.login.resize(102, 30)
        # self.login.move(549, 99)
        # self.login.clicked.connect(self.loginWindow)

        # # Размер окна диалога
        # self.setGeometry(300, 300, 290, 150)
        # self.setWindowTitle('Input dialog')

        # Строка поля ник с синим цветом
        self.le = QLineEdit(self)
        self.le.setStyleSheet("color: blue;")
        self.le.resize(100, 30)
        self.le.move(550, 70)

        # Размер основного окна + загрузка иконки
        self.setGeometry(500, 150, 700, 500)
        self.setWindowTitle('Мессенджер')
        self.setWindowIcon(QIcon('web.png'))
        self.show()

    # Функция вызова окна настроек
    def Sett(self):
        s = SettDialog("Тут будут настройки", self)
        s.exec_()
        self.setPalette(appearance)

    # Закрывает приложение при нажатии кнопки "Escape"
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    # Событие на кнопку "Войти" - выводит диалог с полем для ввода ника, и не отпустит, пока не введёшь
    # def loginWindow(self):
    #     username = self.QInput.Dialog()
    #     text, ok = QInputDialog.getText(self, 'Вход', 'Введите ваш ник:')
    #     while text == "":
    #         if ok:
    #             self.statusBar().clearMessage()
    #         else:
    #             self.statusBar().clearMessage()
    #             break
    #         self.statusBar().showMessage('Вы не ввели ник')
    #         text, ok = QInputDialog.getText(self, 'Вход', 'Введите ваш ник:')
    #     self.statusBar().clearMessage()
    #     if ok:
    #         # Сделает кнопку отправки сообщения активной
    #         self.btn.setEnabled(True)
    #         self.le.setText(str(username))

    # Отправляет сообщение на "Enter"
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            if self.btn.isEnabled() == True:
                self.buttonClicked()
            else:
                self.statusBar().showMessage('Вы не залогинились')

    # Событие на кнопку "Отправить", припысывает впереди сообщения ник автора
    def buttonClicked(self):

        if self.textEdit.text() == "":
            self.statusBar().showMessage('Вы ничего не ввели в сообщении')
        else:
            self.statusBar().clearMessage()
            text = self.textEdit.text()
            username = self.le.text()
            # Выводим ник с сообщением в лог
            # self.textBrowser.append(username + " пишет: " + text)

            data = {'username': username, 'text': text}
            try:
                response = requests.post('http://127.0.0.1:5000/send', json=data)
            except:
                self.textBrowser.append('Сервер недоступен. Порпробуйте позже')
                return

            if response.status_code != 200:
                self.textBrowser.append('Неправильные данные')
                return

            self.textEdit.setText("")


class SettDialog(QDialog):

    def __init__(self, info_str, parent=None):
        super(SettDialog, self).__init__(parent)

        # Окно настроек
        layout = QVBoxLayout(self)
        self.label = QLabel(info_str)
        self.font = QCheckBox('Серый фон')
        self.font.stateChanged.connect(self.changeFont)

        self.findButton = QPushButton(self.tr("&Find"))
        self.findButton.clicked.connect(self.findClick)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok, Qt.Horizontal, self)
        self.buttons.addButton(self.findButton, QDialogButtonBox.ActionRole)
        self.buttons.accepted.connect(self.accept)

        layout.addWidget(self.label)
        layout.addWidget(self.font)
        layout.addWidget(self.buttons)

    # Изменение цвета фона и текста окна настроек
    def changeFont(self, state):
        global appearance
        if state == Qt.Checked:
            self.label.setStyleSheet("color: white;")
            self.font.setStyleSheet("color: white;")
            appearance.setColor(QPalette.Normal, QPalette.Window, QColor("gray"))
            self.setPalette(appearance)
        else:
            self.label.setStyleSheet("color: black;")
            self.font.setStyleSheet("color: black;")
            appearance.setColor(QPalette.Normal, QPalette.Window, QColor("white"))
            self.setPalette(appearance)

    def findClick(self):
        print('Clicked!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
