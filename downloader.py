import requests
import time
import urllib3

urllib3.disable_warnings()


class SongsDownloader:

    def __init__(self, song_name="Pass", r=requests.Session()):

        self.song_name = song_name
        self.r = r
        print(self.song_name)
        
    def get_songs_list(self):

        headers = {
            'user-agent':
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}

        params = {'search': self.song_name, 'time': time.ctime()}

        self.response = self.r.get(
            "https://vk.music7s.cc/api/search.php?", headers=headers, params=params, verify=False)

        if self.response.status_code == 200:
            urls_list = []
            i = 1
            try:
                for item in self.response.json()['items']:
                    urls_list.append(f"{item['url']}")
            
                self.link = urls_list[0]
                headers = {
                    'user-agent':
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
                
                url = f"https://vk.music7s.cc{self.link}"
                self.response = self.r.get(url, headers=headers, verify=False)

                with open(f'./music/{self.song_name}.mp3', 'wb') as write_song:
                    write_song.write(self.response.content)
                
                return [url, "Song in directory"]
            except KeyError:
                return "Песня не найдена"
        else:
            return False
            