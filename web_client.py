import requests


class WebClient(object):
    def download(self, url, file_path):
        response = requests.get(url)
        with open(file_path, "wb") as local_file:
            local_file.write(response.content)
