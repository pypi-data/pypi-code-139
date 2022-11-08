from simba.read_config_unit_tests import read_config_file, read_config_entry
from simba.rw_dfs import read_df
from simba.features_scripts.unit_tests import read_video_info_csv, read_video_info
from simba.drop_bp_cords import create_body_part_dictionary, get_fn_ext, getBpNames
import os, glob
import itertools
import numpy as np
from shapely.geometry import Polygon, Point, LineString
from shapely.affinity import rotate
from joblib import Parallel, delayed
import math
import pickle
from shapely.ops import polygonize
import shapely.wkt
from simba.misc_tools import check_multi_animal_status

class AnimalBoundaryFinder(object):
    def __init__(self,
                 config_path: str,
                 anterior_posterior_distance_mm: int or None,
                 lateral_distance_mm: int or None,
                 boundary_dict: dict or None):

        self.config, self.config_path = read_config_file(ini_path=config_path), config_path
        self.boundary_dict, self.anterior_posterior_distance_mm, self.lateral_distance_mm = boundary_dict, anterior_posterior_distance_mm, lateral_distance_mm
        self.project_path = read_config_entry(self.config, 'General settings', 'project_path', data_type='folder_path')
        self.input_dir = os.path.join(self.project_path, 'csv', 'outlier_corrected_movement_location')
        self.file_type = read_config_entry(self.config, 'General settings', 'workflow_file_type', 'str', 'csv')
        self.files_found = glob.glob(self.input_dir + '/*.' + self.file_type)
        if len(self.files_found) == 0:
            print('SIMBA ERROR: ZERO files found')
            raise ValueError()
        self.vid_info_df = read_video_info_csv(os.path.join(self.project_path, 'logs', 'video_info.csv'))
        self.save_path = os.path.join(self.project_path, 'logs', 'anchored_rois.pickle')
        self.boundary_bps = []
        for k, v in boundary_dict.items():
            for k1, v1 in v.items():
                self.boundary_bps.append(v1)
        self.boundary_cord_headers = []
        self.no_animals = read_config_entry(self.config, 'General settings', 'animal_no', 'int')
        self.multi_animal_status, self.multi_animal_id_lst = check_multi_animal_status(self.config, self.no_animals)
        self.x_cols, self.y_cols, self.pcols = getBpNames(config_path)
        self.animal_bp_dict = create_body_part_dictionary(self.multi_animal_status, list(self.multi_animal_id_lst),  self.no_animals, list(self.x_cols), list(self.y_cols), [], [])
        for bp in self.boundary_bps:
            self.boundary_cord_headers.extend([bp + '_x', bp + '_y'])

    def _save_results(self):
        with open(self.save_path, 'wb') as path:
            pickle.dump(self.polygons, path, pickle.HIGHEST_PROTOCOL)

    def find_boundaries_four_defined_body_parts(self):

        def _array_2_polygon_dict(point_array: np.array,
                                  anterior_posterior_distance_px: int,
                                  lateral_distance_px: int):

            lateral, lateral_x, lateral_y = [point_array[2], point_array[3]], [point_array[2][0], point_array[3][0]], [point_array[2][1], point_array[3][1]]
            anterior, posterior = point_array[2], point_array[3]
            anterior_point, posterior_point = Point(point_array[2]), Point(point_array[3])
            ap_angle_degrees = math.degrees(math.atan2(anterior[0] - posterior[0], posterior[1] - anterior[1]))
            ap_angle_radians = math.radians(ap_angle_degrees)
            if ap_angle_degrees < 0:
                ap_angle_degrees += 360
            if (ap_angle_degrees > 270) and (ap_angle_degrees <= 360):
                left_lateral, right_lateral = lateral[np.argmin(lateral_y)], lateral[np.argmax(lateral_y)]
                left_lateral_point, right_lateral_pint = Point(left_lateral), Point(right_lateral)
                lateral_angle_degrees = math.degrees(math.atan2(left_lateral[0] - right_lateral[0], right_lateral[1] - left_lateral[1]))
                lateral_angle_radians = math.radians(lateral_angle_degrees)
                new_anterior_point = Point((anterior_point.x + int(anterior_posterior_distance_px/2) * math.cos(ap_angle_radians)), anterior_point.y + int(anterior_posterior_distance_px/2) * math.sin(ap_angle_radians))
                new_posterior_point = Point((posterior_point.x - int(anterior_posterior_distance_px / 2) * math.cos(ap_angle_radians)), posterior_point.y - int(anterior_posterior_distance_px / 2) * math.sin(ap_angle_radians))
                new_left_lateral_point = Point((anterior_point.x + int(lateral_distance_px/2) * math.cos(ap_angle_radians)), anterior_point.y - int(anterior_posterior_distance_px/2) * math.sin(ap_angle_radians))


            elif (ap_angle_degrees >= 0) and (ap_angle_degrees <= 90):
                left_lateral, right_lateral = lateral[np.argmin(lateral_x)], lateral[np.argmax(lateral_x)]
                lateral_angle_degrees = math.degrees(math.atan2(left_lateral[0] - right_lateral[0], right_lateral[1] - left_lateral[1]))
                lateral_angle_radians = math.radians(lateral_angle_degrees)
                new_anterior_point = Point((anterior_point.x + int(anterior_posterior_distance_px / 2) * math.cos(ap_angle_radians)), anterior_point.y - int(anterior_posterior_distance_px / 2) * math.sin(ap_angle_radians))
                new_posterior_point = Point((posterior_point.x - int(anterior_posterior_distance_px / 2) * math.cos(ap_angle_radians)), posterior_point.y + int(anterior_posterior_distance_px / 2) * math.sin(ap_angle_radians))
            elif (ap_angle_degrees > 90) and (ap_angle_degrees <= 180):
                left_lateral, right_lateral = lateral[np.argmax(lateral_y)], lateral[np.argmin(lateral_y)]
                lateral_angle_degrees = math.degrees(math.atan2(left_lateral[0] - right_lateral[0], right_lateral[1] - left_lateral[1]))
                lateral_angle_radians = math.radians(lateral_angle_degrees)
                new_anterior_point = Point((anterior_point.x - int(anterior_posterior_distance_px / 2) * math.cos(ap_angle_radians)), anterior_point.y - int(anterior_posterior_distance_px / 2) * math.sin(ap_angle_radians))
                new_posterior_point = Point((posterior_point.x + int(anterior_posterior_distance_px / 2) * math.cos(ap_angle_radians)), posterior_point.y + int(anterior_posterior_distance_px / 2) * math.sin(ap_angle_radians))
            elif (ap_angle_degrees > 180) and (ap_angle_degrees <= 270):
                left_lateral, right_lateral = lateral[np.argmin(lateral_y)], lateral[np.argmax(lateral_y)]
                lateral_angle_degrees = math.degrees(math.atan2(left_lateral[0] - right_lateral[0], right_lateral[1] - left_lateral[1]))
                lateral_angle_radians = math.radians(lateral_angle_degrees)
                new_anterior_point = Point((anterior_point.x - int(anterior_posterior_distance_px / 2) * math.cos(ap_angle_radians)), anterior_point.y + int(anterior_posterior_distance_px / 2) * math.sin(ap_angle_radians))
                new_posterior_point = Point((posterior_point.x + int(anterior_posterior_distance_px / 2) * math.cos(ap_angle_radians)), posterior_point.y - int(anterior_posterior_distance_px / 2) * math.sin(ap_angle_radians))






            #
            # print(angle_degrees)
            #
            # left_lateral_cord =
            #
            # ap_length = int(np.sqrt((point_array[0][0] - point_array[0][1]) ** 2 + (point_array[0][1] - point_array[1][1]) ** 2) + anterior_posterior_distance_px)
            # ap_angle_radians = math.atan2(point_array[0][1] - point_array[1][1], point_array[0][0] - point_array[1][0])
            #
            #
            #
            #
            #
            # ap_center_point = Point(point_array[0][0] / 2, point_array[0][1] / 2)
            # ap_end_point = Point(ap_center_point.x + ap_length/2, ap_center_point.y)
            # ap_start_point = Point(ap_center_point.x - ap_length / 2, ap_center_point.y)
            #
            # ap_linestring = LineString([ap_start_point, ap_end_point])
            # ap_linestring = rotate(ap_linestring, ap_angle_radians, origin=ap_start_point, use_radians=False)
            #
            # lateral_length = np.sqrt((point_array[2][0] - point_array[3][1]) ** 2 + (point_array[2][1] - point_array[3][1]) ** 2) + lateral_distance_px
            # lateral_center_point = Point(point_array[2][0] / 2, point_array[2][1] / 2)
            # lateral_end_point = Point(lateral_center_point.x + lateral_length / 2, lateral_center_point.y)
            # lateral_start_point = Point(lateral_center_point.x - lateral_length / 2, lateral_center_point.y)
            # lateral_radians = math.atan2(point_array[2][1] - point_array[3][1], point_array[2][0] - point_array[3][0])
            # lateral_linestring = LineString([lateral_start_point, lateral_end_point])
            # lateral_linestring = rotate(lateral_linestring, lateral_radians, origin=lateral_start_point, use_radians=False)
            #
            #
            # print(ap_linestring, lateral_linestring)
            #

        self.polygons = {}
        for file_cnt, file_path in enumerate(self.files_found):
            _, self.video_name, _ = get_fn_ext(file_path)
            _, px_per_mm, _ = read_video_info(self.vid_info_df, self.video_name)
            if self.anterior_posterior_distance_mm != None:
                self.anterior_posterior_distance_px = int(px_per_mm * self.anterior_posterior_distance_mm)
            else:
                self.verical_distance_px = 0
            if self.lateral_distance_mm != None:
                self.lateral_distance_px = int(px_per_mm * self.lateral_distance_mm)
            else:
                self.horizontal_distance_px = 0
            self.polygons[self.video_name] = {}
            self.data_df = read_df(file_path=file_path,file_type=self.file_type)[self.boundary_cord_headers].astype(int)
            for animal in self.boundary_dict.keys():
                animal_x_cols = [x for x in self.animal_bp_dict[animal]['X_bps'] if x in self.boundary_cord_headers]
                animal_y_cols = [x for x in self.animal_bp_dict[animal]['Y_bps'] if x in self.boundary_cord_headers]
                animal_arr = self.data_df[[x for x in itertools.chain.from_iterable(itertools.zip_longest(animal_x_cols,animal_y_cols)) if x]].astype(int).values
                animal_arr = np.reshape(animal_arr, (-1, 4, 2))
                self.polygons[self.video_name][animal] = Parallel(n_jobs=5, verbose=2, backend="loky")(delayed(_array_2_polygon_dict)(x, self.anterior_posterior_distance_px, self.lateral_distance_px) for x in animal_arr)

        self._save_results()




test = AnimalBoundaryFinder(config_path='/Users/simon/Desktop/troubleshooting/train_model_project/project_folder/project_config.ini',
                            anterior_posterior_distance_mm=10,
                            lateral_distance_mm=1,
                            boundary_dict={'Animal_1': {'Anterior': 'Nose_1', 'Posterior': 'Tail_base_1', 'Lateral_1': 'Lat_right_1', 'Lateral_2': 'Lat_left_1'},
                                           'Animal_2': {'Anterior': 'Nose_2', 'Posterior': 'Tail_base_2', 'Lateral_1': 'Lat_right_2', 'Lateral_2': 'Lat_left_2'}})
test.find_boundaries_four_defined_body_parts()





