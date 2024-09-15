import time
# import Preprocessing

from Preprocessing.source.analysis.setup.subject_builder import SubjectBuilder
from Preprocessing.source.constants import Constants
from Preprocessing.activity_count.activity_count_service import ActivityCountService
from Preprocessing.feature_builder import FeatureBuilder
from Preprocessing.raw_data_processor import RawDataProcessor
from Preprocessing.time.circadian_service import CircadianService

from Preprocessing.Topological_features import Extract_TFs

# import Preprocessing.Topological_features

def run_preprocessing(subject_set):
    start_time = time.time()

    for subject in subject_set:
        print("Cropping data from subject " + str(subject) + "...")
        RawDataProcessor.crop_all(str(subject))

    if Constants.INCLUDE_CIRCADIAN:
        ActivityCountService.build_activity_counts()  # This uses MATLAB, but has been replaced with a python implementation
        # CircadianService.build_circadian_model()      # Both of the circadian lines require MATLAB to run
        # CircadianService.build_circadian_mesa()       # INCLUDE_CIRCADIAN = False by default because most people don't have MATLAB

    for subject in subject_set:
        FeatureBuilder.build(str(subject))

    for subject in subject_set:
        Extract_TFs(str(subject))

    end_time = time.time()
    print("Execution took " + str((end_time - start_time) / 60) + " minutes")

subject_ids = SubjectBuilder.get_all_subject_ids()
run_preprocessing(subject_ids)
