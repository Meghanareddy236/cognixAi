from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout,
    QPushButton, QFrame, QLabel, QSizePolicy
)
from PyQt5.QtGui import QIcon, QPainter, QMovie, QColor, QTextCharFormat, QFont, QPixmap, QTextBlockFormat, QLinearGradient
from PyQt5.QtCore import Qt, QSize, QTimer
from dotenv import dotenv_values
import sys
import os

env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname")
current_dir = os.getcwd()
old_chat_message = ""
TempDirPath = rf"{current_dir}\Frontend\Files"
GraphicsDirPath = rf"{current_dir}\Frontend\Graphics"

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = Query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's"]

    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
    return new_query.capitalize()

def SetMicrophoneStatus(Command):
    with open(rf'{TempDirPath}\Mic.data', 'w', encoding='utf-8') as file:
        file.write(Command)

def GetMicrophoneStatus():
    with open(rf'{TempDirPath}\Mic.data', 'r', encoding='utf-8') as file:
        Status = file.read()
    return Status

def SetAssistantStatus(Status):
    with open(rf'{TempDirPath}\Status.data', 'w', encoding='utf-8') as file:
        file.write(Status)

def GetAssistantStatus():
    with open(rf'{TempDirPath}\Status.data', 'r', encoding='utf-8') as file:
        Status = file.read()
    return Status

def MicButtonInitialed():
    SetMicrophoneStatus("False")

def MicButtonClosed():
    SetMicrophoneStatus("True")

def GraphDirectoryPath(Filename):
    Path = rf'{GraphicsDirPath}\{Filename}'
    return Path

def TempDirectoryPath(Filename):
    Path = rf'{TempDirPath}\{Filename}'
    return Path

def ShowTextToScreen(Text):
    with open(rf'{TempDirPath}\Responses.data', "w", encoding='utf-8') as file:
        file.write(Text)

class ChatSection(QWidget):
    def __init__(self):
        super(ChatSection, self).__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        self.chat_text_edit.setStyleSheet("""
            QTextEdit {
                    background-color: #1B1B3A;
                    color: #E0E0E0;
                    border-radius: 10px;
                    padding: 10px;
                    font-size: 20px;
                    border: 2px solid #5D9CEC;  /* Add a border */
                    selection-background-color: #81A1C1;  /* Change selection background */
                    selection-color: #ECEFF4;             /* Change selection text color */
                }       """)
        layout.addWidget(self.chat_text_edit)

        self.gif_label = QLabel()
        self.gif_label.setStyleSheet("border: none;")
        movie = QMovie(GraphDirectoryPath('Jarvis.gif'))
        movie.setScaledSize(QSize(500, 300))
        self.gif_label.setMovie(movie)
        movie.start()
        layout.addWidget(self.gif_label, alignment=Qt.AlignRight)

        self.label = QLabel("")
        self.label.setStyleSheet("color: #ECEFF4; font-size: 22px;")
        layout.addWidget(self.label, alignment=Qt.AlignRight)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadmessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)

    def loadmessages(self):
        global old_chat_message
        with open(TempDirectoryPath('Responses.data'), "r", encoding='utf-8') as file:
            messages = file.read()
            if messages != old_chat_message:
                self.addMessage(message=messages, color='#ECEFF4')
                old_chat_message = messages

    def SpeechRecogText(self):
        with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
            messages = file.read()
            self.label.setText(messages)

    def addMessage(self, message, color):
        cursor = self.chat_text_edit.textCursor()
        format = QTextCharFormat()

        # Set the font to Arial, size 14, and apply a slight boldness
        font = QFont("Arial", 12)
        font.setWeight(QFont.Weight(60))  # Slight boldness (Normal is 50, Bold is 75)

        format.setFont(font)
        format.setForeground(QColor(color))

        cursor.setCharFormat(format)
        cursor.insertText(message + "\n")
        cursor.insertText( "\n")
        
        self.chat_text_edit.setTextCursor(cursor)


class InitialScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Background Gradient
        self.setStyleSheet("""
            InitialScreen {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #4C566A, stop:1 #2E3440);
            }
        """)

        gif_label = QLabel()
        movie = QMovie(GraphDirectoryPath('Jarvis.gif'))
        movie.setScaledSize(QSize(1200, 700))
        gif_label.setMovie(movie)
        gif_label.setAlignment(Qt.AlignCenter)
        movie.start()
        layout.addWidget(gif_label)

        self.icon_label = QLabel()
        pixmap = QPixmap(GraphDirectoryPath('Mic_on.png'))
        new_pixmap = pixmap.scaled(80, 80)
        self.icon_label.setPixmap(new_pixmap)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.toggled = True
        self.toggle_icon()
        self.icon_label.mousePressEvent = self.toggle_icon
        layout.addWidget(self.icon_label)

        self.label = QLabel("")
        self.label.setStyleSheet("color: #ECEFF4; font-size: 20px;")
        layout.addWidget(self.label, alignment=Qt.AlignCenter)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)

    def SpeechRecogText(self):
        with open(TempDirectoryPath('Status.data'), 'r', encoding='utf-8') as file:
            messages = file.read()
            self.label.setText(messages)

    def load_icon(self, path, width=80, height=80):
        pixmap = QPixmap(path)
        new_pixmap = pixmap.scaled(width, height)
        self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(GraphDirectoryPath('Mic_on.png'))
            MicButtonInitialed()
        else:
            self.load_icon(GraphDirectoryPath('Mic_off.png'))
            MicButtonClosed()
        self.toggled = not self.toggled

class MessageScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.chat_section = ChatSection()
        layout.addWidget(self.chat_section)

        self.setStyleSheet("""
            MessageScreen {
                background: #5D9CEC;
            }
        """)

class CustomTopBar(QWidget):
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.initUI()
        self.current_screen = None
        self.stacked_widget = stacked_widget

    def initUI(self):
        self.setFixedHeight(60)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(10)

        self.setStyleSheet("""
            CustomTopBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4C566A, stop:1 #2E3440);
                border-radius: 10px;
            }
        """)

        home_button = QPushButton("Home")
        home_button.setIcon(QIcon(GraphDirectoryPath("Home.png")))
        home_button.setStyleSheet("""
            QPushButton {
                background-color: #81A1C1;
                color: #ECEFF4;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
        """)
        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        message_button = QPushButton("Chat")
        message_button.setIcon(QIcon(GraphDirectoryPath("Chats.png")))
        message_button.setStyleSheet("""
            QPushButton {
                background-color: #81A1C1;
                color: #ECEFF4;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
        """)
        message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        minimize_button = QPushButton()
        minimize_button.setIcon(QIcon(GraphDirectoryPath("Minimize2.png")))
        minimize_button.setStyleSheet("""
            QPushButton {
                background-color: #81A1C1;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
        """)
        minimize_button.clicked.connect(self.minimizeWindow)

        self.maximize_button = QPushButton()
        self.maximize_button.setIcon(QIcon(GraphDirectoryPath("Maximize.png")))
        self.maximize_button.setStyleSheet("""
            QPushButton {
                background-color: #81A1C1;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
        """)
        self.maximize_button.clicked.connect(self.maximizeWindow)

        close_button = QPushButton()
        close_button.setIcon(QIcon(GraphDirectoryPath("Close.png")))
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #81A1C1;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
        """)
        close_button.clicked.connect(self.closeWindow)

        title_label = QLabel(f"{str(Assistantname).capitalize()} AI")
        title_label.setStyleSheet("color: #ECEFF4; font-size: 20px;font-weight: bold;")

        layout.addWidget(title_label)
        layout.addStretch(1)
        layout.addWidget(home_button)
        layout.addWidget(message_button)
        layout.addStretch(1)
        layout.addWidget(minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(close_button)

    def minimizeWindow(self):
        self.parent().showMinimized()

    def maximizeWindow(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setIcon(QIcon(GraphDirectoryPath("Maximize.png")))
        else:
            self.parent().showMaximized()
            self.maximize_button.setIcon(QIcon(GraphDirectoryPath("Minimize.png")))

    def closeWindow(self):
        self.parent().close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()

        stacked_widget = QStackedWidget(self)
        initial_screen = InitialScreen()
        message_screen = MessageScreen()
        stacked_widget.addWidget(initial_screen)
        stacked_widget.addWidget(message_screen)

        self.setGeometry(0, 0, screen_width, screen_height)
        self.setStyleSheet("background-color: #1B1B3A;")

        top_bar = CustomTopBar(self, stacked_widget)
        self.setMenuWidget(top_bar)
        self.setCentralWidget(stacked_widget)

def GraphicalUserInterface():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    GraphicalUserInterface()