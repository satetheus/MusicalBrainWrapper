"""
12-22-2018 Lord Vorian

Take inputs from signaler.py and use it to play songs from vibe_parser.py
"""
############################## Imports ########################################
import csv, signaler, vlc
from time import time, sleep
from random import random, choice
from os import path
from  vibe_parser import WORKING_DIR




############################### Get Filenames #################################





cleaned_list = []

with open(path.join(WORKING_DIR,'tempo_list.csv'), 'r') as unread_file:
  read_file = csv.reader(unread_file)
  for i in read_file:
    if len(i) > 1:  # ignore blank lines
      if float(i[1]) > 120:  # only fast music!
        cleaned_list.append(i)

cleaned_list = sorted(cleaned_list, key=lambda i: float(i[1]), reverse=True)


############################# Set Up timer & listen to signaler ###############

def fadeIn(player, seconds):
  """
  Fade in the song in 1% increments
  :param player: VLC Instance media_player_new
  :param seconds: Time to fade over
  :return: Nothing
  """
  seconds = float(seconds)
  step = seconds / 100
  player.audio_set_volume(0)
  # player.set_position(0.5)
  player.play()
  while seconds > 0:
    player.audio_set_volume(100 - int(seconds/step))
    seconds -= step
    sleep(step)

def fadeOut(player, seconds):
  """
  Fade in the song in 1% increments
  :param player: VLC Instance media_player_new
  :param seconds: Time to fade over
  :return: Nothing
  """
  seconds = float(seconds)
  step = seconds / 100
  while seconds > 0:
    player.audio_set_volume(int(seconds/step))
    seconds -= step
    sleep(step)
  player.stop()



def test(player):
  elapsed = 0
  invasions = 0
  invading = 0
  while True:
    # TODO loop chill bpm
    if not int(time()) % 5:

      if signaler.invader_detect() and invading <= 0:
        player.set_media(instance.media_new(choice(cleaned_list)[0]))
        fadeIn(player, 2)
        print('New invasion # {}'.format(invasions))
        invasions += 1
        invading = 2

      elif signaler.invader_detect() and invading > 0:
        invading = 2


      elif invading > 0 and not player.is_playing():
        player.set_media(instance.media_new(choice(cleaned_list)[0]))
        fadeIn(player, 1)


      
      elif not signaler.invader_detect():
        invading -= 1

      if invading <= 0 and player.is_playing():
        fadeOut(player, 5)
    sleep(1)


if __name__ == "__main__":
  instance = vlc.Instance()
  player = instance.media_player_new()
  sleep(15)
  test(player)