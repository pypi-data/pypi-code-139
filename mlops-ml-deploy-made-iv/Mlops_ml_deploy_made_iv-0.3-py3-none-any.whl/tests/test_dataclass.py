"""Unittest for src.data.entities.*"""

import unittest
from unittest import mock
import logging
import pandas as pd

import src
from src.entities import *


class TestDataClass(unittest.TestCase):
    """Tests for dataclasses"""

    def test_dataset_params(self):
        """Should test for DatasetParams"""
        input_file = 'test.csv'
        output_files = ['test1.csv', 'test2.csv']

        ds = DatasetParams(input_file_path=input_file, output_paths=output_files)
        self.assertEqual(ds.input_file_path, input_file)
        self.assertEqual(ds.output_paths, output_files)

    def test_feature_params(self):
        """Should test for FeatureParams"""
        cat_cols = ['1', '2', '3']
        num_cols = ['4', '5', '6']
        target_col = '7'

        ft = FeatureParams(categorical_features=cat_cols, numerical_features=num_cols, target_col=target_col)
        self.assertEqual(ft.target_col, target_col)
        self.assertEqual(ft.categorical_features, cat_cols)
        self.assertEqual(ft.numerical_features, num_cols)

    def test_preprocessing_params(self):
        """Should test for PreprocessingParams"""
        params_list = ['1', '2', '3']
        pp = PreprocessingParams(pipeline=params_list)
        self.assertEqual(pp.pipeline, params_list)

    def test_model_params(self):
        """Should test for ModelParams"""
        model_save_path = 'test.csv'
        model_name = 'Model'
        parameters = [1, 2, 3]
        sp = ModelParams(model_save_path=model_save_path, model_name=model_name, parameters=parameters)
        self.assertEqual(sp.model_save_path, model_save_path)
        self.assertEqual(sp.model_name, model_name)
        self.assertEqual(sp.parameters, parameters)


if __name__ == "__main__":
    unittest.main()
