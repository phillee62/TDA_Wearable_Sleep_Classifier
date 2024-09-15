# import numpy as np

# from .source.constants import Constants
# # from .activity_count.activity_count_feature_service import ActivityCountFeatureService
# # from activity_count_feature_service import ActivityCountFeatureService
# from .heart_rate.heart_rate_feature_service import HeartRateFeatureService
# from .psg.psg_label_service import PSGLabelService
# from .raw_data_processor import RawDataProcessor
# from .time.time_based_feature_service import TimeBasedFeatureService

# from .source import utils
# from .activity_count.activity_count_service import ActivityCountService
# from .source.epoch import Epoch
# from .heart_rate.heart_rate_service import HeartRateService
# from .source.interval import Interval
# from .motion.motion_service import MotionService
# from .psg.psg_service import PSGService
# from .sleep_stage import SleepStage

# from .psg.psg_file_type import PSGFileType
# from .psg.report_summary import ReportSummary

# class Epoch(object):
#     DURATION = 30  # seconds

#     def __init__(self, timestamp, index):
#         self.timestamp = timestamp
#         self.index = index

# class Interval(object):
#     def __init__(self, start_time, end_time):
#         self.start_time = start_time
#         self.end_time = end_time

# class FeatureBuilder(object):

#     @staticmethod
#     def build(subject_id):
#         if Constants.VERBOSE:
#             print("Getting valid epochs...")
#         valid_epochs = RawDataProcessor.get_valid_epochs(subject_id)

#         if Constants.VERBOSE:
#             print("Building features...")
#         FeatureBuilder.build_labels(subject_id, valid_epochs)
#         FeatureBuilder.build_from_wearables(subject_id, valid_epochs)
#         FeatureBuilder.build_from_time(subject_id, valid_epochs)

#     @staticmethod
#     def build_labels(subject_id, valid_epochs):
#         psg_labels = PSGLabelService.build(subject_id, valid_epochs)
#         PSGLabelService.write(subject_id, psg_labels)

#     @staticmethod
#     def build_from_wearables(subject_id, valid_epochs):

#         count_feature = ActivityCountFeatureService.build(subject_id, valid_epochs)
#         heart_rate_feature = HeartRateFeatureService.build(subject_id, valid_epochs)
#         ActivityCountFeatureService.write(subject_id, count_feature)
#         HeartRateFeatureService.write(subject_id, heart_rate_feature)

#     @staticmethod
#     def build_from_time(subject_id, valid_epochs):

#         if Constants.INCLUDE_CIRCADIAN:
#             circadian_feature = TimeBasedFeatureService.build_circadian_model(subject_id, valid_epochs)
#             TimeBasedFeatureService.write_circadian_model(subject_id, circadian_feature)

#         cosine_feature = TimeBasedFeatureService.build_cosine(valid_epochs)
#         time_feature = TimeBasedFeatureService.build_time(valid_epochs)

#         TimeBasedFeatureService.write_cosine(subject_id, cosine_feature)
#         TimeBasedFeatureService.write_time(subject_id, time_feature)

# class RawDataProcessor:
#     BASE_FILE_PATH = utils.get_project_root().joinpath('outputs/cropped/')

#     @staticmethod
#     def crop_all(subject_id):
#         # psg_raw_collection = PSGService.read_raw(subject_id)       # Used to extract PSG details from the reports
#         psg_raw_collection = PSGService.read_precleaned(subject_id)  # Loads already extracted PSG data
#         motion_collection = MotionService.load_raw(subject_id)
#         heart_rate_collection = HeartRateService.load_raw(subject_id)

#         valid_interval = RawDataProcessor.get_intersecting_interval([psg_raw_collection,
#                                                                      motion_collection,
#                                                                      heart_rate_collection])

#         psg_raw_collection = PSGService.crop(psg_raw_collection, valid_interval)
#         motion_collection = MotionService.crop(motion_collection, valid_interval)
#         heart_rate_collection = HeartRateService.crop(heart_rate_collection, valid_interval)

#         PSGService.write(psg_raw_collection)
#         MotionService.write(motion_collection)
#         HeartRateService.write(heart_rate_collection)
#         ActivityCountService.build_activity_counts_without_matlab(subject_id, motion_collection.data)  # Builds activity counts with python, not MATLAB

#     @staticmethod
#     def get_intersecting_interval(collection_list):
#         start_times = []
#         end_times = []
#         for collection in collection_list:
#             interval = collection.get_interval()
#             start_times.append(interval.start_time)
#             end_times.append(interval.end_time)

#         return Interval(start_time=max(start_times), end_time=min(end_times))

#     @staticmethod
#     def get_valid_epochs(subject_id):

#         psg_collection = PSGService.load_cropped(subject_id)
#         motion_collection = MotionService.load_cropped(subject_id)
#         heart_rate_collection = HeartRateService.load_cropped(subject_id)

#         start_time = psg_collection.data[0].epoch.timestamp
#         motion_epoch_dictionary = RawDataProcessor.get_valid_epoch_dictionary(motion_collection.timestamps,
#                                                                               start_time)
#         hr_epoch_dictionary = RawDataProcessor.get_valid_epoch_dictionary(heart_rate_collection.timestamps,
#                                                                           start_time)

#         valid_epochs = []
#         for stage_item in psg_collection.data:
#             epoch = stage_item.epoch

#             if epoch.timestamp in motion_epoch_dictionary and epoch.timestamp in hr_epoch_dictionary \
#                     and stage_item.stage != SleepStage.unscored:
#                 valid_epochs.append(epoch)

#         return valid_epochs

#     @staticmethod
#     def get_valid_epoch_dictionary(timestamps, start_time):
#         epoch_dictionary = {}

#         for ind in range(np.shape(timestamps)[0]):
#             time = timestamps[ind]
#             floored_timestamp = time - np.mod(time - start_time, Epoch.DURATION)

#             epoch_dictionary[floored_timestamp] = True

#         return epoch_dictionary

# import datetime as dt

# class TimeService(object):
#     @staticmethod
#     def get_start_epoch_timestamp(report_summary: ReportSummary):
#         if report_summary.file_type == PSGFileType.Compumedics:
#             study_date = dt.datetime.strptime(report_summary.study_date + ' ' + report_summary.start_time,
#                                               '%m/%d/%Y %I:%M:%S %p')
#             if study_date.strftime('%p') == 'AM':
#                 study_date += dt.timedelta(days=1)
#             return study_date.timestamp()

#         if report_summary.file_type == PSGFileType.Vitaport:
#             study_date = dt.datetime.strptime(report_summary.study_date + ' ' + report_summary.start_time,
#                                               '%m/%d/%y %H:%M:%S')
#             if int(study_date.strftime('%H')) < 12:
#                 study_date += dt.timedelta(days=1)
#             return study_date.timestamp()
