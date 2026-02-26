from datetime import datetime
date_str1=input()
date_str2=input()
date1=datetime.strptime(date_str1,"%Y-%m-%d %H:%M:%S")
date2=datetime.strptime(date_str2,"%Y-%m-%d %H:%M:%S")
diff=date2-date1
seconds=diff.total_seconds()
print(seconds)