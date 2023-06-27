import PySimpleGUI as sg
import information_window
import database_interface
import validation
import run_script
from datetime import datetime

username = 'admin'
password = 'admin'

def process():
    layout1 = [
            [sg.Text("Booking ID: (Example:23450)"), sg.Input(key='-BOOKING_ID-', do_not_clear=True, size=(80, 1))],
            [sg.Text("Result Range: (Example:20)"), sg.Input(key='-RANGE-', do_not_clear=True, size=(80, 1))],
            [sg.Text("Age Range: (Example:20-30)"), sg.Input(key='-AGE-', do_not_clear=True, size=(80, 1))],
            [sg.Text("Enter RACE: (Example:white)"), sg.Input(key='-RACE-', do_not_clear=True, size=(80, 1))],
            [sg.Button('Add And Run Script',size=(30, 1)), sg.Button('Show History', size=(20, 1)), sg.Button('Clear History', size=(20, 1)), sg.Exit()],
            [sg.Output(size=(100,50))]]


    window = sg.Window("Python Script GUI", layout1, size=(800,600), grab_anywhere=True, element_justification='c')

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == 'Add And Run Script':
            validation_result = validation.validate(values)
            if validation_result["is_valid"]:

                last_searched_date = datetime.now()
                last_searched_date.strftime('%m/%d/%Y')

                database_interface.insert_contact(values['-AGE-'], values['-RACE-'], values['-BOOKING_ID-'], last_searched_date, values['-RANGE-'])
                booking_id = values['-BOOKING_ID-']
                range = values ['-RANGE-']
                race = values['-RACE-']
                age = values['-AGE-']
                cmd = "python3 script.py " + str(booking_id) + " " + str(range) + " --race " + str(race) +" --age " + str(age)
                sg.popup("Are you sure?")
                run_script.runCommand(cmd, window=window)

            else:
                error_message = validation.generate_error_message(validation_result["values_invalid"])
                sg.popup(error_message)
        elif event == 'Show History':
            information_window.create()
        elif event == 'Clear History':
            information_window.clear_record()
def login():
    layout = [[sg.Text("Log In", size =(15, 1), font=40)],
            [sg.Text("Username", size =(15, 1), font=16),sg.InputText(key='-usrnm-', font=16)],
            [sg.Text("Password", size =(15, 1), font=16),sg.InputText(key='-pwd-', password_char='*', font=16)],
            [sg.Button('Ok'),sg.Button('Cancel')]]

    window = sg.Window("Log In", layout)

    while True:
        event,values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        else:
            if event == "Ok":
                if values['-usrnm-'] == username and values['-pwd-'] == password:
                    sg.popup("Welcome admin!")
                    window.close()
                    process()
                    break
                elif values['-usrnm-'] != username or values['-pwd-'] != password:
                    sg.popup("Invalid login. Try again")

        window.close()

if __name__=='__main__':
    # login()
    process()

