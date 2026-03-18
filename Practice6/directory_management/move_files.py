import shutil
import os
os.makedirs("test", exist_ok=True)
with open("example.txt", "w") as f:
    f.write("Hello")
shutil.move("example.txt", "test/example.txt")
shutil.copy("test/example.txt", "test/copy.txt")
print("Файл перемещён и скопирован")