from datetime import datetime, timedelta, timezone

# ------------------------------- PREPROCESSING ------------------------------ #
naive_datetime = datetime(2021, 4, 11, 0, 0, 0)
edt_offset = timezone(timedelta(hours=-4))
edt_time = naive_datetime.replace(tzinfo=edt_offset)

utc_time = edt_time.astimezone(timezone.utc)

# --------------------------------- DATETIME --------------------------------- #
DATETIME_FORMAT = "%Y-%m-%d"
KERNEL_TIME = utc_time

# ------------------------------- ARCHITECTURE ------------------------------- #
NUM_BLOCKS_PER_DAY = 48
NUM_DAYS_PER_FILE = 5
NUM_BLOCKS_PER_FILE = NUM_BLOCKS_PER_DAY * NUM_DAYS_PER_FILE

INTEGER_SIZE = 16
INT_MAX = 2 << INTEGER_SIZE

# ----------------------------------- MASKS ---------------------------------- #
MASK_WRITTEN = 0x01
MASK_NOTE = 0x02
MASK_CATEGORY = 0xFC
MASK_LINDEX = ~0xFF

# ----------------------------------- FILE ----------------------------------- #
FILE_NAME = "247_logs_"