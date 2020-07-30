
import os
import googleapiclient.discovery
from pytube import YouTube
import subprocess
import config

class YouTubeHelper():
    
    def __init__(self):
        self.youtube_api = self.get_youtube_build()
        self.destination_folder = 'D:/Videos'
        
    def get_youtube_build(self):
        # Get the developer key from config.py
        developer_key = config.api_key
        api_service_name = "youtube"
        api_version = "v3"
        yt_build = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey = developer_key)
        return yt_build
    
    def download_single_video(self, video_id, filename='testFile', resolution='720p'):
        video = YouTube("https://www.youtube.com/watch?v={}".format(video_id))
        video_streams = video.streams.filter(file_extension = "mp4", res=resolution)
        if len(video_streams) == 0:
            video_stream = video.streams.filter(progressive=True).get_highest_resolution()
        else:
            video_stream = video_streams.first()

        if not video_stream.includes_audio_track:
            audio_stream = video.streams.filter(only_audio=True, file_extension='mp4').first()
            audio_stream.download(filename='audio', output_path=self.destination_folder)
            video_stream.download(filename='video', output_path=self.destination_folder)
            subprocess_command = 'ffmpeg -i "' + self.destination_folder + '/video.mp4" -i "' + self.destination_folder + '/audio.mp4" -c copy "' + destination_folder + '/' + filename + '.mp4"'
            print(subprocess_command)
            subprocess.run(subprocess_command, shell=True)
            os.remove(self.destination_folder+'/video.mp4')
            os.remove(self.destination_folder+'/audio.mp4')
        else:
            video_stream.download(filename=filename, output_path=self.destination_folder)
            
    def download_single_video_from_name(self, video_name, subscriber_name, filename='testFile', resolution='720p'):

        video_id = self.get_single_video_id(video_name, subscriber_name)
        if video_id is not None:
            self.download_single_video(video_id, filename=filename, resolution=resolution)

    def get_single_video_id(self, video_name, subscriber_name):
        channel_id = self.get_channel_id(channel_name=subscriber_name)

        request = self.youtube_api.search().list(
            part='snippet',
            maxResults=25,
            channelId=channel_id,
            q=video_name
        )
        response = request.execute()

        try:
            video_id = response['items'][0]['id']['videoId']
        except KeyError:
            return None
        return video_id
    
    def get_channel_id(self, channel_name):
        
        request = self.youtube_api.channels().list(
            part="snippet,contentDetails,statistics",
            forUsername=channel_name
        )
        response = request.execute()

        try:
            channel_id = response['items'][0]['id']
        except KeyError:
            return None

        return channel_id


    def get_playlist_id(self, playlist_name, channel_id):
        next_page_token = None
        searching_for_playlist = True

        while searching_for_playlist:
            request = self.youtube_api.playlists().list(
                part="snippet,contentDetails",
                channelId=channel_id,
                maxResults=50,
                pageToken = next_page_token
            )
            playlists = request.execute()

            playlist_ids = [pi['id'] for pi in playlists['items'] if pi['snippet']['title'] == playlist_name]
            if len(playlist_ids) == 0:
                try:
                    next_page_token = playlists['nextPageToken']
                except KeyError:
                    searching_for_playlist = False
            else:
                searching_for_playlist = False

        if len(playlist_ids) > 0:
            return playlist_ids[0]
        else:
            return None

    def get_video_ids(self, playlist_id):
        
        next_page_token = None
        searching_for_videos = True
        videos = []

        while searching_for_videos:
            request = self.youtube_api.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
            playlist_items = request.execute()

            videos += [(item['snippet']['title'], item['snippet']['resourceId']['videoId']) for item in playlist_items['items']]
            try:
                next_page_token = playlist_items['nextPageToken']
            except KeyError:
                searching_for_videos = False

        return videos
    
    def set_directory_name(self, directory_name):
        self.directory_name = directory_name
    
    def download_videos(videos, playlist_name, is_new_directory=False, 
                       resolution='720p', numeric_naming=True, naming_stub=None):
        if is_new_directory:
            if self.directory_name is None:
                self.directory_name = playlist_name.replace('.', '_')
            try:
                os.mkdir(self.directory_name)
            except FileExistsError:
                pass

        i = 0

        for title, video_id in videos:
            i += 1
            if numeric_naming:
                if naming_stub is not None:
                    title = str(i) + '_' + naming_stub
                else:
                    title = str(i) + '_' + title

            download_single_video(video_id, filename=title, resolution=resolution)
