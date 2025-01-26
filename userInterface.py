import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QHBoxLayout, QVBoxLayout, QWidget, QTextEdit, QLabel, QTabWidget)
from PyQt5.QtGui import QFont
from morse_to_word import decrypt
import subprocess
import qdarkstyle
from sensor_to_morse import MorseUpdater


currentLineIndex = 0
ladderDiagram = "-------------------------------------------------------------------------------------------------------------------------------------()-----"
nextLine = "--------------------------------------------------------------------------------------------------------------------------------------------"
ladderDiagramList = [
    ladderDiagram,
    nextLine
]
currIdx = 6
output_statement = 'output'

arrayGatesMain = []
arrayGatesParallel = []

class LadderProgrammingConsole(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main window properties
        self.setWindowTitle('PLC Ladder Programming Console')
        self.setGeometry(100, 100, 800, 400)  # Adjusted the size

        # Main tab widget
        self.tab_widget = QTabWidget(self)

        # --- First Tab ---
        first_tab_content = QWidget()

        # Main layout for the first tab
        main_layout_first_tab = QVBoxLayout()
        # Set spacing and margins for the main layout
        main_layout_first_tab.setSpacing(10)
        main_layout_first_tab.setContentsMargins(10, 10, 10, 10)

        # Horizontal layout for buttons
        btn_layout = QHBoxLayout()

        # Create buttons
        self.on_btn = QPushButton('ON', self)
        self.off_btn = QPushButton('OFF', self)
        self.parallel_on_btn = QPushButton('Parallel On', self)
        self.parallel_off_btn = QPushButton('Parallel Off', self)
        self.run_btn = QPushButton('Run', self)

        # Add buttons to horizontal layout
        btn_layout.addWidget(self.on_btn)
        btn_layout.addWidget(self.off_btn)
        btn_layout.addWidget(self.parallel_on_btn)
        btn_layout.addWidget(self.parallel_off_btn)
        btn_layout.addWidget(self.run_btn)

        # Add the horizontal button layout to the main layout of the first tab
        main_layout_first_tab.addLayout(btn_layout)

        # Add the display area
        self.text_display = QTextEdit(self)
        self.text_display.setText("\n".join(ladderDiagramList))
        main_layout_first_tab.addWidget(self.text_display)

        # Add a small output section at the bottom
        self.output_label = QLabel("Out displayed here", self)
        main_layout_first_tab.addWidget(self.output_label)
        self.output_label.setStyleSheet("background-color: #f2f2f2; color: #333;")

        first_tab_content.setLayout(main_layout_first_tab)
        self.tab_widget.addTab(first_tab_content, "Ladder Diagram")

        # --- Second Tab (Mini Python IDE) ---
        second_tab_content = QWidget()
        layout_second_tab = QVBoxLayout()

        self.code_editor = QTextEdit(self)
        layout_second_tab.addWidget(self.code_editor)
        self.morse_updater = MorseUpdater()
        self.morse_updater.morseUpdated.connect(self.update_morse_editor)
        # Set the font for the code_editor
        font = QFont("Courier New", 10)
        self.code_editor.setFont(font)

        self.run_code_btn = QPushButton("Run", self)
        self.run_code_btn.clicked.connect(self.run_python_code)
        layout_second_tab.addWidget(self.run_code_btn)

        second_tab_content.setLayout(layout_second_tab)
        self.tab_widget.addTab(second_tab_content, "Mini Python IDE")

        # Set the tab widget as the central widget
        self.setCentralWidget(self.tab_widget)

        # Connect buttons to respective functionalities (to be implemented)
        self.on_btn.clicked.connect(self.on_btn_function)
        self.off_btn.clicked.connect(self.off_btn_function)
        self.parallel_off_btn.clicked.connect(self.parallel_off_btn_function)
        self.parallel_on_btn.clicked.connect(self.parallel_on_btn_function)
        self.run_btn.clicked.connect(self.run_btn_function)
        # Style buttons
        self.on_btn.setStyleSheet("background-color: #333; color: #eee; border: 1px solid #555;")
        self.off_btn.setStyleSheet("background-color: #333; color: #eee; border: 1px solid #555;")
        self.parallel_on_btn.setStyleSheet("background-color: #333; color: #eee; border: 1px solid #555;")
        self.parallel_off_btn.setStyleSheet("background-color: #333; color: #eee; border: 1px solid #555;")
        self.run_btn.setStyleSheet("background-color: #333; color: #eee; border: 1px solid #555;")

        font_label = QFont("Verdana", 9)
        self.output_label.setFont(font_label)
    def convert_morse_to_english(self, morse_text):
        MORSE_CODE_DICT = { 'a':'.-', 'b':'-...', 'c':'-.-.', 'd':'-..', 'e':'.',
                            'f':'..-.', 'g':'--.', 'h':'....', 'i':'..', 'j':'.---',
                            'k':'-.-', 'l':'.-..', 'm':'--', 'n':'-.', 'o':'---',
                            'p':'.--.', 'q':'--.-', 'r':'.-.', 's':'...', 't':'-',
                            'u':'..-', 'v':'...-', 'w':'.--', 'x':'-..-', 'y':'-.--',
                            'z':'--..', '1':'.----', '2':'..---', '3':'...--',
                            '4':'....-', '5':'.....', '6':'-....', '7':'--...',
                            '8':'---..', '9':'----.', '0':'-----', ', ':'--..--',
                            '.':'.-.-.-', '?':'..--..', '/':'-..-.', '-':'-....-',
                            '(':'-.--.', ')':'-.--.-', ':': '---...', '"':'.-..-.', ' ': '.-.-'}
    
        def decrypt(message):
            message += ' '
            decipher = ''
            citext = ''
            if (len(message) > 0):

                for letter in message:
                    if (letter != ' '):
                        i = 0
                        citext += letter
                    else:
                        i += 1
                        if i == 2:
                            decipher += ' '
                        else:
                            decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(citext)]
                            citext = ''
            return decipher

        return decrypt(morse_text)
    def update_morse_editor(self, morse_text):
        # self.code_editor.append(morse_text)
        english_text = self.convert_morse_to_english(morse_text)
        if (english_text != ''):
            self.code_editor.append(english_text)
    def run_python_code(self):
        code = self.code_editor.toPlainText()
        with open("userWritten.py", "w") as file:
            file.write(code)

        # Run the script
        result = subprocess.run(["python", "userWritten.py"], capture_output=True, text=True)

        # Optionally, display the output or errors in the IDE (can use a QLabel or another QTextEdit).
        # Here's a simple example of displaying the output in a QLabel below the Run button:
        output_label = QLabel(result.stdout if result.stdout else result.stderr, self)
        self.output_label.setStyleSheet("background-color: #f2f2f2; color: #333;")
        layout = self.tab_widget.currentWidget().layout()
        layout.addWidget(output_label)

    def on_btn_function(self):
        global ladderDiagramList, currIdx
        # Your logic here
        print(currIdx)
        currentLine = ladderDiagramList[0]  # First line
        currentLine = currentLine[:currIdx - 1] + '[' + ' ' + ']' + currentLine[currIdx + 2:]
        ladderDiagramList[0] = currentLine
        self.text_display.setText("\n".join(ladderDiagramList))
        arrayGatesMain.append([True, currIdx])
        currIdx = currIdx + 8

    def off_btn_function(self):
        global ladderDiagramList, currIdx
        # Your logic here
        print(currIdx)
        currentLine = ladderDiagramList[0]  # First line
        currentLine = currentLine[:currIdx - 1] + '[' + '/' + ']' + currentLine[currIdx + 2:]
        ladderDiagramList[0] = currentLine
        self.text_display.setText("\n".join(ladderDiagramList))
        arrayGatesMain.append([False, currIdx])
        currIdx = currIdx + 8  # Assuming you still want the cursor index to move after pressing the off button

    def parallel_off_btn_function(self):
        global currIdx, ladderDiagramList
        print(currIdx)
        currentLine = ladderDiagramList[1]  # First line
        currentLine = currentLine[:currIdx - 1] + '[' + '/' + ']' + currentLine[currIdx + 2:]
        ladderDiagramList[1] = currentLine
        self.text_display.setText("\n".join(ladderDiagramList))
        arrayGatesParallel.append([False, currIdx])

    def parallel_on_btn_function(self):
        global currIdx, ladderDiagramList
        print(currIdx)
        currentLine = ladderDiagramList[1]  # First line
        currentLine = currentLine[:currIdx - 1] + '[' + ' ' + ']' + currentLine[currIdx + 2:]
        ladderDiagramList[1] = currentLine
        self.text_display.setText("\n".join(ladderDiagramList))
        arrayGatesParallel.append([True, currIdx])

    def run_btn_function(self):
        self.output_label.setText("Run pressed!")
        print(arrayGatesMain)
        print(arrayGatesParallel)
        for i in range(len(arrayGatesParallel)):
            for idx in range(len(arrayGatesMain)):
                if (arrayGatesParallel[i][1] == arrayGatesMain[idx][1]) and (arrayGatesParallel[i][0] == True):
                    arrayGatesMain[idx][0] = True
        print(arrayGatesMain)

        result = True
        for i in range(len(arrayGatesMain)):
            if arrayGatesMain[i][0] == False:
                result = False

        result_text = str(result)
        self.output_label.setText(result_text)
    def triggerOnButton(self):
        self.on_btn_function

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    window = LadderProgrammingConsole()
    window.show()
    # window.triggerOnButton()
    sys.exit(app.exec_())
