class streamHeader:

    def __init__(self):

        self.sortedGroupId = 0;
        self.sampleModeString = SINGLE_RATE; # multiTBase, this is tracked here and in StreamHeaderBaseData, not ideal

        self.data = StreamHeaderBaseData()

        self.dataGroups = [] # ArrayList < StreamDataGroup_V2 > ();
        self.origHeader = [] # ArrayList < String > (); # very useful debug
        self.isValid = false

        self.indexFileNames = [] # ArrayList < String > (); // track index file names where necessary

    def addDataGroup(self, StreamDataGroup_V2, dataGroup ) :
        getDataGroups().add(dataGroup)

    def setSamplePeriod_uS(self, samplePeriod) :
        self.data.samplePeriodInt = samplePeriod

    def getSamplePeriod_uS(self):
        self.data.samplePeriodInt

    def getSamplePeriod_nS(self):
        return self.data.channelGroupList.get(0).getDetailsFullList().get(0).getSampleTime_nS()

    def getSamplePeriod_mS(self):
        return int(self.getSamplePeriod_nS() / 1000_000)

    def getVersion(self):
        return self.data.version

    def setVersion(self, version):
        self.data.version = version

    def getAverage():
        return data.average

    def setAverage(self, average):
        self.data.average = average;

    def getLegacyChannels(self):
        return self.data.channels

    def setLegacyChannels(self, channels):
        self.data.channels = channels;

    def isMultiRate(self):
        return self.data.isMultiRate()

    def getDataGroups(self):
        return self.dataGroups

    def setDataGroups(self, dataGroups):
        self.dataGroups = dataGroups

    def getChannelGroupCount(self):
        return self.data.channelGroupList.size()

    def getDetailsList(self, groupId):
        return self.data.channelGroupList.get(groupId).getDetailsDeviceEnabledList()

    def getDetailsList(self):
        return getDetailsList(0)

    def getAllDetailsList(self):
        retVal = [] # ArrayList < ChannelInfoRecord > ();
        for i in range(self.data.channelGroupList.size()):
            retVal.append( self.data.channelGroupList.get(i).getDetailsDeviceEnabledList() )

        return retVal

    def getGroupList(self):
        return self.data.channelGroupList

    def getDevicePeriod(self):

        return self.data.getDevicePeriod()

    def getMainPeriod(self):
        return data.getMainPeriod()

    def initialiseHeader(self):
        self.data.initialise()

    def initFromDataGroups(self):
        if (self.getDataGroups().size() == 0):
            return

        firstDataGroup = self.getDataGroups().get(0)
        self.data.setDevicePeriod( int(firstDataGroup.samplePeriod) )

        self.data.initFromDataGroups(getDataGroups());
