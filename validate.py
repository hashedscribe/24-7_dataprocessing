# ---------------------------------- IMPORTS --------------------------------- #
# DATETIMES
from datetime import datetime, timedelta, timezone
from settings import DATETIME_FORMAT, KERNEL_TIME

# ARCHITECTURE
from settings import NUM_BLOCKS_PER_DAY, NUM_BLOCKS_PER_FILE, NUM_DAYS_PER_FILE

# MASKS
from settings import MASK_WRITTEN, MASK_NOTE, MASK_CATEGORY, MASK_LINDEX


# -------------------------------- VALIDATORS -------------------------------- #

def check_file_arr(array, warnings = False, verbose = False):
    print(array)
    
    # check that the number of days is correct per file
    if(len(array) < NUM_DAYS_PER_FILE and warnings):
        print("WARNING: found less than " + str(NUM_DAYS_PER_FILE) + " lines/days recieved.")
    elif(len(array) > NUM_DAYS_PER_FILE):
        raise ValueError("ERROR: found more than" + str(NUM_DAYS_PER_FILE) + " lines/days recieved. Aborting.")
    elif(verbose):
        print("Passed: Number of lines/days is as expected.")
        
        
    header = None
    flagged_warning = False
    seen = set()
    
    for day in array:
        #  check that all the headers are matching
        if header == None:
            header = day["header"]
        elif(day["header"] != header):
            raise ValueError("ERROR: headers within files do not match. Expected " + 
                             str(header) + ", recieved " + str(day["header"]) + ". Aborting.")
        
        # check that the number of blocks per day is correct
        if(len(day["data"]) < NUM_BLOCKS_PER_DAY and warnings):
            print("WARNING: found less than " + str(NUM_BLOCKS_PER_DAY) + " blocks.")
            flagged_warning = True
        elif(len(day["data"]) > NUM_BLOCKS_PER_DAY):
            raise ValueError("ERROR: found more than" + str(NUM_BLOCKS_PER_DAY) + 
                             " blocks. Aborting.")
        
        # check that there are no duplicate blocks in each file
        for block in day["data"]:
            if(block in seen):
                raise ValueError("ERROR: found duplicate block. Aborting.")
            else:
                seen.add(block)
        
        # check that the local index is within bounds
        local_index = (block & MASK_LINDEX) >> 8
        if(local_index < 0 or local_index >= NUM_BLOCKS_PER_FILE):
            raise ValueError("ERROR: local index of " + str(block) + " is " + 
                             str(local_index) + ". Aborting.")
              
    
    if(not flagged_warning and verbose):
        print("Passed: Blocks meets invariant requirements.")
            
    
    