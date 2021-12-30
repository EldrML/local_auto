"""
A python script to extract data from text files which are poorly formatted fixed-width.
Written in Fall 2021 to parse information from spacelaunchreport.com by Liam Durbin.
"""
#region IMPORTS
from pathlib import Path
import pandas as pd
import numpy as np
#endregion

#region VARIABLES
# Path to the text files.
ABS_PATH_       = r'C:\Users\Liam\Desktop\_grad_school\_Fall 2021\AAE 590\final_project\txt_files'

# Names of the text files to scan.
file_names      = ['Early','Titan','Thor','Atlas','MX','Pegasus','Scout','SpaceShuttle']

# Columns within the text files.
txt_file_categ  = ['Date','Vehicle','ID','Site', 'Payload','Failure Description','Result#']

# Columns desired for the table export.
table_columns   = ['Date','Family','Vehicle','ID','Site','Pad',
                   'Payload','Failure Description','Result#']
txt_file_list   = []
#endregion

def get_column_widths(header_str, col_names):
    """
    Logic to get the distance between columns based on the number of spaces between the headers.
    """
    col_split   = []
    col_width   = []

    for categ in col_names:             #For each category name
        col_flag    = True
        col_count   = 0
        i           = 0
        waiting_for_next_col = False

        while col_flag: #Checking for column's name to match

            if not waiting_for_next_col and header_str[i] == categ[i]:
                col_count   += 1
                i           += 1
                if col_count == len(categ)-1:
                    waiting_for_next_col = True
                    i       += 1

            elif waiting_for_next_col and i == len(header_str) or header_str[i] != ' ':
                col_text = header_str[0:col_count+1]
                col_split.append(col_text)
                col_width.append(col_count+1)
                header_str = header_str.replace(col_text,'')
                col_flag = False

            elif waiting_for_next_col and header_str[i] == ' ':
                col_count   += 1
                i           += 1

    return col_split, col_width

#region MAIN CODE
table_array = []

for filename in file_names:

    filepath = Path(ABS_PATH_,filename+'.txt')
    f = open(filepath,'r')
    content = f.read()
    f.close()

    # Isolate the Header Line and data.
    header_line = content.partition('\n\n')[2].partition('\n------')[0]
    faildata    = content.partition('----\n')[2].partition('\n----')[0].split("\n")

    # Get the Width of each column.
    (col_names, col_lens) = get_column_widths(header_line, txt_file_categ)

    # Split the faildata into columns based on their lengths.
    for row in faildata:                # For each line:
        row_array   = []
        for j, col in enumerate(txt_file_categ):  # For each column:

            # Add a "family" column
            if col == txt_file_categ[1]:
                family_text = filename
                row_array.append(family_text.strip())

            # Get the text to write
            list_text = row[0:col_lens[j]]

            if col == txt_file_categ[3]:
                # Split Site column into location and launchpad
                site_text   = list_text[0:2]
                pad_text    = list_text[3:-1]
                row_array.append(site_text.strip())
                row_array.append(pad_text.strip())
            else:
                # Write the text directly.
                row_array.append(list_text.strip())

            # Strip out the text from the str.
            row = row.replace(list_text,'',1) 

        # Add the columns to an array.
        table_array.append(row_array)

# Create Output Table.
data_out    = pd.DataFrame(np.array(table_array),columns=table_columns)

# Save to CSV.
OUT_PATH    = r'C:\Users\Liam\Desktop\_grad_school\_Fall 2021\AAE 590\final_project\txt_files\failure_list'
data_out.to_csv(Path(OUT_PATH +'.csv'))
           