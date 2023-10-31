import pypresence
import time
import json
import subprocess
import platform
import shutil


# the locator returns a tuple (lat, long) in decimal degrees
def platformLocator():

    def macOS():
        return tuple(
            json.loads(
                subprocess.check_output(['get-location', '-f', 'json'
                                         ]).decode('utf-8'))['coordinates'])

    os = platform.system()
    if os == "Darwin":
        if shutil.which("get-location") is not None:
            return macOS
        else:
            print(
                "Please install get-location from\nhttps://github.com/lindes/get-location"
            )
            exit(1)
    else:
        print(f'{os} is not supported')
        exit(1)


def updateLocation(RPC, locator):
    lat, long = locator()
    print(f'current location: {lat}, {long}')
    RPC.update(state=f'at: {lat}, {long}',
               buttons=[{
                   "label":
                   "open map",
                   "url":
                   f'https://www.google.com/maps/place/{lat},{long}'
               }])


def main():
    locator = platformLocator()
    print("platform locator OK")
    # for the name "hide and seek", you can use your own
    clientID = "1169009519876132985"
    RPC = pypresence.Presence(clientID)
    RPC.connect()
    print("connected to discord")
    print("getting location...")
    while True:
        updateLocation(RPC, locator)
        time.sleep(15)


if __name__ == "__main__":
    main()
