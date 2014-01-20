import subprocess

from pyaib.plugins import keyword

from util import error


def sec_eval(cmd):
  return subprocess.check_output(['python', 'python/sec_eval.py', cmd])


@keyword('python')
def python(irc_c, msg, trigger, args, kwargs):
  try:
    msg.reply(msg.nick + ': ' + sec_eval(' '.join(args)))
  except:
    msg.reply(msg.nick + ': ' + error())

