from pyaib.plugins import keyword


@keyword('python')
def python(irc_c, msg, trigger, args, kwargs):
  try:
    msg.reply(msg.nick + ': ' + repr(eval(' '.join(args))))
  except Exception as e:
    msg.reply(repr(e))

