# https://github.com/SaeidDadkhah/Shot-Boundary-Detection/blob/master/ShotBoundaryDetection.py

# Object of type time is not JSON serializable 
# Fix by mollnn

import cv2
import numpy as np
import warnings

import common
import time

class ShotcutDetector:
    def __init__(self):
        # Video attributes
        self._vid = None
        self.__frame = None
        self.__rearranged = False
        self.__total_frames = 0

        # Shot boundary attributes
        self.sb = []

    def __set_video(self, vid):
        # Video attributes
        self._vid = vid
        self.__frame = None
        self.__rearranged = False
        self.__total_frames = self._vid.get(cv2.CAP_PROP_FRAME_COUNT)

        # Shot boundary attributes
        self.sb = []

    def open_video(self, file):
        vid = cv2.VideoCapture(file)
        if vid.isOpened():
            self.__set_video(vid)
            return True
        else:
            return False

    def video_is_available(self):
        return self._vid is not None and self._vid.isOpened()

    def next_frame(self, rearrange=False):
        a = self._vid.get(cv2.CAP_PROP_POS_FRAMES)
        if a >= self.__total_frames - 1:
            return None
        valid, self.__frame = self._vid.read()
        if valid:
            if rearrange:
                return self.__rearrange()
            else:
                return self.__frame
        else:
            return self.__frame

    def set_frame(self, frame):
        self._vid.set(cv2.CAP_PROP_POS_FRAMES, frame)

    def current_frame(self, rearrange=False):
        if rearrange:
            if self.__rearranged:
                return self.__frame
            else:
                return self.__rearrange()
        else:
            return self.__frame

    def previous_frame(self, rearrange=False):
        frame_pos = self._vid.get(cv2.CAP_PROP_POS_FRAMES)
        if frame_pos <= 1:
            return None
        self._vid.set(cv2.CAP_PROP_POS_FRAMES, frame_pos - 2)
        return self.next_frame(rearrange)

    def __rearrange(self):
        b, g, r = cv2.split(self.__frame)
        self.__frame = cv2.merge((r, g, b))
        self.__rearranged = True
        return self.__frame

    def __detect_multi_step_comparison_scheme(self,
                                              set_progress=None,
                                              cut_l=4,
                                              cut_threshold=45,
                                              gradual_l=10,
                                              gradual_threshold=42.5,
                                              mu_threshold=2):
        cnt_progress=0
        
        def calc_phi_eta(alg_atr_l):
            def calc_sigma():
                res = 0
                n_max = len(histograms)
                if 0 < n - l < n_max and 0 < n + 1 + l < n_max:
                    for back_hist, for_hist in zip(histograms[n - l], histograms[n + 1 + l]):
                        # noinspection PyUnresolvedReferences
                        res += sum(np.abs(back_hist - for_hist))
                    return 100 / (2 * 3 * width * height) * res
                else:
                    return 0

            def calc_local_mean():
                start_l = n - 2 * alg_atr_l
                start_l = start_l if start_l > 0 else 0
                end_l = n + 2 * alg_atr_l
                end_l = end_l if end_l < len(sigma) else len(sigma)
                two_summation = np.sum(sigma[range(start_l, end_l)])
                return two_summation[0][0] / ((end_l - start_l + 1) * (alg_atr_l + 1))

            # calculate sigma
            sigma = []
            for n in range(len(histograms)):
                tmp = []
                for l in range(alg_atr_l + 1):
                    tmp.append(calc_sigma())
                # sigma.append(np.array(tmp))
                sigma.append(tmp)
            sigma = np.matrix(sigma)

            # calculate local means
            # noinspection PyShadowingNames
            mu = []
            for n in range(len(histograms)):
                mu.append(np.array([calc_local_mean()] * (alg_atr_l + 1)))
            # noinspection PyShadowingNames
            mu = np.matrix(mu)

            # calculate eta
            # noinspection PyShadowingNames
            eta = sigma - mu

            # calculate phi
            # noinspection PyShadowingNames
            phi = np.sum(eta, axis=1)

            # plt.suptitle("L = {x}".format(x=alg_atr_l))
            # plt.subplot(411), plt.plot(range(len(sigma)), sigma), plt.title("sigma")
            # plt.subplot(412), plt.plot(range(len(mu)), mu), plt.title("mu")
            # plt.subplot(413), plt.plot(range(len(eta)), eta), plt.title("eta")
            # plt.subplot(414), plt.plot(range(len(phi)), phi), plt.title("phi")
            # plt.show()
            return phi, eta

        def zero_crossing_detection(array):
            array_start = []
            array_max = []
            array_end = []

            for i in range(1, len(array) - 1):
                if array[i - 1] < 0 < array[i + 1]:
                    try:
                        if array_start[-1] == i - 1:
                            continue
                    except IndexError:
                        pass
                    array_start.append(i)
                    current_max = i + 1
                    i += 1
                    while i < len(array) and 0 < array[i + 1]:
                        if array[current_max] < array[i]:
                            current_max = i
                        i += 1
                    array_max.append(current_max)
                    array_end.append(i)

            return array_start, array_max, array_end

        if self.video_is_available():
            if set_progress is not None:
                set_progress(0, "Making histograms")

            current_frame_num = self._vid.get(cv2.CAP_PROP_POS_FRAMES)

            self._vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
            colors = ('b', 'g', 'r')
            width = self._vid.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = self._vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
            frame_count = self._vid.get(cv2.CAP_PROP_FRAME_COUNT)

            valid, frame = self._vid.read()
            histograms = []
            while valid:
                histograms.append([])
                for i, col in enumerate(colors):
                    histograms[-1].append(
                        np.array(cv2.calcHist([frame], [i], None, [8], [0, 256])))
                if set_progress is not None:
                    set_progress(
                        int(55 * self._vid.get(cv2.CAP_PROP_POS_FRAMES) / frame_count),
                        "Making histograms")

                if self._vid.isOpened():
                    valid, frame = self._vid.read()
                else:
                    valid = False

            # return video to first state
            self._vid.set(cv2.CAP_PROP_POS_FRAMES, current_frame_num)

            # print(len(histograms))

            # cut detection
            # print("{s}: {t}".format(s="cut; phi, eta",
            #                         t=datetime.datetime.now()))
            if set_progress is not None:
                set_progress(55, "Processing cuts")
            phi, eta = calc_phi_eta(cut_l)
            # print("{s}: {t}".format(s="cut; zero",
            #                         t=datetime.datetime.now()))
            phi_start, phi_max, phi_end = zero_crossing_detection(phi)

            # print("{s}: {t}".format(s="cut; final",
            #                         t=datetime.datetime.now()))
            cuts = []
            for pm in phi_max:
                if phi.item((pm, 0)) > cut_threshold and eta.item((pm, 0)) > mu_threshold:
                    if 0.5 < eta.item((pm, 0)) / eta.item((pm, 1)) < 2:
                        cuts.append(pm)
                        # print(phi.item((pm, 0)))

            # gradual transition detection
            # print("{s}: {t}".format(s="grad; phi, eta",
            #                         t=datetime.datetime.now()))
            if set_progress is not None:
                set_progress(58, "Processing gradual transition")
            phi, eta = calc_phi_eta(gradual_l)
            # print("{s}: {t}".format(s="grad; zero",
            #                         t=datetime.datetime.now()))
            phi_start, phi_max, phi_end = zero_crossing_detection(phi)

            # print("{s}: {t}".format(s="grad; final",
            #                         t=datetime.datetime.now()))
            gradual_transitions = []
            for ps, pm, pe in zip(phi_start, phi_max, phi_end):
                if phi.item((pm, 0)) > gradual_threshold and eta.item((pm, 0)) < mu_threshold:
                    gradual_transitions.append((ps, pe))
                    # print(phi.item((pm, 0)))

            if set_progress is not None:
                set_progress(65, "Finalizing results...")
            return cuts, gradual_transitions
        else:
            print("shotcut: Error: Video is not available!")

    def detect(self, set_progress=None, finish=None):

        # noinspection PyShadowingNames
        cuts, gradual_transitions = self.__detect_multi_step_comparison_scheme(set_progress=set_progress)
        # print("{s}: {t}".format(s="finalize sbd",
        #                         t=datetime.datetime.now()))

        self.sb = []
        cut_index = 0
        gradual_index = 0
        total_transitions = len(cuts) + len(gradual_transitions)
        while cut_index < len(cuts) and gradual_index < len(gradual_transitions):
            if cuts[cut_index] < gradual_transitions[gradual_index][0]:
                self.sb.append({'transition': 'cut',
                                'cut_frame': cuts[cut_index]})
                cut_index += 1
            else:
                self.sb.append({'transition': 'gradual',
                                'start_frame': gradual_transitions[gradual_index][0],
                                'end_frame': gradual_transitions[gradual_index][1]})
                gradual_index += 1
            if set_progress is not None:
                set_progress(65 + 35 * (cut_index + gradual_index) / total_transitions, "Finalizing results...")

        while cut_index < len(cuts):
            self.sb.append({'transition': 'cut',
                            'cut_frame': cuts[cut_index]})
            cut_index += 1
            if set_progress is not None:
                set_progress(65 + 35 * (cut_index + gradual_index) / total_transitions, "Finalizing results...")
        
        while gradual_index < len(gradual_transitions):
            self.sb.append({'transition': 'gradual',
                            'start_frame': gradual_transitions[gradual_index][0],
                            'end_frame': gradual_transitions[gradual_index][1]})
            gradual_index += 1
            if set_progress is not None:
                set_progress(65 + 35 * (cut_index + gradual_index) / total_transitions, "Finalizing results...")

        # print("{s}: {t}".format(s="finalize gui",
        #                         t=datetime.datetime.now()))
        # print(self.sb)

        if finish is not None:
            finish()

def solve_shotcut(filename):
    time_start=time.time()
    sbd = ShotcutDetector()
    sbd.open_video(filename)
    sbd.detect()
    print("    shotcut time usage: ", time.time()-time_start)
    return sbd.sb

####################################################

# 镜头分割，并写入数据库（弃用）
def shotcut_to_sql(bvid):
    if len(common.query(common.readConfig("dbname"), """
        select * from shotcut where bvid='{bvid}'
        """.format(bvid=bvid))) > 0:
        print("shotcut: Already cut. Shotcut process terminated.")
        return

    ans = solve_shotcut('../data/media/'+bvid+'.mp4')

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

# 返回镜头分割结果
def shotcut(bvid):
    warnings.filterwarnings("ignore")
    ans = solve_shotcut('../data/media/'+bvid+'.mp4')
    return ans