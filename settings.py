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
NUM_BLOCKS_PER_FILE = 256
NUM_DAYS_PER_FILE = NUM_BLOCKS_PER_FILE // NUM_BLOCKS_PER_DAY

# ----------------------------------- MASKS ---------------------------------- #
MASK_WRITTEN = 0x01
MASK_NOTE = 0x02
MASK_CATEGORY = 0xFC
MASK_LINDEX = ~0xFF