import os
os.makedirs("test/folderA/folderB", exist_ok=True)
print("Содержимое текущей папки:")
for item in os.listdir("."):
    print(item)
print("\nTXT файлы:")
for file in os.listdir("."):
    if file.endswith(".txt"):
        print(file)