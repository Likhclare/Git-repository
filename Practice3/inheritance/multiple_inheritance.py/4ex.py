class Camera:
    def take_photo(self):
        print("Photo taken")

class Phone:
    def call(self):
        print("Calling")

class Smartphone(Camera, Phone):
    pass

sp = Smartphone()
sp.take_photo()
sp.call()
