from .settings import Settings
from six import string_types
from .model import Model
from .versioning import Versioning
from .global_functions import globalFunctions as gf
from datetime import date
from github import Github
import os
import json


class Validate:
    def __init__(self, id="Optional"):
        self._id = id
        self._mae_value = 0
        self._mae_expected_value = 0
        self._mae_deviation_percentage = 0
        self._r2_value = 0
        self._r2_expected_value = 0
        self._r2_deviation_percentage = 0
        self._mae_valid = False
        self._r2_valid = False

    # MAE values
    @property
    def MAE_Deviation_percentage(self):
        """
        :type: float
        """
        return self._mae_deviation_percentage

    @MAE_Deviation_percentage.setter
    def MAE_Deviation_percentage(self, value):
        """
        :type: float
        """
        self._mae_deviation_percentage = value

    @property
    def Mae_expected_value(self):
        """
        :type: float
        """
        return self._mae_expected_value

    @Mae_expected_value.setter
    def Mae_expected_value(self, value):
        """
        :type: float
        """
        self._mae_expected_value = value

    # R2 values
    @property
    def R2_Deviation_percentage(self):
        """
        :type: float
        """
        return self._r2_deviation_percentage

    @R2_Deviation_percentage.setter
    def R2_Deviation_percentage(self, value):
        """
        :type: float
        """
        self._r2_deviation_percentage = value

    @property
    def R2_expected_value(self):
        """
        :type: float
        """
        return self._r2_expected_value

    @R2_expected_value.setter
    def R2_expected_value(self, value):
        """
        :type: float
        """
        self._r2_expected_value = value

    def Start_validation(self, localpath="Optional", model_url="Optional", model_port="Optional"):
        if localpath == "Optional":
            localpath = gf.Path_is_dir(
                Settings.Base_path + "/" + Settings.Enviroment_name + "/" + Settings.Enviroment_version + "/")
        else:
            localpath = gf.Path_is_dir(localpath)

        # Get Values from model
        model = Model()
        if model_url != "Optional":
            model.Model_URL = model_url
        if model_port != "Optional":
            model.Model_port = model_port

        response = model.Custom_request("post", "/validate")
        response_json = response.json()
        self._mae_value = response_json["MAE_value"]
        self._r2_value = response_json["R2_value"] * 100

        # Calculate max MAE and min MAE
        max_mae = self._mae_expected_value + \
            ((self._mae_expected_value / 100) * self._mae_deviation_percentage)
        min_mae = self._mae_expected_value - \
            ((self._mae_expected_value / 100) * self._mae_deviation_percentage)

        # check if MAE value is within range
        if self._mae_value >= min_mae and self._mae_value <= max_mae:
            print("MAE value is within range")
            self._mae_valid = True

        # Calculate max R2% and min R2%
        max_r2 = self._r2_expected_value + \
            ((self._r2_expected_value / 100) * self._r2_deviation_percentage)
        min_r2 = self._r2_expected_value + \
            ((self._r2_expected_value / 100) * self._r2_deviation_percentage)

        # check if MAE value is within range
        if self._r2_value >= min_r2 and self._r2_value <= max_r2:
            print("R2 value is within range")
            self._r2_valid = True

        print("Writing validation data to: " + localpath)
        self.Save_validation_results(localpath)
        print("Done writing validation results")

        if self._mae_valid and self._r2_valid:
            version = Versioning()
            version.Upload_enviroment()

    def Save_validation_results(self, localpath):
        git = Github(Settings.Gitaccesstoken)
        git_user = git.get_user()
        git_user_data = git_user.get_emails()

        # Create validation documentation
        validation_json = {
            "validation_date": date.today().strftime("%d-%m-%Y"),
            "validation_by": git_user_data[0].email,
            "expected_mae_value": self._mae_expected_value,
            "mae_deviation_percentage": self._mae_deviation_percentage,
            "actual_mae_value": self._mae_value,
            "expected_R2_value": self._r2_expected_value,
            "R2_deviation_percentage": self._r2_deviation_percentage,
            "actual_R2_value": self._r2_value,
            "mae_within_expected_range": self._mae_valid,
            "r2_within_expected_range": self._r2_valid
        }

        path = localpath + "/validation_data/validation_data.json"

        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(json.dumps(validation_json))

        return True
