"""
GUI for the application
"""
from tkinter import *
import source.Converter as C
import win32clipboard


CF_RTF = win32clipboard.RegisterClipboardFormat("Rich Text Format")
URL_NOT_FOUND_ERR = 'Error: could not find url %s'

# creating the window
window = Tk()
window.title('Harvard Citations Converter')
window.geometry('808x710')
window.configure()

# entry - list of urls split by commas
entry = Entry(window, width=120)
entry.grid(column=0, row=0)
entry.focus()

#where the conversion will be printed
result = Text(window, height=40, width=100)
result.grid(column=0, row=2)


"""
Function for when the button is clicked - will convert the urls, print to the gui and copy to clipboard
"""
def clicked():
    result.delete("1.0", END)
    names = ''.join(entry.get().split()).replace(' ', '').split(',')
    result.tag_config('page_title', font='arial 12 italic')
    result.tag_config('regular', font='arial 12')
    string_arr = ["{\\rtf1\\ansi\\deff0 {\\par "]

    for name in names:
        try:
            s = C.website(name)
            for _ in range(len(s)):
                value = s[_]
                if _ == 2:
                    result.insert(INSERT, value, 'page_title')
                    string_arr.append("\\i " + value + "\\i0")
                else:
                    result.insert(INSERT, value, 'regular')
                    string_arr.append(value)
        except ConnectionError:
            error = URL_NOT_FOUND_ERR % name
            result.insert(INSERT, error)
            string_arr.append(error)

        string_arr.append("\\line ")
        result.insert(INSERT, '\n')

    string_arr.append("\\par}")
    string_rtf = ''.join(string_arr)

    print(string_rtf)
    rtf = bytearray(string_rtf, 'utf8')

    win32clipboard.OpenClipboard(0)
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(CF_RTF, rtf)
    win32clipboard.CloseClipboard()


convert_button = Button(window, text='Convert and Copy to Clipboard', command=clicked, height=1, width=50)
convert_button.grid(column=0, row=1)

window.mainloop()
