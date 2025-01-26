import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtCore import QTimer
import subprocess
import serial

ser = serial.Serial('COM3', 2400)

class SimpleIDE(QWidget):
    def __init__(self):
        super().__init__()

        # State variable for button colors
        self.lightStates = [True, False, True]

        self.initUI()

        # Start a QTimer to toggle button colors every 2 seconds
        self.dataTimer = QTimer(self)
        self.dataTimer.timeout.connect(self.fetchExternalData)
        self.dataTimer.start(1)  # Timeout is in milliseconds

    def initUI(self):
        layout = QVBoxLayout()

        # Text editor
        self.textEdit = QTextEdit(self)
        layout.addWidget(self.textEdit)

        # Run script button
        self.runButton = QPushButton('Run', self)
        self.runButton.clicked.connect(self.runScript)
        layout.addWidget(self.runButton)

        # Light up buttons
        self.lightUpButtons = [QPushButton(f"Button {i}", self) for i in range(1, 4)]
        for btn in self.lightUpButtons:
            layout.addWidget(btn)

        self.setLayout(layout)
        self.setWindowTitle('Simple IDE')
        self.setGeometry(300, 300, 600, 400)

    def saveToFile(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Python Files (*.py);;All Files (*)")
        if filename:
            with open(filename, 'w') as file:
                file.write(self.textEdit.toPlainText())
        return filename

    def runScript(self):
        filename = self.saveToFile()
        if filename:
            output = subprocess.check_output(['python', filename])
            QMessageBox.information(self, 'Output', output.decode())
        else:
            QMessageBox.warning(self, 'Warning', 'Failed to save or run the script.')

    def updateButtonColors(self, lightStates):
        for btn, state in zip(self.lightUpButtons, lightStates):
            color = "green" if state else "red"
            btn.setStyleSheet(f"background-color: {color};")

    def toggleButtonColors(self):
        # Toggle the states
        self.lightStates = [not state for state in self.lightStates]
        self.updateButtonColors(self.lightStates)

    def fetchExternalData(self):
        # Fetch the external data (this is a placeholder, replace with real data fetching logic)
        new_data = self.getDataFromSource()

        # Update the button colors based on the new data
        self.updateButtonColors(new_data)

    def getDataFromSource(self):
        # Placeholder method. Replace with actual logic to get data from your external source.
        # For demonstration, we simply toggle the states
        line = ser.readline().decode('utf-8').strip()

        # Convert the comma-separated string to a list of integers
        data = list(map(int, line.split(',')))
        return data

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SimpleIDE()
    ex.show()
    sys.exit(app.exec_())
