import os, time, sys
import datetime
directory = r"app\static\qrcodes"
for filename in os.listdir(directory):
    if filename.endswith(".png"):
        path=directory+'\\'+filename
        time_file = os.path.getmtime(path)
        time_file_time=datetime.datetime.fromtimestamp(time_file)
        time_now=datetime.datetime.now()
        time_now_sec=datetime.datetime.now().second
        if (time_now.time()>time_file_time.time() or time_now.date() > time_file_time.date()) or (time_now_sec-time_file_time.second>=20):
            os.remove(path)

