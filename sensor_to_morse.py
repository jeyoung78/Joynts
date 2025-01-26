

import time
from PyQt5.QtCore import QTimer, pyqtSignal, QObject

class MorseUpdater(QObject):
    morseUpdated = pyqtSignal(str)
    OnUpdated = pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        
        self.variables = [[False, False, False, False, False], [False, False, False, False, False]]
        self.morse_words = []
        
        self.last_variables = None  # Store the previous state of variables
        self.last_modified = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_morse)
        self.timer.start(1000)  # Adjust the time interval as needed


        
    def update_morse(self):
        current_time = time.time()
        if current_time - self.last_modified > 2:  # Check if morse.txt has been modified
            print(current_time)
            print(self.last_modified)
            with open('morse.txt', 'r') as file:
                lines = file.readlines()
                if lines:
                    # Assuming the format is [[True,False,False,False,False],[False,False,True,False,False],...]
                    variables = eval(lines[0].strip())
                    if isinstance(variables, list) and all(isinstance(v, bool) for v in variables[0]):
                        self.variables = variables
                        # print(self.variables[0])
                        self.last_modified = current_time

                        # Process and emit the Morse code (if needed)
                        # self.process_variables()
                        morse_text =  self.process_variables()
                        with open('morse.txt', 'w') as file:
                            pass
                        # with open('morse.txt', 'w') as file:
                        #     pass
                        print(morse_text)
                        if morse_text:
                            self.morseUpdated.emit(morse_text)
                        self.last_modified = current_time
                        self.last_variables = variables






 
    def process_variables(self):
        morse_word = ""
        on_update = False
        for i in range(len(self.variables)):
            if (self.variables[i][0] and not self.variables[i][1] and not self.variables[i][2] and not self.variables[i][3] and not self.variables[i][4]):
                print(1)
                morse_word += "."
            elif (not self.variables[i][0] and not self.variables[i][1] and self.variables[i][2] and not self.variables[i][3] and not self.variables[i][4]):
                print(2)
                morse_word += "-"
            elif (not self.variables[i][0] and not self.variables[i][1] and not self.variables[i][2] and self.variables[i][3] and not self.variables[i][4]):
                print(3)
                morse_word += " "
                self.morse_words.append(morse_word)
                # morse_word = "" 
                # print(morse_word)
            elif (not self.variables[i][0] and self.variables[i][1] and not self.variables[i][2] and not self.variables[i][3] and not self.variables[i][4]):
                print(4)
                on_update = True
                self.OnUpdated.emit(on_update)


            
        return morse_word
    
    

if __name__ == '__main__':
    morse_updater = MorseUpdater()
    morse_updater.update_morse()  # Start the MorseUpdater


