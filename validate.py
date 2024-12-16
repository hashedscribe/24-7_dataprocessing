# ---------------------------------- IMPORTS --------------------------------- #
# DATETIMES
from datetime import datetime, timedelta, timezone
from settings import DATETIME_FORMAT, KERNEL_TIME

# ARCHITECTURE
from settings import NUM_BLOCKS_PER_DAY, NUM_BLOCKS_PER_FILE, NUM_DAYS_PER_FILE, INT_MAX

# MASKS
from settings import MASK_WRITTEN, MASK_NOTE, MASK_CATEGORY, MASK_LINDEX


# -------------------------------- VALIDATORS -------------------------------- #
def check_file_arr(array, warnings = False, verbose = False):
    if(verbose):
        print(array)
    flagged_warning = False
    
    # check that the number of days is correct per file
    if(len(array) < NUM_DAYS_PER_FILE and warnings):
        print("WARNING: recieved " + str(len(array)) + " lines/days recieved.")
        flagged_warning = True
    elif(len(array) > NUM_DAYS_PER_FILE):
        raise ValueError("ERROR: recieved " + str(len(array)) + " lines/days recieved. Aborting.")
    elif(verbose):
        print("PASSED: Number of lines/days is as expected.") 
        
    header = None
    seen = set()
    num_blocks = 0
    
    for day in array:
        #  check that all the headers are matching
        if header == None:
            header = day["header"]
        elif(day["header"] != header):
            raise ValueError("ERROR: headers within files do not match. Expected " + 
                             str(header) + ", recieved " + str(day["header"]) + ". Aborting.")
        
        # check that the number of blocks per day is correct
        if(len(day["data"]) < NUM_BLOCKS_PER_DAY and warnings):
            print("WARNING: recieved " + str(len(day["data"])) + " blocks per day.")
            flagged_warning = True
        elif(len(day["data"]) > NUM_BLOCKS_PER_DAY):
            raise ValueError("ERROR: recieved" + str(len(day["data"])) + 
                             " blocks per day. Aborting.")
        
        for block in day["data"]:
            num_blocks += 1
            
            # check that the integers are all within 16bit
            if(block >= INT_MAX):
                raise ValueError("ERROR: bad header (" + str(block) + "). Aborting.")
            
            # check that there are no duplicate blocks in each file
            if(block in seen):
                raise ValueError("ERROR: found duplicate block. Aborting.")
            else:
                seen.add(block)
        
        # check that the local index is within bounds
        local_index = (block & MASK_LINDEX) >> 8
        if(local_index < 0 or local_index >= NUM_BLOCKS_PER_FILE):
            raise ValueError("ERROR: local index of " + str(block) + " is " + 
                             str(local_index) + ". Aborting.")
    
    # check that the number of blocks on file is expected
    if(num_blocks < NUM_BLOCKS_PER_FILE and warnings):
        print("WARNING: recieved " + str(num_blocks) + " blocks per file.")
        flagged_warning = True
    elif(num_blocks > NUM_BLOCKS_PER_FILE):
        raise ValueError("ERROR: recieved" + str(num_blocks) + " blocks per file. Aborting.")
    
    if(not flagged_warning and verbose):
        print("PASSED: Blocks meets invariant requirements.")
            