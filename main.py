from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from youtubesearchpython import VideosSearch
import yt_dlp
import os

class MusicDownloaderApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Input for Singer's Name
        self.singer_input = TextInput(hint_text='Enter singer\'s name', multiline=False)
        self.layout.add_widget(self.singer_input)

        # Input for Song Name
        self.song_input = TextInput(hint_text='Enter song name', multiline=False)
        self.layout.add_widget(self.song_input)

        # Dropdown/Spinner to choose Audio or Video
        self.download_type_spinner = Spinner(
            text='Choose Download Type',
            values=('Audio', 'Video'),
            size_hint=(1, 0.3)
        )
        self.layout.add_widget(self.download_type_spinner)

        # Download Button
        self.download_button = Button(text='Download Song')
        self.download_button.bind(on_press=self.download_song)
        self.layout.add_widget(self.download_button)

        # Status Label to show progress and feedback
        self.status_label = Label(text='')
        self.layout.add_widget(self.status_label)

        return self.layout

    def download_song(self, instance):
        singer_name = self.singer_input.text.strip()
        song_name = self.song_input.text.strip()
        download_type = self.download_type_spinner.text

        full_query = f"{song_name} {singer_name}"

        # Inform the user we are searching for the song
        self.status_label.text = f"Searching for '{full_query}'..."
        songs = search_songs(full_query, limit=1)

        if songs:
            song = songs[0]
            video_url = song['link']
            self.status_label.text = f"Downloading {song['title']} as {download_type}..."

            # Decide to download either audio or video based on user choice
            if download_type == 'Audio':
                download_audio(video_url)
            elif download_type == 'Video':
                download_video(video_url)

            self.status_label.text = f"Downloaded: {song['title']}.{download_type.lower()}"
        else:
            self.status_label.text = f"No results found for '{full_query}'."

        # Clear input fields for the next song
        self.singer_input.text = ""
        self.song_input.text = ""

        # Prompt the user for another song
        self.status_label.text += "\nYou can enter another song."

# Search function to query YouTube for songs
def search_songs(query, limit=1):
    search = VideosSearch(query, limit=limit)
    return search.result()['result']

# Function to download audio using yt-dlp
def download_audio(video_url, output_path="downloads/"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
    }

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

# Function to download video using yt-dlp
def download_video(video_url, output_path="downloads/"):
    ydl_opts = {
        'format': 'bestvideo+bestaudio',  # Download both video and audio
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
    }

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

if __name__ == '__main__':
    MusicDownloaderApp().run()
