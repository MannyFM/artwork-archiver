import json
import urllib.request

import os

global working_dir


def dump_file(item):
    filename = "{}-{}.jpeg".format(item[0], item[1])
    filename = filename.replace(" ", "_")
    filename = filename.replace("/", "_")
    filename = filename.replace("\\", "_")
    filename = working_dir + "/" + filename
    urllib.request.urlretrieve(item[2], filename)


def main():
    with open('dump.json') as json_data_file:
        data = json.load(json_data_file)

    if not os.path.exists(working_dir):
        os.makedirs(working_dir)

    size = len(data)
    for i, item in enumerate(data):
        print("\rDownloading {}/{}".format(i, size), end="")
        dump_file(item)
    print("\nYeah")


if __name__ == '__main__':
    print("Script is started")
    working_dir = "output"
    main()
    print("Script ended")
