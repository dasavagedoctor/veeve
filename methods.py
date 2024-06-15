from pytube import YouTube, Playlist
from colorama import Fore, Style
import os
import subprocess




# Get the user's home directory
user_home = os.path.expanduser("~")

# Define the path to the Downloads folder
download_path = os.path.join(user_home, "Downloads")


#-------------------------------------------------


# convert video files to mp3
def convert_to_mp3(file_path):
    mp3_file_path = file_path[:-4] + ".mp3"  
    subprocess.run(['ffmpeg', '-i', file_path, '-vn', '-acodec', 'libmp3lame', '-q:a', '2', mp3_file_path])
    return mp3_file_path


#-------------------------------------------------


# display the menu
def menu():
    while True:
        print('''
----------------------
1. Download video
2. Download playlist
3. Quit
----------------------      
              ''')
        print(Fore.CYAN + "Enter your choice: " + Style.RESET_ALL, end="")
        choice = int(input())
        if choice == 1:
            video()

        if choice == 2:
            playlist()

        if choice == 3:
            break


#-------------------------------------------------
        

# get url and return an object of class Youtube
def get_url(type):
    
    if type == 'video':
        while True:
            url = input(Fore.CYAN + "\nEnter the url for your video: " + Style.RESET_ALL)
            try:
                yt = YouTube(url)
                break
            except:
                print(Fore.RED + f"\nInvalid url!" + Style.RESET_ALL)
        
        return yt
    
    if type == 'playlist':
        while True:
            url = input(Fore.CYAN + "\nEnter the url for your playlist: " + Style.RESET_ALL)
            try:
                playlist = Playlist(url)
                break
            except:
                print(f"\nInvalid url!")
        
        return playlist


#-------------------------------------------------
    

#displays video information 
def info(yt):
    title = yt.title
    print(Fore.GREEN + f"\nTitle: {title} \n" + Style.RESET_ALL)
    

#-------------------------------------------------
    

#display available download resolutions and get desired resolution
def get_res(yt):
    streams = yt.streams.filter(file_extension='mp4')
    resolutions = [stream.resolution for stream in streams]

    # append available resolutions to res as integers
    res = []
    for i,resolution in enumerate(resolutions):
        if resolution == None:
            continue
        else:
            res.append(int(resolution[:-1]))

    # remove duplicate values from the list res
    res = list(set(res))

    #sort the available resolutions in ascending order
    res.sort()
    for i in range(len(res)):
        res[i] = str(res[i]) + 'p'
    
    #print out the available download resolutions
    print(Fore.GREEN + "Available resolutions: " + str(res) + Style.RESET_ALL)

    #allows the user to enter their desired download resolution
    desired_res = None
    desired_res = input(Fore.CYAN + "Enter your desired resolution: " + Style.RESET_ALL).strip()
    while desired_res not in res:
        desired_res = input(Fore.RED + "Please enter a valid argument: " + Style.RESET_ALL).strip()

    # returns the desired resolution 
    return desired_res

#-------------------------------------------------


#downloads the video at the set resolution
def download_video(yt, res, output_path):
    stream = yt.streams.get_by_resolution(resolution=res)
    try:
        file_path = stream.download(output_path=output_path)
        print(Fore.LIGHTYELLOW_EX + f"\n{yt.title} has been successfully downloaded!" + Style.RESET_ALL)

        convert_choice = input(Fore.CYAN + "\nDo you want to convert the downloaded file to mp3? (yes/no): " + Style.RESET_ALL)
        if convert_choice.lower() == 'yes':
            mp3_file_path = convert_to_mp3(file_path)
            print(Fore.LIGHTYELLOW_EX + f"\n{file_path} has been converted to {mp3_file_path}" + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + "The selected resolution seems to be unavailable, choose a lower resolution!" + Style.RESET_ALL)
    

#-------------------------------------------------
        

#downloads a video 
def video():

    #create Youtube object
    yt = get_url(type='video')

    #displays url information
    info(yt)


    #get all the available resolutions
    resolution = get_res(yt)

    download_video(yt, resolution, download_path)


#-------------------------------------------------
    

#downloads a playlist of videos
def playlist():
    playlist_obj = get_url(type='playlist')
    output_path = os.path.join(download_path, "Playlists", playlist_obj.title)
    convert_choice = input(Fore.CYAN + "\nDo you want to convert all downloaded files to mp3? (y/n): " + Style.RESET_ALL)

    downloaded_files = []
    for video in playlist_obj.videos:
        try:
            stream = video.streams.get_highest_resolution()
            file_path = stream.download(output_path=output_path)
            downloaded_files.append(file_path)
            print(Fore.LIGHTYELLOW_EX + f"\n{video.title} has been successfully downloaded!" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"An error occurred while downloading '{video.title}': {str(e)}" + Style.RESET_ALL)

    if convert_choice.lower() == 'y':
        for file_path in downloaded_files:
            mp3_file_path = convert_to_mp3(file_path)
            print(Fore.LIGHTYELLOW_EX + f"\n{file_path} has been converted to {mp3_file_path}" + Style.RESET_ALL)


#-------------------------------------------------

def veeve():
    print(Fore.GREEN + '''
⠀⠀⠀⢠⣾⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣰⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢰⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣄⣀⣀⣤⣤⣶⣾⣿⣿⣿⡷
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀
⣿⣿⣿⡇⠀⡾⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀
⣿⣿⣿⣧⡀⠁⣀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠉⢹⠉⠙⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀            veeve allows you to download youtube videos and playlists
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣀⠀⣀⣼⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀            using a command line program
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀            
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀             Be nice to veeve   
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠀⠤⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⠿⠋⢃⠈⠢⡁⠒⠄⡀⠈⠁⠀⠀⠀⠀⠀⠀⠀
⣿⣿⠟⠁⠀⠀⠈⠉⠉⠁⠀⠀⠀⠀⠈⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠀⠀⠀⠀⠀⠀⠀⠀''' + Style.RESET_ALL)




