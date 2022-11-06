import pandas as pd
from time import time
import pathlib
import os
import numpy as np
import math


def test():
    print("Hallo")



def func_resample_df_to_frequency(df,
                                  method="snapshot",
                                  frequency="H",
                                  ):

    # method either takes snapshot at full hours (instantaneous values. simplified method) or weighted means per hour (detailed, precise method).
    list_methods = ["snapshot", "weighted", "groupby", "weighted_slow", ]
    if method not in list_methods:
        raise ValueError("Invalid method. Expected one of: {}".format(list_methods))

    # make a copy to maintain original df
    df_return = df.copy()

    # if index is datetime, convert to integer. will be redone at the end.
    if isinstance(df.index, pd.DatetimeIndex):
        df_return.index = (df_return.index - df_return.index.min()) / pd.Timedelta("1 hour")

    # get columns names
    list_variables = df_return.columns

    #df_return)
    #print(df_return)

    start_value_index = df_return.index.min()
    #print("start_value_index: {}".format(start_value_index))

    if method == "groupby":
        if not isinstance(df.index, pd.DatetimeIndex):
            df_return.index = pd.Timestamp('2021-01-01')+pd.to_timedelta(df_return.index, unit='H')

        df_return = df_return.groupby(pd.Grouper(freq="H", label="right", closed="right")).mean()

    if not method == "groupby":
        # index is still in fraction of hours
        # set all full hours to index in case of time steps larger than 1 hour
        ## get index min and max as integer
        idx_min_int = math.floor(df_return.index.min())
        #if idx_min_int != 0:
        #    print("Attention: Time series does not start from 0.")
        idx_max_int = math.ceil(df_return.index.max())
        #print("idx_min_int: {}".format(idx_min_int))
        #print("idx_max_int: {}".format(idx_max_int))

        idx_from_zero = df_return.index - idx_min_int
        df_return.index = idx_from_zero

        number_simulated_hours = idx_max_int - idx_min_int
        #print("number_simulated_hours: {}".format(number_simulated_hours))
        #display(idx_from_zero)

        ## create float index according to given frequency


        # transformation from string to timedelta object
        # https://stackoverflow.com/questions/31469811/convert-pandas-freq-string-to-timedelta
        number_integer_steps = int(pd.Timedelta(number_simulated_hours, "H") / pd.Timedelta(to_offset(frequency)))
        #print("number_integer_steps: {}".format(number_integer_steps))

        idx_integer_steps = pd.Index(list(range(number_integer_steps + 1)))
        #print("idx_integer_steps: {}".format(idx_integer_steps))

        factor_scaling = number_integer_steps / number_simulated_hours
        #print("factor_scaling: {}".format(factor_scaling))

        # stretch index to ... so that math.ceil can be used for integers
        idx_return_stretched = df_return.index * factor_scaling
        #print("idx_return_stretched: {}".format(idx_return_stretched))

        # set index
        df_return.index = idx_return_stretched
        #display("df_return: ", df_return)


        ## union
        # union with full intervals
        idx_complete = df_return.index.union(idx_integer_steps)

        ## set index including all full hours. interpolate missing values.
        df_return = df_return.reindex(idx_complete).interpolate(method="index")
        #display("df_return: ", df_return)

        #print("0: {}".format(df_return))


    if method == "weighted":

        # get full hours for later groupby
        ## rounding up ("ceil") is is equivalent to pandas resample with label="right" and closed="right"
        df_return['bins_of_frequency'] = np.ceil(df_return.index)

        #print(df_return)

        # get weight according to length of time step. fill first value with
        ## if the prn file starts with time 0 this value "0" is "alone" and has to be maintained by fillna(1)
        ## division by zero has to be avoided
        if df_return["bins_of_frequency"][0] == 0:
            value_fillna = 1
        ## if prn file does not start with time 0 the first value has no weight
        else:
            value_fillna = 0
        df_return['weight'] = df_return.index.to_series().diff().fillna(value_fillna)

        #df_return.groupby("bins_of_frequency").apply(display)
        df_return = df_return.groupby("bins_of_frequency").apply(lambda x: pd.Series(np.average(x[list_variables], weights=x["weight"], axis=0), index=list_variables)).rename_axis(None)
        #display(df_return)

    elif method == "weighted_slow":

        # get full hours for later groupby
        ## rounding up ("ceil") is is equivalent to pandas resample with label="right" and closed="right"
        df_return['bins_of_frequency'] = np.ceil(df_return.index)

        #print(df_return)

        # get weight according to length of time step. fill first value with
        ## if the prn file starts with time 0 this value "0" is "alone" and has to be maintained by fillna(1)
        ## division by zero has to be avoided
        if df_return["bins_of_frequency"][0] == 0:
            value_fillna = 1
        ## if prn file does not start with time 0 the first value has no weight
        else:
            value_fillna = 0
        df_return['weight'] = df_return.index.to_series().diff().fillna(value_fillna)

        # use user defined function
        df_return = df_return.groupby("bins_of_frequency").apply(wavg, list_variables, "weight").rename_axis(None)


    elif method == "snapshot":

        # select only full integers for index
        df_return = df_return.reindex(idx_integer_steps)

    #display("df_return: ", df_return)

    # index might still be stretched of not frequency is not full hours
    # set integer index back to float fraction of hours
    df_return.index = df_return.index.to_series().divide(factor_scaling).add(idx_min_int)
    #display("df_return: ", df_return)

    # if original index was datetime, reset to datetime
    if isinstance(df.index, pd.DatetimeIndex):
        df_return.index = pd.Timestamp('2021-01-01') + pd.to_timedelta(df_return.index, unit='H')

    #display(df_return)

    return df_return


def func_read_ida_prn_to_df(prn_path,
                            sep,
                            start_year,
                            resample_to_frequency_method=None,
                            resample_to_frequency=None,
                            set_datetime_index=True,
                            read_variables=[],
                            ):

    #print(prn_path)

    # function which reads an IDA ICE prn.

    # read prn file
    time_import_start = time()

    #print(prn_path)
    #try:
    df_read = pd.read_csv(prn_path,
                              #delimiter="\s+|\t", #sep='\s+' # only supported for slower python engine
                              sep=sep,
                              skipinitialspace=True,
                              #engine="python",
                              engine="c", # c engine faster than python engine
                              )
    #except:
    #    print("file {} not available".format(prn_path))
    #    pass

    lines_df_read = len(df_read)

    #print(df_read)
    #display(df_read)
    #print(df_read.columns)

    # delete "unnamed" and first column name "#" from header
    list_col_names = [x for x in df_read.columns if ("Unnamed" not in x) if (x != "#")]
    #print(list_col_names)

    #display()

    # drop empty columns at the end of df. by how="all" only last column with all nan values is deleted. other columns might contain single nan values
    #df_read = df_read.dropna(how="all", axis=1)
    df_read = df_read.iloc[:, 0:len(list_col_names)].copy()
    #print(df_read)
    #print(df_read.sum())
    df_read = df_read.set_axis(list_col_names, axis=1)#.set_index("time").rename_axis(None)
    #display(df_read)

    # set new column names
    #df_read.columns = list_col_names

    # set index to time column and delete index name for diagrams
    df_read = df_read.set_index("time").rename_axis(None).dropna(how="all")
    #df_read.index.name = None

    # drop "order" column
    if "order" in df_read:
        df_read = df_read.drop(labels="order", axis=1)

    # remove duplicates
    df_read = df_read[~df_read.index.duplicated()]

    # take only given variables
    if read_variables not in [[], [""], [''], 0, "", '', None]:
        #print("read_variables: ", read_variables)
        try:
            df_read = df_read[read_variables]
            all_variables = "Like selection"
        except:
            all_variables = "Selection not available. All selected."
            #print("Selected variables are not in prn-file '{}'. All available variables are selected.".format(pathlib.Path(prn_path).name))
    else:
        all_variables = "None. All selected."

    time_import = round((time() - time_import_start), 2)

    #display(df_read)

    # resample if demanded
    if resample_to_frequency_method != None:
        time_resample_start = time()

        df_read = func_resample_df_to_frequency(df_read,
                                                method=resample_to_frequency_method,
                                                frequency=resample_to_frequency,
                                                )
        time_resample = round((time() - time_resample_start), 2)
    else:
        time_resample = "no resampling"

    #print("df_read: {}".format(df_read))
    #display(df_read)

    if set_datetime_index and not isinstance(df_read.index, pd.DatetimeIndex):
        time_datetime_start = time()

        #if None not in (resample_to_frequency_number, resample_to_frequency_unit):
        #    number = int(resample_to_frequency_number)
        #    unit = resample_to_frequency_unit
        #else:
        #    number = 1
        #    unit = "H"
        df_read.index = pd.Timestamp('{}-01-01'.format(start_year)) + pd.to_timedelta(df_read.index.to_series(), unit="H")#.multiply(number)
        #display(df_read)

        # resample to given frequency by "nearest" because by conversion to datetime index rounding errors might occur
        # this is applied to data which is already resampled. So no additional resampling is applied.
        # this serves only for eliminating rounding errors.
        if resample_to_frequency_method != None:
            df_read = df_read.resample("{}".format(resample_to_frequency), label="right", closed="right").nearest()

        time_datetime = round((time() - time_datetime_start), 2)
    else:
        time_datetime = "no datetime index"

    ser_time_metrics = pd.Series(data=[lines_df_read, time_import, time_resample, time_datetime, all_variables],
                                 index=["Number of lines", "Time import [sec]", "Time resampling (method: '{}') [sec]".format(resample_to_frequency_method), "Time datetime index [sec]", "Variable selection"],
                                 name=pathlib.Path(prn_path).name,
                                 )
    #print("time for resampling of {} with method '{}': {} s".format(pathlib.Path(prn_path).name, resample_to_frequency_method, round((time()-time_resample), 2)))

    return df_read, ser_time_metrics

def func_read_ida_prn_versions_to_multiindex_df(
        folder_path,
        sep,
        start_year,
        list_version_names_to_read,
        list_level_names_to_read=[],
        output_files_and_variables_to_read=[],
        resample_to_frequency_method=None,
        resample_to_frequency=None,
        set_datetime_index=True,
        simulation_type="energy",
):


    # if no output files are given, select default ones
    list_default = [
            "AMBIENT_WIND",
            "BLDCTRL",
            "BUILDING-OCCUPANCY",
            "OUTPUT-FILE",
            # OUTPUT-FILE_ach,
            # OUTPUT-FILE_air_flow,
            # OUTPUT-FILE_panel_opening_ctrl,
            # OUTPUT-FILE_test,
            "PLANT_POWER",
            "REPORT-AUX",]
    list_default_prn = ["{}.prn".format(x) for x in list_default
        ]
    if output_files_and_variables_to_read == []:
        index = pd.MultiIndex.from_arrays((list_default, ["global" for x in range(len(list_default))]), names=["output_file", "level"])
        #print(index)
        ser_output_files_and_variables_to_read = pd.Series(data=[[] for x in range(len(list_default))], index=index)
    # else check if all variables should be read or only selected ones
    else:
        ser_output_files_and_variables_to_read = pd.DataFrame.from_dict(output_files_and_variables_to_read).stack().rename_axis(["output_file", "level"])#.rename("variables").to_frame()

    #display(ser_output_files_and_variables_to_read)

    # empty list for later concat
    list_df = []

    # empty list for time metrics of import
    list_time_import = []

    # loop over selected version names
    for version_name in list_version_names_to_read:
        #print("version_name: ", version_name)

        path_folder_version_name = os.path.join(folder_path, version_name)
        #print("path_folder_version_name: ", path_folder_version_name)

        # empty list for later concat
        list_df_version = []

        # loop over rows in series
        for idx, variables in ser_output_files_and_variables_to_read.iteritems():
            output_file, level = idx
            #print(variables)

            if simulation_type == "energy":
                if level == "global":
                    prn_path = os.path.join(path_folder_version_name, "energy", output_file + ".prn")
                else:
                    prn_path = os.path.join(path_folder_version_name, "energy", "{}.{}.prn".format(level, output_file))
                #print(prn_path)

            elif simulation_type == "custom":

                if level == "global":
                    prn_path = os.path.join(path_folder_version_name, output_file + ".prn")
                else:
                    prn_path = os.path.join(path_folder_version_name, level, output_file + ".prn")


            try:
                df_file, ser_time_metrics_file = func_read_ida_prn_to_df(prn_path=prn_path,
                                                                     sep=sep,
                                                                         start_year=start_year,
                                                                     read_variables=variables,
                                                                     resample_to_frequency=resample_to_frequency,
                                                                     resample_to_frequency_method=resample_to_frequency_method,
                                                                     set_datetime_index=set_datetime_index,
                                                                     )

            except FileNotFoundError as not_found:
                print("file not_found: {}".format(not_found.filename))
                continue
            #display(df_file)

            # create multiindex
            df_file.columns = pd.MultiIndex.from_product([[version_name], [level], [output_file], df_file.columns], names=["version", "level", "output-file", "variable"])
            #print(df_file)

            # set multiindex name for time metrics dataframe
            ser_time_metrics_file.name = (version_name, ser_time_metrics_file.name, level)

            list_df_version.append(df_file)
            list_time_import.append(ser_time_metrics_file)



        # concat list of dataframes in one dataframe per version
        df_version = pd.concat(list_df_version, axis=1)

        # sort columns
        df_version = df_version.sort_index(axis=1)

        list_df.append(df_version)

    # create and display dataframe for import metrics
    #print(list_time_import)
    df_time_metrics = pd.DataFrame(list_time_import).sort_index() #.rename_axis(["Version name", "Output-file"])
    #display(df_time_metrics)

    # if dataframes are not resampled, put them all in a series
    if resample_to_frequency_method == None:
        df = pd.Series(list_df, index=list_version_names_to_read)
        print("Attention: Version dataframes are collected in a pandas series.")
    # if dataframes are resampled, put them all in a common dataframe
    else:
        df = pd.concat(list_df, axis=1)

        # sort columns. better not.
        #df = df.sort_index(axis=1)

    return df, df_time_metrics



def func_export_df_to_ida_prn(df, filepath_export, header=True, prepend_suffix=True):

    # make a copy of original df
    df_return = df.copy()

    # check for nan values
    ser_with_nan_values = df_return.isna().sum()
    #print(ser_with_nan_values)

    ## interpolate nan values by index
    if ser_with_nan_values.sum() != 0:
        columns_with_nan_values = df_return.columns[df_return.isna().any()]
        print("NaN values in columns {} are interpolated".format(columns_with_nan_values))
        df_return = df_return.interpolate(method="index", axis=0)

    ## fillna nan at begin and end of columns
    df_return = df_return.fillna(method="bfill").fillna(method="ffill")

    ## drop columns with only nan values
    df_return = df_return.dropna(axis=1)

    # flatten multiindex.
    if isinstance(df_return.columns, pd.MultiIndex):
        df_return.columns = ['_'.join(col).strip() for col in df_return.columns.to_frame().fillna("nan").values]


    # prepend underline and strings
    if prepend_suffix:
        cols = df_return.columns
        df_return.columns = ["_{}_{}".format(str(integer).zfill(len(str(len(cols)))), aks) for integer, aks in zip(range(len(cols)), cols)]



    # replace dots. "." is not allowed.
    df_return.columns = df_return.columns.str.replace(".", "_", regex=False)

    # check if index is datetime (then convert to fraction of hours) or not
    if isinstance(df_return.index, pd.DatetimeIndex):
        # get minimum of old index
        hour_of_year_min = (df_return.index.min().dayofyear - 1) * 24 + df_return.index.min().hour
        index_min = df_return.index.min()

        # create new index as fraction of hours starting at 0
        index_new = hour_of_year_min + (df_return.index - index_min) / pd.Timedelta("1 hour")
    else:
        index_new = df_return.index

    ## insert new index "time" as column
    #df_return.insert(0, "time", index_new)

    df_return.index = index_new
    df_return.rename_axis("time", inplace=True)

    # index has to start with 0 (zero). Otherwise numerical error in IDA. create if not exists
    if df_return.index.min != 0:
        #print(1)
        df_return.loc[0] = df_return.loc[df_return.index.min()].copy()
        df_return.sort_index(inplace=True)

    df_return = df_return.reset_index()

    # insert new empty first column with header "#"
    df_return.insert(0, "#", np.nan)

    # write prn file
    ## tabulator as separator. don't write index (index=False) because new index is in column "time"
    ## line_terminator \r\n (with carriage return). otherwise import in ida ice doesn't work.
    df_return.to_csv(filepath_export, sep="\t", index=False, line_terminator="\r\n", header=header)

    return df_return



def func_convert_epw_to_ida_prn(path_file):

    file_export = path_file.replace(".epw", "_epw.prn")

    df_epw = func_read_epw(path_file)

    df_epw = df_epw.reset_index(drop=True)

    df_return = func_export_df_to_ida_prn(df_epw, file=file_export)

    return df_return
