import pandas as pd
import numpy as np


def validate_input(message, valid_inputs, list_input=False):
    """
    Validate user input for both single entry and multiple entries
    Return single entry as a string and mutliple entries as a list
    """
    while True:
        user_input = input(message)
        if list_input:
            user_input = [x.lower().strip() for x in user_input.split(',')]
            if len([x for x in user_input if x not in valid_inputs])==0:
                break
        else:
            if user_input.lower() in valid_inputs:
                break
        
    return user_input


def check_col(df, col_name):
    if col_name in df.columns:
        return True
    else:
        print("No data on {} for this city. ".format(col_name))
        return False