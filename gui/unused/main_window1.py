import PySimpleGUI as sg
import information_window
import database_interface
import validation
import run_script
from datetime import datetime

username = 'admin'
password = 'admin'

def process():
    layout1 = [[sg.Text("Enter Age:"), sg.Input(key='-NAME-', do_not_clear=True, size=(80, 1))],
            [sg.Text("Enter RACE:"), sg.Input(key='-ADDRESS-', do_not_clear=True, size=(80, 1))],
            [sg.Text("Enter Range:"), sg.Input(key='-PHONE_NUMBER-', do_not_clear=True, size=(80, 1))],
            [sg.Button('Add And Run Script',size=(30, 1)), sg.Button('Show History', size=(30, 1)), sg.Exit()],
            [sg.Output(size=(80,15))]]


    window = sg.Window("Python Script GUI", layout1, size=(500,300), grab_anywhere=True, element_justification='c')
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == 'Add And Run Script':
            validation_result = validation.validate(values)
            if validation_result["is_valid"]:

                last_searched_date = datetime.now()
                last_searched_date.strftime('%m/%d/%Y')

                database_interface.insert_contact(values['-NAME-'], values['-ADDRESS-'], values['-PHONE_NUMBER-'], last_searched_date)
                sg.popup("Inputed and runing script...")
                range = values['-PHONE_NUMBER-']
                race = values['-ADDRESS-']
                age = values['-NAME-']
                cmd = "python database.py " + str(range) + " 20 "+ "--race " + str(race) +" --age " + str(age)
                run_script.runCommand(cmd, window=window)
            else:
                error_message = validation.generate_error_message(validation_result["values_invalid"])
                sg.popup(error_message)
        elif event == 'Show History':
            information_window.create()

# layout = [[sg.Text("Log In", size =(15, 1), font=40)],
#         [sg.Text("Username", size =(15, 1), font=16),sg.InputText(key='-usrnm-', font=16)],
#         [sg.Text("Password", size =(15, 1), font=16),sg.InputText(key='-pwd-', password_char='*', font=16)],
#         [sg.Button('Ok'),sg.Button('Cancel')]]

# window = sg.Window("Log In", layout)

# while True:
#     event,values = window.read()
#     if event == "Cancel" or event == sg.WIN_CLOSED:
#         break
#     else:
#         if event == "Ok":
#             if values['-usrnm-'] == username and values['-pwd-'] == password:
#                 sg.popup("Welcome!")
#                 process()
#                 break
#             elif values['-usrnm-'] != username or values['-pwd-'] != password:
#                 sg.popup("Invalid login. Try again")

#     window.close()



