import PySimpleGUI as sg
import database_interface



def get_contact_records():
    contact_records = database_interface.retrieve_contacts()
    return contact_records




def create():
    contact_records_array = get_contact_records()
    headings = ['Booking ID', 'Last_searched_date']

    contact_information_window_layout = [
        [sg.Table(values=contact_records_array, headings=headings, max_col_width=35,
                    auto_size_columns=True,
                    display_row_numbers=True,
                    justification='center',
                    num_rows=10,
                    key='-TABLE-',
                    selected_row_colors='blue on grey',                    
                    expand_x=True,
                    expand_y=True,
                    row_height=35,
                    tooltip='Reservations Table')]
    ]

    contact_information_window = sg.Window("History Window", 
    contact_information_window_layout, modal=True, size=(500,300))

    while True:
        event, values = contact_information_window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        
    contact_information_window.close()
def clear_record():    
    database_interface.delete_history()    
    print("Cleared all history!")