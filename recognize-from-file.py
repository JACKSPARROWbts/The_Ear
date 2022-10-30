import os
import sys
import libs
import libs.fingerprint as fingerprint
import argparse
from libs.reader_file import FileReader
from argparse import RawTextHelpFormatter
from itertools import izip_longest
from termcolor import colored
from libs.config import get_config
from libs.reader_microphone import MicrophoneReader
from libs.visualiser_console import VisualiserConsole as visual_peak
from libs.visualiser_plot import VisualiserPlot as visual_plot
from libs.db_sqlite import SqliteDatabase


song = 'sample.mp3'
#seconds = 5

r = FileReader(song) # only get filename

#get data,fs,file_hash,extension,songname,num_channels
data = r.parse_audio()
Fs = data['Fs']
num_channel = len(data['channels'])

result = set()
matches = []
db = SqliteDatabase()
#channel_amount = len(data)

def grouper(iterable, n, fillvalue=None):
  args = [iter(iterable)] * n
  return (filter(None, values) for values
          in izip_longest(fillvalue=fillvalue, *args))

def find_matches(samples, Fs=fingerprint.DEFAULT_FS):
  hashes = fingerprint.fingerprint(samples, Fs=Fs)
  return return_matches(hashes)


def return_matches(hashes):
  mapper = {}
  for hash, offset in hashes:
    mapper[hash.upper()] = offset
  values = mapper.keys()

  for split_values in grouper(values, 1000):
    # @todo move to db related files
    query = """
      SELECT upper(hash), song_fk, offset
      FROM fingerprints
      WHERE upper(hash) IN (%s)
    """
    query = query % ', '.join('?' * len(split_values))

    x = db.executeAll(query, split_values)
    matches_found = len(x)

    if matches_found > 0:
      msg = '   ** found %d hash matches (step %d/%d)'
      print colored(msg, 'green') % (
        matches_found,
        len(split_values),
        len(values)
      )
    else:
      msg = '   ** not matches found (step %d/%d)'
      print colored(msg, 'red') % (
        len(split_values),
        len(values)
      )

    for hash, sid, offset in x:
      # (sid, db_offset - song_sampled_offset)
      yield (sid, offset - mapper[hash])


for channeln, channel in enumerate(data['channels']):
  # TODO: Remove prints or change them into optional logging.
  matches.extend(find_matches(channel))


def align_matches(matches):
  diff_counter = {}
  largest = 0
  largest_count = 0
  song_id = -1

  for tup in matches:
    sid, diff = tup

    if diff not in diff_counter:
      diff_counter[diff] = {}

    if sid not in diff_counter[diff]:
      diff_counter[diff][sid] = 0

    diff_counter[diff][sid] += 1

    if diff_counter[diff][sid] > largest_count:
      largest = diff
      largest_count = diff_counter[diff][sid]
      song_id = sid

  songM = db.get_song_by_id(song_id)

  nseconds = round(float(largest) / fingerprint.DEFAULT_FS *
                   fingerprint.DEFAULT_WINDOW_SIZE *
                   fingerprint.DEFAULT_OVERLAP_RATIO, 5)

  return {
    "SONG_ID": song_id,
    "SONG_NAME": songM[1],
    "CONFIDENCE": largest_count,
    "OFFSET": int(largest),
    "OFFSET_SECS": nseconds
  }


total_matches_found = len(matches)

print ''

if total_matches_found > 0:
  msg = ' ** totally found %d hash matches'
  print colored(msg, 'green') % total_matches_found

  song = align_matches(matches)

  msg = ' => song: %s (id=%d)\n'
  msg += '    offset: %d (%d secs)\n'
  msg += '    confidence: %d'

  print colored(msg, 'green') % (
    song['SONG_NAME'], song['SONG_ID'],
    song['OFFSET'], song['OFFSET_SECS'],
    song['CONFIDENCE']
  )
else:
  msg = ' ** not matches found at all'
  print colored(msg, 'red')
