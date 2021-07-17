import sys
sys.path.append("..")

import extractor.naive

def extract(bvid, src_type, clip_type):
    if src_type==0 and clip_type==0:
        extractor.naive.solve(bvid)
    else:
        print("Unsupported Type Parameters!")