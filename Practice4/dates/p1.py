from datetime import datetime,timedelta
today=datetime.now()
five_days_ago=today-timedelta(days=5)
print(today.date())
print(five_days_ago.date())