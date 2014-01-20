import subprocess

from pyaib.plugins import keyword

from util import error


def seval(cmd):
  return subprocess.check_output(['python', 'seval.py', cmd])


@keyword('python')
def python(irc_c, msg, trigger, args, kwargs):
  try:
    msg.reply(msg.nick + ': ' + seval(' '.join(args)))
  except:
    msg.reply(msg.nick + ': ' + error())

