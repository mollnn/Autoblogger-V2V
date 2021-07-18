import sys
sys.path.append("..")

import extractor.pipeline

bvid="BV1S4411n71U"
# extractor.pipeline.downloadMedia(bvid)
# extractor.pipeline.downloadInfo(bvid)
# extractor.pipeline.shotCut(bvid)
extractor.pipeline.extract(bvid,0,0)