import time


def log(string):
    t = time.strftime(r"%Y-%m-%d-%H:%M:%S", time.localtime())
    print("[%s]%s" % (t, string))