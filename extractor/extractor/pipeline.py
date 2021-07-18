import sys
sys.path.append("..")

import extractor.naive
import extractor.advanced
import spider.stable

def extract(bvid, src_type, clip_type):
    if src_type==0 and clip_type==0:
        extractor.naive.solve(bvid)
    else:
        print("Unsupported Type Parameters!")

def spider_info(bvid):
    spider.stable.solve(bvid)

    