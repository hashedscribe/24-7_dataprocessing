from datetime import datetime, timedelta, timezone

# Create a naive datetime for April 11, 2021, 12:00 AM EDT
naive_datetime = datetime(2021, 4, 11, 0, 0, 0)
edt_offset = timezone(timedelta(hours=-4))
edt_time = naive_datetime.replace(tzinfo=edt_offset)

# Convert to UTC
utc_time = edt_time.astimezone(timezone.utc)

KERNEL_TIME = utc_time
NUM_BLOCKS_PER_DAY = 48