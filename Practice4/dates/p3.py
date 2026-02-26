from datetime import datetime
now=datetime.now()
print(now)
no_microseconds=now.replace(microsecond=0)
print(no_microseconds)