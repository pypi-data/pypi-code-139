from teradataml.analytics.json_parser.json_store import _JsonStore
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messagecodes import MessageCodes
from teradataml.common.messages import Messages
from teradataml.context.context import get_connection
from teradataml.utils.validators import _Validators
from teradataml.common.constants import ValibConstants
from teradataml.common.utils import UtilFuncs


def display_analytic_functions(type=None, name=None):
    """
    DESCRIPTION:
        Display list of analytic functions available to use on the Teradata Vantage system, user is connected to.

    PARAMETERS:
        type:
            Optional Argument.
            Specifies the type(s) of functions to list down.
            Permitted Values: "BYOM", "TABLE OPERATOR", "SQLE", "VAL"
            Types: str or list of str(s)

        name:
            Optional Argument.
            Specifies the search string for function name. When this argument 
            is used, all functions matching the name are listed.
            Types: str or list of str(s)

    RETURNS:
        None

    RAISES:
        TeradataMlException.

    EXAMPLES:
        >>> from teradataml import create_context, display_analytic_functions

        # Example 1: Displaying a list of available analytic functions
        >>> connection_name = create_context(host = host, username=user, password=password)
        >>> display_analytic_functions()

            List of available functions:
                Analytics Database Functions:
                    * PATH AND PATTERN ANALYSIS functions:
                         1. Attribution
                         2. nPath
                         3. Sessionize
                         .
                         .
                         .
                         5. VectorDistance
                    * FEATURE ENGINEERING UTILITY functions:
                         1. FillRowId
                         2. NumApply
                         3. RoundColumns
                         4. StrApply
                TABLE OPERATOR Functions:
                     1. ReadNOS
                     2. WriteNOS
                BYOM Functions:
                     1. H2OPredict
                     2. ONNXPredict
                     3. PMMLPredict
                Vantage Analytic Library (VAL) Functions:
                    * DESCRIPTIVE STATISTICS functions:
                         1. AdaptiveHistogram
                         2. Explore
                         3. Frequency
             ...

         # Example 2: When no analytic functions are available on the cluster.
         >>> display_analytic_functions(name="invalid")

            No analytic functions available with connected Teradata Vantage system with provided filters.

         # Example 3: List all available SQLE analytic functions.
         >>> display_analytic_functions(type="SQLE")

            List of available functions:
                Analytics Database Functions:
                    * PATH AND PATTERN ANALYSIS functions:
                         1. Attribution
                         2. nPath
                         3. Sessionize
                    * MODEL SCORING functions:
                         1. DecisionForestPredict
                         2. DecisionTreePredict
                         3. GLMPredict
                         4. KMeansPredict
                         .
                         .
                         .
                         4. KNN
                         5. VectorDistance
                    * FEATURE ENGINEERING UTILITY functions:
                         1. FillRowId
                         2. NumApply
                         3. RoundColumns
                         4. StrApply
          ...

         # Example 4: List all functions with function name containing string "fit".
         >>> display_analytic_functions(name="fit")

            List of available functions:
                Analytics Database Functions:
                    * FEATURE ENGINEERING TRANSFORM functions:
                         1. BincodeFit
                         2. Fit
                         3. NonLinearCombineFit
                         4. OneHotEncodingFit
                         5. OrdinalEncodingFit
                         6. PolynomialFeaturesFit
                         7. RandomProjectionFit
                         8. RowNormalizeFit
                         9. ScaleFit
                         10. SimpleImputeFit
                    * DATA CLEANING functions:
                         1. OutlierFilterFit

         # Example 5: List all SQLE functions with function name containing string "fit".
         >>> display_analytic_functions(type="SQLE", name="fit")

            List of available functions:
                Analytics Database Functions:
                    * FEATURE ENGINEERING TRANSFORM functions:
                         1. BincodeFit
                         2. Fit
                         3. NonLinearCombineFit
                         4. OneHotEncodingFit
                         5. OrdinalEncodingFit
                         6. PolynomialFeaturesFit
                         7. RandomProjectionFit
                         8. RowNormalizeFit
                         9. ScaleFit
                         10. SimpleImputeFit
                    * DATA CLEANING functions:
                         1. OutlierFilterFit


         # Example 6: List all functions of type "TABLE OPERATOR" and "SQLE" containing "fit" and "nos".
         >>> display_analytic_functions(type=["SQLE", "TABLE OPERATOR"], name=["fit", "nos"])

            List of available functions:
                Analytics Database Functions:
                    * FEATURE ENGINEERING TRANSFORM functions:
                         1. BincodeFit
                         2. Fit
                         3. NonLinearCombineFit
                         4. OneHotEncodingFit
                         5. OrdinalEncodingFit
                         6. PolynomialFeaturesFit
                         7. RandomProjectionFit
                         8. RowNormalizeFit
                         9. ScaleFit
                         10. SimpleImputeFit
                    * DATA CLEANING functions:
                         1. OutlierFilterFit
                TABLE OPERATOR Functions:
                     1. ReadNOS
                     2. WriteNOS

    """
    # Argument validation.
    validator = _Validators()
    arg_info_matrix = []

    arg_info_matrix.append(["name", name, True, (str, list)])
    arg_info_matrix.append(["type", type, True, (str, list), False,
                            ["SQLE", "TABLE OPERATOR", "BYOM", "VAL"]])

    validator._validate_function_arguments(arg_info_matrix)

    if get_connection() is None:
        error_code = MessageCodes.INVALID_CONTEXT_CONNECTION
        error_msg = Messages.get_message(error_code)
        raise TeradataMlException(error_msg, error_code)

    func_type_category_name_dict = _JsonStore._get_func_type_category_name_dict()

    # Add entry for VAL functions in func_type_category_name_dict.
    func_type_category_name_dict["VAL"] = ValibConstants.CATEGORY_VAL_FUNCS_MAP.value

    _display_functions(func_type_category_name_dict, type, name)


def _display_functions(func_type_category_name_dict, func_types=None, search_keywords=None):
    """
    Function to display the available functions.
    Functions are filtered based on function_type and function_filter, if provided.

    PARAMETERS:
        func_type_category_name_dict:
            Required Argument.
            Specifies the dictionary with key as function name and 
            value as function metadata.
            Types: dict

        func_types:
            Optional Argument.
            Specifies the type of function.
            Types: str

        search_keywords:
            Optional Argument.
            Specifies the filter for function.
            Types: str

    RETURNS:
        None

    RAISES:
        None

    EXAMPLES:
        _display_functions(func_type_category_name_dict = {'WhichMin':
                                    <teradataml.analytics.json_parser.metadata._AnlyFuncMetadata object at 0x7f2918084ac8>,
                          type = "SQLE", name="min")

    """

    # Store a flag to decide whether to print header or not.
    list_header_printed = False

    # If type is not specified, print functions under all types.
    if func_types is None:
        func_types = list(func_type_category_name_dict.keys())

    # Check for type of 'type'. If str, convert it to list.
    func_types = UtilFuncs._as_list(func_types)

    # Map to store function types and corresponding type to be printed.
    func_type_display_type_map = {"SQLE": "Analytics Database",
                                  "VAL": "Vantage Analytic Library (VAL)",
                                  "UAF": "Unbounded Array Framework (UAF)"}

    # Template for function type header.
    type_header = "\n\t{} Functions:"

    # Iterate over all function types one by one and print the corresponding functions.
    for func_type in func_types:
        type_header_printed = False
        funcs = func_type_category_name_dict.get(func_type)
        if isinstance(funcs, dict):
            # For function types having function categories,
            # get list of all functions under all categories.
            for func_cat, func_list in funcs.items():
                func_list = _get_filtered_list(func_list, search_keywords)
                if len(func_list) > 0:
                    if not list_header_printed:
                        print("\nList of available functions:")
                        list_header_printed = True
                    if not type_header_printed:
                        print(type_header.format(func_type_display_type_map.get(func_type, func_type)))
                        type_header_printed = True
                    _print_indexed_list(func_name_list=func_list,
                                        margin="\t\t\t",
                                        header="\t\t* {} functions:".format(func_cat.upper()))

        elif isinstance(funcs, list):
            func_list = _get_filtered_list(funcs, search_keywords)
            if len(func_list) > 0:
                if not list_header_printed:
                    print("\nList of available functions:")
                    list_header_printed = True
                _print_indexed_list(func_name_list=func_list,
                                    margin="\t\t",
                                    header=type_header.format(func_type_display_type_map.get(func_type, func_type)))

    if not list_header_printed:
        print("No analytic functions available with connected Teradata Vantage system with provided filters.")


def _get_filtered_list(name_list, search_keywords=None):
    """
    Function to filter out the names of functions which contain search_keywords in their names.

    PARAMETERS:
        name_list:
            Required Argument.
            Specifies the list of function names.
            Types: List of str(s)

        search_keywords:
            Optional Argument.
            Specifies the filter for the function.
            Types: str or list of str(s)

    RETURNS:
        list

    RAISES:
        None

    EXAMPLES:
        _get_filtered_list("SQLE", ["WhichMin", "Fit"], ["fit", "min"])

    """

    # If search_keyword is specified.
    if search_keywords is not None:
        func_name_list = []

        # Check for type of search_keywords. If str, convert it to list.
        search_keywords = UtilFuncs._as_list(search_keywords)

        # Filter one by one and return list of filtered functions.
        for search_keyword in search_keywords:
            filtered_func_list = [func for func in name_list if search_keyword.lower() in func.lower()]
            func_name_list.extend(filtered_func_list)

        return func_name_list

    # Return all available functions to print.
    else:
        return name_list


def _print_indexed_list(func_name_list, margin, header):
    """
    Function to print a list with index, margin and header provided.

    PARAMETERS:
        func_name_list:
            Required Argument.
            Specifies the list of function names to print.
            Types: List of str(s)

        margin:
            Required Argument.
            Specifies the margin from home.
            Types: str

        header:
            Optional Argument.
            Specifies the header for list.
            Types: str

    RETURNS:
        None

    RAISES:
        None

    EXAMPLES:
        _print_indexed_list(["OutlierFilterFit","SimpleImputeFit"], "\t\t\t")

    """
    if header:
        print(header)
    functions = enumerate(sorted(func_name_list, key=lambda function_name: function_name.lower()), 1)
    for key, value in functions:
        print("{} {}. {}".format(margin, key, value))
