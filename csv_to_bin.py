import os, sys

# DATETIMES
from datetime import datetime, timedelta, timezone
from settings import DATETIME_FORMAT, KERNEL_TIME

# ARCHITECTURE
from settings import NUM_BLOCKS_PER_DAY, NUM_BLOCKS_PER_FILE

# MASKS
from settings import MASK_WRITTEN, MASK_NOTE, MASK_CATEGORY, MASK_LINDEX

def split_to_array(file, delim = "\n"):
    return [line.split(delim) for line in file]

def parse_legend(legend_file):
    legend_arr = split_to_array(legend_file)
    i = 0
    legend = {}
    for entry in legend_arr:
        legend[entry[0]] = i
        i += 1
    return legend

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

def day_to_entries(day_string, legend_dict):
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

def main():
    input_file_name = input()
    legend_file_name = input()
    
    read_file = open(os.path.join(sys.path[0], "./tests/" + input_file_name + ".csv"))
    legend_file = open(os.path.join(sys.path[0], "./legends/" + legend_file_name + ".txt"))
    output_binary = open(os.path.join(sys.path[0], "./output/binarytest.bin"), "wb")
    
    output_binary.write(b'\x21')
    lines = split_to_array(read_file)
    legend_dict = parse_legend(legend_file)
    
    day_to_entries(lines[0][0], legend_dict)
    

if __name__ == "__main__":
    main()