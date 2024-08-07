# this removes markdown formatting that LEGA outputs
# @author: Jasmine Klein
# @version: 1.1

import re
import tkinter as tk
from tkinter import *

class Window():

    def __init__(self):

        self.OLD_TEXT =  ""
        self.NEW_TEXT = ""

        # create window
        self.window = tk.Tk()
        self.window.configure(bg='white')
        self.window.geometry("1024x600")
        self.window.title("Remove Markdown")

        self.vscroll = tk.Scrollbar(self.window, orient=tk.VERTICAL)
        self.hscroll = tk.Scrollbar(self.window, orient=tk.HORIZONTAL)

        # initalize non reactive components
        self.setup()

        # textbox that user inputs the raw lega data into 
        self.input_text = tk.Text(self.window, pady=10, padx=10, height=24, width=70)
        self.input_text.grid(row=3, column=0)
        self.input_text.config(font=("Calibri", 11))

        # textbox to display cleaned data
        self.output_text = tk.Text(self.window, pady=10, padx=10, height=24, width=70)
        self.output_text.grid(row=3, column=1)
        self.output_text.config(font=("Calibri", 11), yscrollcommand=self.vscroll)

        # button to initate formatting
        self.format_button = tk.Button(self.window, text="reformat!", fg='#ff4216', borderwidth=0, cursor='hand2', highlightthickness = 0, command=self.__get_input__)
        self.format_button.grid(row=1, column=0, pady=10)

        # button to clear both text fields and start over, this could be done bteer some way
        self.reset_button = tk.Button(self.window, text="clear text", borderwidth=0, cursor='hand2', command=self.reset)
        self.reset_button.grid(row=4, column=0, padx=10, pady=40)

        self.start()

    # set visuals and static components
    def setup(self):
        # like a textbox for instructions lowkey
        subhead_text = "paste your raw LEGA response into left textbox and press reformat to remove markdown formatting" 
        subhead_label = tk.Label(self.window, text=subhead_text, bg = 'white', wraplength=650)
        subhead_label.grid(row=0, column=0, columnspan=3)
        subhead_label.config(font=("Calibri", 12))

    # handler for buttons
    def button_state(self, button):
        # button logic...duh lol
        if button.cget("state") == "normal":
            button.configure(state="disabled")
        else:
            button.configure(state="normal")

    def start(self):
        self.window.mainloop()

    def reset(self):
        self.window.destroy()
        self.__init__()
    
    def __get_input__(self):
        # get text from user input from left textbox
        self.OLD_TEXT = self.input_text.get(1.0, "end-1c")
        
        # disable format button
        if self.OLD_TEXT != "":
            self.button_state(self.format_button)

        # removes all markdown syntax for headings, bold, italics, bullet list
        text = reformat(str(self.OLD_TEXT))

        sections = text.split('   ') # remove indent spacing
        for section in sections:
            newline = section.split('\n') # break up new lines
            for x in newline:
                self.NEW_TEXT += x.lstrip() + '\n' # remove leading whitespaces, add newline
        
        # display the reformatted text in right text box
        self.__set_output__(self.NEW_TEXT)

    def __set_output__(self, output):

        if output is None:
            output = self.NEW_TEXT

        self.button_state(self.format_button)
        self.output_text.insert("1.0", output)


# returns the input string without any formatting
def reformat(lega: str):
    # define patterns of stuff you want to get rid of
    headings = (r'#{3,}')
    astriks = (r'\*{2,}')

    cleaned = re.sub(headings, '', lega)
    cleaned = cleaned.replace('*', '') # italics and bold

    return cleaned.strip()

    
def main():
    Window()


if __name__ == '__main__':
    main()