import ffmpeg
import json
import os
import re
import json

def edit(clip_desc_list, output_filename, quiet=True):
    # clip_desc_list is a list of dict{'filename'=?, 'start'=?, 'duration'=?}
    clip_list = []
    for clip_desc in clip_desc_list:
        clip = ffmpeg.input(
            clip_desc["filename"], ss=clip_desc["start"], t=clip_desc["duration"])
        clip_list += [clip]
    ans = clip_list[0]
    for i in range(1, len(clip_list)):
        ans = ffmpeg.concat(ans, clip_list[i])
    ans.output(output_filename).run(quiet=True, overwrite_output=True)

