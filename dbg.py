from settings import MASK_WRITTEN

def dbg_files(file_arr):
    file_index = file_arr[0]["header"]
    print("============= FILE " + str(file_index) + " =============")
    for day in file_arr:
        not_written = 0
        for block in day["data"]:
            not_written += not (MASK_WRITTEN & block)
        print("total: " + str(len(day["data"])), "| written: " + str(len(day["data"])-not_written), "blank: " + str(not_written))

