import requests
from bs4 import BeautifulSoup
from pprint import pprint
import ast
from downloader import SongsDownloader
from config import *


def get_track_params(response):

    audio_response = response[response.find("shHash")+9:]
    shHash = audio_response[:audio_response.find(",")-1]
    audio_response = response[response.find("shObj")+8:]
    shObj = audio_response[:audio_response.find(",")-1]
    return shObj, shHash




s = requests.Session()

#auth
login_response = s.get("https://vk.com").text
login_response = login_response[login_response.find('"POST"'):]
login_response = login_response[login_response.find('action="')+8:]
auth_link = login_response[:login_response.find('"')]
s.post(auth_link,params = {"email":LOGIN,"pass":PASSWORD})

while True:
    number = int(input("Track: "))
    audio_id = str(456239000 + number)
    audio = user_id + "_" + audio_id

    #post audio
    response = s.get(f"https://vk.com/like.php?act=publish_box&al=1&object=audio{audio}&to=mail").text
    shObj, shHash = get_track_params(response)
    
    response = s.post(f"https://vk.com/like.php?Message=https://vk.com/id{user_id} {user_id}:{number}"
                       "&act=a_do_publish&al=1&close_comments=0&friends_only=0&from=box&hash={shHash}"
                       "&mark_as_ads=0&mute_notifications=0&object={shObj}&ret_data=1&to=-{GROUP_ID}").text

    if "Запись отправлена" in response:

        print("Пост отправлен")
        group_page = s.get(f"https://vk.com/public{GROUP_ID}").content
        soup = BeautifulSoup(group_page, 'html.parser')

        author = soup.findAll("span", {"class": "medias_music_author"})
        title = soup.findAll("span", {"class": "medias_audio_title"})
        duration = ("span", {"class": "medias_audio_dur"})
        
        name = f"{author[0].text}{title[0].text}"
        time = name[-6::]
        revoke_time = name.replace(time, '')

        sd = SongsDownloader(revoke_time)
        songs_list = sd.get_songs_list()
        print(songs_list)

    elif '["2",' in response:
        print("Ошибка: Капча")

    else:
        print("Неопознанная ошибка (Проверьте id группы и логин с паролем)")
