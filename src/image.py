class ImageDownload():
    def __init__(self, url, path):
        self.url = url
        self.path = path

    def download(self):
        from urllib.request import urlretrieve
        from os.path import isfile

        if not isfile(self.path):
            urlretrieve(self.url, self.path)
            print("Downloaded image to {}".format(self.path))
        else:
            print("Image already exists at {}".format(self.path))


class Remove_image():
    def __init__(self, path):
        self.path = path

    def remove(self):
        from shutil import rmtree
        rmtree(self.path)
