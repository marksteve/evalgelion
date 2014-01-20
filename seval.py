from seccomp import SecureEvalHost

from sys import argv


if __name__ == '__main__':
  sec = SecureEvalHost()
  sec.start_child()
  try:
    print sec.eval(' '.join(argv[1:]))
  finally:
    sec.kill_child()

