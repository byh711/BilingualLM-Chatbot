# -*- coding:utf-8 -*-
'''
This module checks columns of the 'test.csv' file, extracts the necessary information,
and sends appropriate data to the 'parse_tree.py' file for further processing.
'''

import time
import traceback
from Working_code import config as cf
from Working_code import parse_tree as pt

# Set logger
logger = cf.logging.getLogger("__state_checker__")

def get_line_from_csv(csvfile):
    """Continuously read the current line of the given CSV file."""
    csvfile.seek(0,2)  # Move to the last line of the file
    while True:
        try:
            line = csvfile.readlines()[-1]
        except:
            time.sleep(0.1)   
            continue
        yield line

def update_data_from_csv(csvfile, initial_state):
    """
    Append data to the lists from the CSV and send it to the 'parse_tree.py' for further processing.
    """
    lines = get_line_from_csv(csvfile)
    global no_columns_csv
    for line in lines:
        row = line.split(',')  # Split the line by ',' as the format is CSV

        if row[0] == '\n':  # Skip empty lines
            continue

        try:
            if row[0] != 'OS_timestamp' and (len(row)-1) == no_columns_csv:
                # Extract relevant data
                cf.data.update({
                    'Phase': row[2],
                    'Hunger_AVATAR': row[11],
                    'Health_AVATAR': row[10],
                    'Sanity_AVATAR': row[12],
                    'Curr_Active_Item_AVATAR': row[8],
                    'Curr_Equip_Hands_AVATAR': row[9],
                    'Attack_Target_AVATAR': row[13],
                    'Defense_Target_AVATAR': row[14],
                    'Food_AVATAR': float(row[16]),
                    'Tool_AVATAR': row[22],
                    'Lights_AVATAR': row[23],
                    'Is_Fireplace_AVATAR': row[24],
                    'Is_Light_AVATAR': row[25],
                    'Is_Monster_AVATAR': int(row[26]),
                    'Twigs_AVATAR': int(row[17]),
                    'Flint_AVATAR': int(row[18]),
                    'Rock_AVATAR': int(row[19]),
                    'Grass_AVATAR': int(row[20]),
                    'Log_AVATAR': int(row[21]),
                    'Player_Xloc': row[34]
                })

                # Send the current state data to 'parse_tree.py' for processing
                logger.info("Update state and hand over to decision tree.")
                pt.parse_decision_tree(cf.data, initial_state)
            else:
                pass

        except Exception as e:
            logger.error('Error reading current line as data: %s', e)
            logger.error('The line is: ' + line)
            logger.error(traceback.format_exc())

def state_changed_withoutHandler():
    """
    Monitor the CSV file for game updates, process it to a new representation (if necessary),
    and then execute the decision tree for the virtual avatar.
    """
    logger.info('Opening the CSV file and regularly checking for added lines')

    # Set up empty initial state for Avatar data
    cf.initial_state.update({
        'Phase': '',
        'Huger_AVATAR': '',
        'Health_AVATAR': '',
        'Sanity_AVATAR': '',
        'Curr_Active_Item_AVATAR': '',
        'Curr_Equip_Hands_AVATAR': '',
        'Attack_Target_AVATAR': '',
        'Defense_Target_AVATAR': '',
        'Food_AVATAR': '',
        'Tool_AVATAR': '',
        'Lights_AVATAR': '',
        'Is_Fireplace_AVATAR': '',
        'Is_Light_AVATAR': '',
        'Is_Monster_AVATAR': '',
        'Twigs_AVATAR': '',
        'Flint_AVATAR': '',
        'Rock_AVATAR': '',
        'Grass_AVATAR': '',
        'Log_AVATAR': '',
        'Player_Xloc': ''
    })

    try:
        with open(cf.INTERFACE_FILEFOLDER, 'r', encoding='utf-8', newline='') as csvfile:
            csvheader = csvfile.readline().strip().split(',')
            global no_columns_csv
            no_columns_csv = len(csvheader) - 1  # Count all columns

            logger.debug(' printing all header names: ')

            # Write down column information to log file
            for i in range(no_columns_csv):
                logger.debug('%s : %s', i, csvheader[i])
                
            update_data_from_csv(csvfile, cf.initial_state)

    except Exception as e:
        logger.error('Error during opening csv file: %s', e)