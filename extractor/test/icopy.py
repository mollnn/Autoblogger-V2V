import sys
sys.path.append("..")

import extractor.pipeline


bvid="BV1E5411j75F"
filename="D:/1.mp4"
extractor.pipeline.importMedia(bvid, filename)