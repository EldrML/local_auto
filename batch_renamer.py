#import _helper_functions as hf
import os
import re
#from os import rename as rn

os.system('cls')

# testing filepath selection
#folderpath  = hf.search_for_file_path()
folderpath  = r'F:\_SFX\_BOOM Libraries'
#rep_list    = {'boom library - ', 'boom library ', 'boom.Library.', 'boom_', 'BL - -'}
rep_list    = {'Hollywood Edge'}
rep_str     = 'HE'

for filename in os.listdir(folderpath):
    #for front_end in boom_list:
    for rep_item in rep_list:
        regex_replace = re.compile(re.escape(rep_item), re.IGNORECASE)

        if bool(regex_replace.match(filename)):
            os.rename   (   os.path.join(folderpath,filename), 
                            os.path.join(folderpath,regex_replace.sub(rep_str, filename))
                        )
            break
        