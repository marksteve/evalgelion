from __future__ import print_function

import socket

HOST = 'localhost'
PORT = 4240


def serve():
  print("Serving at {}:{}".format(HOST, PORT))
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind((HOST, PORT))
  server.listen(1)

  bot, addr = server.accept()
  while True:
    msg = bot.recv(2**20)
    try:
      try:
        lang, cmd = msg.split(' ', 1)
      except ValueError:
        continue
      else:
        if lang == 'python':
          out = cmd
    except Exception as e:
      out = str(e)
    bot.send(out)
  bot.close()


if __name__ == '__main__':
  serve()
