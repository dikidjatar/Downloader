# Coded By Dikidjatar
"""
Nothing To See Here...
https://dikidjatar.my.id
"""
import os, time, requests
from pytube import YouTube
from pydub import AudioSegment
import youtube_dl

from rich import print
from rich.panel import Panel
from rich.console import Console

class Downloader:
   def __init__(self):
      self.save_path = '/sdcard/Download'
      self.video_path = '.vidlog'
   
   def download_video_youtube(self, url):
      try:
         print("[bold italic yellow]Memproses link...", end="\r")
         youtube_video = YouTube(url)
         available_resolutions = [stream.resolution for stream in youtube_video.streams.filter(file_extension="mp4")]
         video_title = youtube_video.title
         print(Panel(f"[bold green italic]{video_title}"))
         print("Resolusi video yang tersedia:")
         for i, resolution in enumerate(available_resolutions, start=1):
            print(f"{i}. {resolution}")
         choice = int(input("Masukan pilihan resolusi video: "))
         selected_resolution = available_resolutions[choice - 1]
         video_stream = youtube_video.streams.filter(file_extension="mp4", resolution=selected_resolution).first()
         print(f"[bold red]Downloading => [green italic]{video_title}", end="\r")
         video_stream.download(self.save_path)
         print(Panel(f"[bold green]Video '{video_title}.mp4' dengan resolusi [italic yellow]{selected_resolution}[/italic yellow] berhasil diunduh.", width=65))
      except Exception as e:
         print(Panel("[bold red]Gagal download video", e, width=65))
         
   def download_audio_youtube(self, url):
      try:
         print("[bold italic yellow]Memproses link...", end="\r")
         youtube_video = YouTube(url)
         audio_stream = youtube_video.streams.filter(only_audio=True).first()
         video_title = youtube_video.title
         print(f"[bold red]Downloading => [green italic]{video_title}", end="\r")
         audio_stream.download(self.video_path)
         title = os.listdir(self.video_path)
         for t in title:
            title = os.path.splitext(t)[0]
         self.convert_to_mp3(title)
      except Exception as e:
         print(Panel("[bold red italic]Gagal download musik", str(e)))
         
   def download_video_facebook(self, url):
      ydl_opts = {
         'format': 'bestvideo+bestaudio/best',
         'outtmpl': f'{self.save_path}/%(title)s.%(ext)s',
      }
      with youtube_dl.YoutubeDL(ydl_opts) as ydl:
         ydl.download([url])
   
   def convert_to_mp3(self, video_title):
      try:
         print("[bold italic yellow]=> Mengkonversi ke mp3...", end="\r")
         video = AudioSegment.from_file(self.video_path + '/' + video_title + '.mp4', format="mp4")
         audio = video.set_channels(1)
         audio.export(self.save_path + '/' + video_title + '.mp3', format="mp3")
         print(Panel(f"[bold green]Audio '{video_title}.mp3' Berhasil diunduh'"))
         os.system(f"rm {self.video_path}/*.mp4")
      except Exception as e:
         print(Panel("[bold red italic]Terjadi kesalahan saat mengkonversi ke mp3", str(e)))
         
def clear_screen():
   os.system('cls' if os.name == 'nt' else 'clear')
   
def banner():
   clear_screen()
   print('''
[bold white italic]Created By Dikidjatar | [blue] https://github.com/dikidjatar[/bold white italic]
[bold cyan] _____                    _                 _             
(____ \                  | |               | |            
 _   \ \ ___  _ _ _ ____ | | ___   ____  _ | | ____  ____ 
| |   | / _ \| | | |  _ \| |/ _ \ / _  |/ || |/ _  )/ ___)
| |__/ / |_| | | | | | | | | |_| ( ( | ( (_| ( (/ /| |    
[red]|_____/ \___/ \____|_| |_|_|\___/ \_||_|\____|\____)_|  
''')

def check_folder():
   if os.path.exists(".vidlog") == False:
      os.mkdir(".vidlog")
      
def main():
   banner()
   check_folder()
   try:
      downloader = Downloader()
      print("(00) Logout")
      print("(01) Download Video YouTube")
      print("(02) Download Musik MP3 YouTube")
      print("(03) Download Video Facebook");print("")
      chooice = input("Masukan pilihan (1/2/3): ")
      
      if chooice in ["0", "00"]:logout()
      elif chooice in ["1", "01"]:
         url = input("Masukan URL video YouTube: ")
         downloader.download_video_youtube(url)
      elif chooice in ["2", "02"]:
         url = input("Masukan URL video YouTube: ")
         downloader.download_audio_youtube(url)
      elif chooice in ["3", "03"]:
         print(Panel("[bold green]Masukan URL Video Facebook Anda. [italic yellow]Pastikan Videonya Harus Pubilk.", style="bold white", width=65, subtitle="[bold white]╭─────", subtitle_align="left"))
         url = Console().input("[bold white]   ╰─> ")
         downloader.download_video_facebook(url)
      else:
         print(Panel("[bold red italic]Pilihan anda salah!", width=65));time.sleep(3);main()
   except KeyboardInterrupt as e:
      print("Good By!")
   
def logout():
   print("Berhasil logout...")
   os.system("xdg-open https://www.facebook.com/dikijatar")
   
if __name__ == "__main__":
   main()