import sys
sys.path.append("..")

import extractor.pipeline

bvid="BV1rs411s7Ur"
extractor.pipeline.downloadMedia(bvid)
extractor.pipeline.downloadInfo(bvid)
extractor.pipeline.shotCut(bvid)
extractor.pipeline.extract(bvid,0,0)