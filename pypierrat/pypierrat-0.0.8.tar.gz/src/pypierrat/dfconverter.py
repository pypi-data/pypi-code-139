import pandas as pd

class DfConverter:
    # Constructor
    def __init__(self):
        return
    
    # Methods
    def JsonRecordsToColumns(self, dataframe, columns=[], inplace=False, drop=False):
        '''
        Converts a dataframe with json records to a dataframe with columns.
        
        Parameters: 
            dataframe (pandas.DataFrame): Dataframe with json records
            columns (str, list<str>): Columns of type dict
            inplace (bool): If True, the dataframe is modified in place
            drop (bool): If True, the json records are dropped
        '''
        
        # CHECK 
        if (not isinstance(dataframe, pd.DataFrame)):
            raise TypeError
        if not ((isinstance(columns, list)) or (isinstance(columns, str))):
            raise TypeError
        if (not isinstance(inplace, bool)):
            raise TypeError
        if (not isinstance(drop, bool)):
            raise TypeError
        
        # INIT
        # Set columns
        if isinstance(columns, list):
            if (len(columns) == 0):
                columns = dataframe.columns.to_list()
        else:
            columns = [columns]
        
        # Init dataframe with inplace
        if not inplace:
            dataframe = dataframe.copy()
            
        # PROCESS
        # For each columns
        for c in columns:
            # Extract data
            data = dataframe[c].to_list()
            # Put in new dataframe
            ndf = pd.DataFrame(data)
            # for each new columns
            for nc in ndf.columns.to_list():
                if type(ndf[nc][0]) == dict:
                    ndf = self.JsonRecordsToColumns(ndf, columns=nc, drop=True)
            # Prefix to columns
            ndf = ndf.add_prefix(c + '.')
            # Concat dataframe
            dataframe = pd.concat([dataframe, ndf], axis=1)
            # Drop column
            if drop:
                dataframe.drop(c, axis=1, inplace=True)
        
        # RETURN DF
        return dataframe
    