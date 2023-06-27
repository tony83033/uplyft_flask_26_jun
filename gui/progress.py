import PySimpleGUI as sg
import time
def run():
    layout = [
        [sg.ProgressBar(max_value=1000, orientation='h', size=(50,20), key="-PROG-")]
    ]

    window = sg.Window("Progressing", layout)
    for i in range(10):
        event, values = window.read(timeout=5)
        if event == "Cancel":
            window.close()
        window["-PROG-"].UpdateBar(i+1)
    print("Currently we are processing script, please wait..."+"\n")
    time.sleep(3)
    print("Result will be displayed in this box."+"\n")
    # print(event, values)
    window.close()
