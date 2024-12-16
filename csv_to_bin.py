# ---------------------------------- IMPORTS --------------------------------- #
import os, sys

# DATETIMES
from datetime import datetime, timedelta, timezone
from settings import DATETIME_FORMAT, KERNEL_TIME

# ARCHITECTURE
from settings import NUM_BLOCKS_PER_DAY, NUM_BLOCKS_PER_FILE, NUM_DAYS_PER_FILE

# MASKS
from settings import MASK_WRITTEN, MASK_NOTE, MASK_CATEGORY, MASK_LINDEX

# FILE
from settings import FILE_HEADER

# VALIDATORS 
from validate import check_file_arr

# ----------------------------- GLOBAL VARIABLES ----------------------------- #
legend_dict = {}

# --------------------------------- FUNCTIONS -------------------------------- #

# converts the file given to an array where each line in the file is an array 
# entry
def file_to_array(file):
    array = []
    for line in file:
        array.append(line.strip())
    return array

# takes in a legend file returns an array with each element in the legend as an
# array entry
def parse_legend(legend_file):
    legend_arr = file_to_array(legend_file)
    i = 0
    legend = {}
    for entry in legend_arr:
        legend[entry.strip()] = i
        i += 1
    return legend

# TODO needs some refining to be more modular
def esdt_to_utc(naive_dt, is_daylight_savings = False):
    time_offset = timezone(timedelta(hours=-5))
    if(is_daylight_savings):
        time_offset = timezone(timedelta(hours=-4))
    with_timezone = naive_dt.replace(tzinfo=time_offset)
    return with_timezone.astimezone(timezone.utc)

def get_raw_index(day_string):
    # TODO find a way to check if a time is in daylight savings
    curr_day = esdt_to_utc(datetime.strptime(day_string, DATETIME_FORMAT), True)
    day_delta = (curr_day - KERNEL_TIME).days
    return day_delta * NUM_BLOCKS_PER_DAY

def get_file_index(raw_index):
    return raw_index // NUM_BLOCKS_PER_FILE

def get_local_index(raw_index):
    return raw_index % NUM_BLOCKS_PER_FILE

def day_to_entries(day_string):
    global legend_dict
    day_array = day_string.split(",")
    
    raw_index = get_raw_index(day_array[0])
    file_index = get_file_index(raw_index)
    local_index = get_local_index(raw_index)
    
    processed_data = {"header": file_index, "data": []}
    
    for entry in day_array[1:]:
        is_written = True
        has_note = False
        category = legend_dict[entry]
        
        processed_data["data"].append(local_index << 8 | category << 2 | has_note << 1 | is_written)
        local_index += 1
    return processed_data

def collect_to_file_size(lines):
    global legend_dict
    
    file_arr = []
    for line in lines:
        file_arr.append(day_to_entries(line))

    check_file_arr(file_arr, warnings = False, verbose = False)
    return(file_arr)

def write_bin(file_arr):
    # since all the header indices are the same, this shouldn't be an issue
    print("===========================")
    for line in file_arr:
        print(line)
    file_index = file_arr[0]["header"]
    
    filename = FILE_HEADER + f"{file_index:04d}"
    output_binary = open(os.path.join(sys.path[0], "./output/binarytest.bin"), "wb")

def main():
    global legend_dict
    input_file_name = input("test file name: ")
    legend_file_name = input("legend file name: ")
    
    read_file = open(os.path.join(sys.path[0], "./tests/" + input_file_name + ".csv"))
    legend_file = open(os.path.join(sys.path[0], "./legends/" + legend_file_name + ".txt"))
    
    lines = file_to_array(read_file)
    legend_dict = parse_legend(legend_file)
    
    file_arrays = []
    i = 0
    while i < len(lines):
        file_arrays.append(collect_to_file_size(lines[i:i+5]))
        i += 5
    
    for file_arr in file_arrays:
        write_bin(file_arr)
    

if __name__ == "__main__":
    main()