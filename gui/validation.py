
def validate(values):
    is_valid = True
    values_invalid = []

    if len(values['-AGE-']) == 0:
        values_invalid.append('Age')
        is_valid = False
    
    if len(values['-RACE-']) == 0:
        values_invalid.append('Race')
        is_valid = False

    if len(values['-BOOKING_ID-']) == 0:
        values_invalid.append('Booking ID')
        is_valid = False
    
    if len(values['-RANGE-']) == 0:
        values_invalid.append('Range')
        is_valid = False

    result = {"is_valid": is_valid, "values_invalid": values_invalid}
    return result

def generate_error_message(values_invalid):
    error_message = ''
    for value_invalid in values_invalid:
        error_message += ('\nInvalid' + ':' + value_invalid)

    return error_message