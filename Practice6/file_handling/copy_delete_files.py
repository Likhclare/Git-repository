import shutil
import os
shutil.copy("sample.txt", "backup.txt")
if os.path.exists("sample.txt"):
    os.remove("sample.txt")