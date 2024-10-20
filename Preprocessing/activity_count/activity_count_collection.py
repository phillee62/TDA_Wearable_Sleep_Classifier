import numpy as np

from .. import interval


class ActivityCountCollection(object):
    def __init__(self, subject_id, data):
        self.subject_id = subject_id
        self.data = data
        self.timestamps = data[:, 0]
        self.values = data[:, 1:]

    def get_interval(self):
        return interval(start_time=np.amin(self.data[:, 0]),
                        end_time=np.amax(self.data[:, 0]))
