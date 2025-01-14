import os

from ..source import utils
from ..source.constants import Constants


class CircadianService(object):

    @staticmethod
    def build_circadian_model():
        os.system(Constants.MATLAB_PATH + ' -nodisplay -nosplash -nodesktop -r \"run(\'' + str(
            utils.get_project_root()) + '/preprocessing/time/clock_proxy/Circadian_DLMO_Model/runCircadianModel.m\'); exit;\"')

    @staticmethod
    def build_CRHR_model():
        os.system(Constants.MATLAB_PATH + ' -nodisplay -nosplash -nodesktop -r \"run(\'' + str(
            utils.get_project_root()) + '/preprocessing/time/clock_proxy/CRHR/run_CRHR_Model.m\'); exit;\"')

    @staticmethod
    def build_circadian_mesa():
        os.system(Constants.MATLAB_PATH + ' -nodisplay -nosplash -nodesktop -r \"run(\'' + str(
            utils.get_project_root()) + '/preprocessing/time/clock_proxy/Circadian_DLMO_Model/runCircadianMESA.m\'); exit;\"')
