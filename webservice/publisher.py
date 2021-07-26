from posix import times_result
import common
import spider
import os
from common import sqlQuery
import time
from threading import Thread


def publish(ovid):
    print("publish",ovid)
    # xxx.run()