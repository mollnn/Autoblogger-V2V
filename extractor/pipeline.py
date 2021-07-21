import os.path
import common
import cutter_danmu
import shotcut
import spider
import formatter

# --- Function List ---
# def downloadMedia(bvid):
# def downloadInfo(bvid):
# def shotCut(bvid):
# def extract(bvid, src_type, clip_type):
# ---------------------


def extract(bvid, src_type, clip_type):
    print("extractor.main.extract: Hello!")
    if len(common.query(common.readConfig("dbname"), """
        select * from extraction where bvid='{bvid}' and src_type='{src_type}' and clip_type='{clip_type}'
        """.format(bvid=bvid, src_type=src_type, clip_type=clip_type))) > 0:
        print("extractor.main.extract: Already extracted with same bvid, src_type and clip_type. Terminated.")
        return
    if src_type == 0 and clip_type == 0:
        cutter_danmu.solve(bvid)
    # elif src_type == 0 and clip_type == 1:
    #     extractor.xlove.solve(bvid)
    # elif src_type == 0 and clip_type == 2:
    #     extractor.xshock.solve(bvid)
    # elif src_type == 0 and clip_type == 3:
    #     extractor.xhumor.solve(bvid)
    else:
        print("Unsupported Type Parameters!")


def shotCut(bvid):
    print("extractor.main.shotCut: Hello!")
    if len(common.query(common.readConfig("dbname"), """
        select * from shotcut where bvid='{bvid}'
        """.format(bvid=bvid))) > 0:
        print("extractor.main.doShotCut: Already cut. Shotcut process terminated.")
        return

    ans = shotcut.shotcut('../data/media/'+bvid+'.mp4')

    for item in ans:
        cutid = common.generateCutid()
        if item["transition"] == "gradual":
            common.query(common.readConfig("dbname"), """
                insert into shotcut 
                (bvid, cutid, transition, start_frame, end_frame)
                values
                ('%s','%s','%s',%d,%d)
                """ % (bvid, cutid, item["transition"], item["start_frame"], item["end_frame"]))
        else:
            common.query(common.readConfig("dbname"), """
                insert into shotcut 
                (bvid, cutid, transition, cut_frame)
                values
                ('%s','%s','%s',%d)
                """ % (bvid, cutid, item["transition"], item["cut_frame"]))

    print("extractor.main.doShotCut: Finish all SQL Writing.")


def downloadInfo(bvid):
    print("extractor.main.downloadInfo: Hello!")
    ans = common.query(
        common.readConfig("dbname"), "select * from Vinfo where bvid='%s'" % bvid)
    if len(ans) > 0:
        print("extractor.main.downloadInfo: Info already exists. Terminated.")
        return
    spider.getInfo(bvid)


def downloadMedia(bvid):
    print("extractor.main.downloadMedia: Hello!")
    if os.path.isfile('../data/media/'+bvid+'.mp4'):
        print("extractor.main.downloadMedia: Media already exists. Terminated.")
        return
    spider.getMP4ByBid(
        bvid, ffmpeg_config="-c:v libx264 -c:a aac -vf scale=320:180 -r 24 -strict experimental -threads 4 -preset ultrafast")


def importMedia(bvid, filename):
    print("extractor.main.importMedia: Hello!")
    if os.path.isfile('../data/media/'+bvid+'.mp4'):
        print("extractor.main.importMedia: Media already exists. Terminated.")
        return
    if os.path.isfile(filename) == False:
        print("extractor.main.importMedia: Source media invalid. Terminated.")
    formatter.importMP4(
        bvid, filename, ffmpeg_config="-c:v libx264 -c:a aac -vf scale=320:180 -r 24 -strict experimental -threads 4 -preset ultrafast")