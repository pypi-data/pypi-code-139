import math


class StreamHeaderBaseData:

    def __init__(self):

        self.MULTI_RATE = "Multi Rate"
        self.SINGLE_RATE = "Single Rate"

        self.version=None
        self.average=None
        self.channels=None

        self.sampleModeString = self.SINGLE_RATE;
        self.devicePeriod = "";
        self.mainPeriod = "";

        self.devicePeriodInt=None

        self.samplePeriodInt=None

        self.xmlGroupList=None
        self.channelGroupList = []

        self.samplePeriods_nS = None
        self.samplePeriod_nS = 0;

    class Group :
        def __init__(self):
            self.deviceGroupId
            self.sortedGroupId
            self.channelCount
            self.sampleRateBase
            self.sampleRateExponent
            self.averagingRate


    class XMLGroupList :
        def __init__(self):
            self.groupList = []


    class ChannelGroup:
        def __init__(self):
            self.groupId = 0
            self.detailsFullList = []
            self.detailsDeviceEnabledList = None

        def setGroupToChannels(self):
            for cir in self.getDetailsFullList():
                cir.setDeviceGroupId(groupId)

        def getDetailsFullList(self):
            return self.detailsFullList;

        def setDetailsFullList(self, detailsFullList):
            self.detailsFullList = detailsFullList

        def getDetailsDeviceEnabledList(self):

            if not self.detailsDeviceEnabledList:
                self.detailsDeviceEnabledList = []

            for cir in self.detailsFullList:
                if cir.isDeviceEnabled():
                    self.detailsDeviceEnabledList.append(cir)

            return self.detailsDeviceEnabledList



    def getDevicePeriod(self):
        return self.devicePeriod

    def setDevicePeriod(self, devicePeriod):
        self.devicePeriod = devicePeriod
        s = self.devicePeriod[0, len(self.devicePeriod) - 2]
        self.setDevicePeriod(int(s))

    def getMainPeriod(self):
        return self.mainPeriod

    def setMainPeriod(self, mainPeriod):
        self.mainPeriod = mainPeriod;
        s = str(mainPeriod)[0, len(mainPeriod) - 2]
        self.samplePeriodInt = int(s)


    def postXMLInit( self ) :
        groupSamplePeriodList = None
        samplePeriod_uS = 0

        class GroupSamplePeriodEntry:
            def __init__(self):
                self.samplePeriod = None
                self.deviceGroupId = None
                self.group = None
                self.channelGroup = None

            def GroupSamplePeriodEntry(self, group, channelGroup, samplePeriod, deviceGroupId) :
                super();
                self.group = group;
                self.channelGroup = channelGroup;
                self.samplePeriod = samplePeriod;
                self.deviceGroupId = deviceGroupId;


        if xmlGroupList and self.xmlGroupList.groupList.size() > 0:

            groupSamplePeriodList = []
            samplePeriods_nS = [] # xmlGroupList.groupList.size()
            channelGroupIdxi = 0

            for group in self.xmlGroupList.groupList:
                freq = group.sampleRateBase * math.pow(10, group.sampleRateExponent)
                period_nS = 1000_000_000 / freqmultiTBase
                average =  math.pow(2, group.averagingRate)
                samplePeriodsnS = period_nS * average

                groupSamplePeriodList.append( GroupSamplePeriodEntry( group, self.channelGroupList.get( channelGroupIdxi ), samplePeriodsnS, group.deviceGroupId ) )
                samplePeriods_nS[group.deviceGroupId] = samplePeriodsnS
                channelGroupIdxi += 1

            unsorted = []
            newlist = sorted(groupSamplePeriodList, key=lambda x: x.samplePeriod)

            # Collections.sort( groupSamplePeriodList, new Comparator < GroupSamplePeriodEntry > (){	// multiTBase sort groups by ascending sample period
            #     @Override
            #     public int compare(GroupSamplePeriodEntry o1, GroupSamplePeriodEntry o2) {
            #         if ( o1.samplePeriod < o2.samplePeriod )
            #         return -1;
            #         if (o1.samplePeriod > o2.samplePeriod)
            #             return 1;
            #
            #         return 0;
            #     }} );

            for i in range(len(groupSamplePeriodList)):
                group2 = groupSamplePeriodList[i].group
                group2.sortedGroupId = i
                samplePeriods_nS[group.sortedGroupId] = groupSamplePeriodList[i].samplePeriod

            for i in range(len(self.xmlGroupList.groupList)):
                self.xmlGroupList.groupList[i] = groupSamplePeriodList[i].group
                self.channelGroupList[i] = groupSamplePeriodList[i].channelGroup


            for i in range(len(self.channelGroupList)):
                cg = self.channelGroupList[i]
                detailsList = cg.getDetailsFullList
                for item in detailsList:
                    item.setSortedGroupId(i)

            self.samplePeriod_nS = samplePeriods_nS[0]

        else:
            samplePeriod_uS = self.samplePeriodInt
            samplePeriod_nS = samplePeriod_uS * 1000

            for cg in self.channelGroupList:
                detailsList = cg.getDetailsFullList()
                for cir in detailsList:
                    cir.setDeviceGroupId(cg.groupId)
                    cir.setSortedGroupId(cg.groupId)


        for cg in self.channelGroupList:
            cg.setGroupToChannels()

            detailsList = cg.getDetailsFullList()

            for cir in detailsList:
                if self.samplePeriod_nS:
                    cir.postXMLInit(self.version, self.samplePeriods_nS[ cir.getSortedGroupId() ])
                else:
                    cir.postXMLInit(self.version, samplePeriod_uS)


    def initialise(self):
        self.channelGroupList.clear()
        x = ChannelGroup()
        self.channelGroupList.append(x)

    def detDetailsList(self, index):
        return self.channelGroupList[index].getDetailsFullList()

    def setDevicePeriod(self, samplePeriod):
        self.devicePeriodInt = samplePeriod

    def isMultiRate(self):
        return self.sampleModeString == self.MULTI_RATE


