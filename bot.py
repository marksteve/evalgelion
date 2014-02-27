#!/bin/python

from __future__ import print_function

import fileinput
import os
import re
import shutil
import socket
import subprocess
import sys
import time
from multiprocessing import Process

NICK = 'evalgelion2'
IRC_DIR = './irc'
LINE_PAT = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2} <(.+?)> (.+?): (.+)")
CONTAINER_HOST = 'localhost'
CONTAINER_PORT = 4240


def ii(server):
  subprocess.call([
    './ii/ii',
    '-i', IRC_DIR,
    '-s', server,
    '-n', NICK,
  ])
  return


def bot(server, channel):
  # shutil.rmtree(IRC_DIR)

  channel_path = '{irc_dir}/{server}/#{channel}/'.format(
    irc_dir=IRC_DIR,
    server=server,
    channel=channel,
  )

  while not os.path.exists(channel_path + 'out'):
    time.sleep(0.1)
  print("{} joined #{}".format(NICK, channel))

  container = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  container.connect((CONTAINER_HOST, CONTAINER_PORT))

  with open(channel_path + 'out') as channel_out:
    channel_out.seek(0, 2)
    while True:
      line = channel_out.readline()
      if not line:
        time.sleep(0.1)
        continue
      match = LINE_PAT.match(line)
      if match:
        from_nick, to_nick, msg = match.groups()
        if to_nick == NICK:
          with open(channel_path + 'in', 'w') as channel_in:
            container.send(msg)
            out = container.recv(2**20)
            channel_in.write("{from_nick}: {out}\n".format(
              from_nick=from_nick,
              out=out,
            ))


def main():
  try:
    server, channel = sys.argv[1:3]
  except IndexError:
    print("Usage: {} server channel".format(sys.argv[0]))
    return

  # Start ii
  ii_proc = Process(target=ii, args=(server,))
  ii_proc.start()

  # Join channels
  print("{} is joining #{}".format(NICK, channel))
  server_in = '{irc_dir}/{server}/in'.format(
    irc_dir=IRC_DIR,
    server=server,
  )
  while not os.path.exists(server_in):
    time.sleep(0.1)
  subprocess.call(
    'echo "/j #{channel}" > {server_in}'.format(
      channel=channel,
      server_in=server_in,
    ),
    shell=True,
  )

  # Start bot
  bot_proc = Process(target=bot, args=(server, channel))
  bot_proc.start()

  bot_proc.join()
  ii_proc.join()


if __name__ == '__main__':
  main()

