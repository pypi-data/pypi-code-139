import unittest

from pytest_ver import pth

from gui_api_tkinter.lib import version
from gui_api_tkinter.lib.harness.gui_api_harness import GuiApiHarness
from ver.helpers import services
from ver.helpers.helper import Helper
from ver.helpers.logger_mock import Logger


# -------------------
class TestTp006(unittest.TestCase):
    page1 = None
    logger = None
    helper = None
    th = None

    # --------------------
    @classmethod
    def setUpClass(cls):
        pth.init()

        services.th = GuiApiHarness()
        services.th.init()
        services.logger = Logger()
        services.helper = Helper()

    # -------------------
    def setUp(self):
        print('')

    # -------------------
    def tearDown(self):
        services.helper.kill_process()
        self.assertFalse(services.helper.gui_process.is_alive())

        # uncomment for debugging
        # print(f'DBG {services.logger.lines}')

    # --------------------
    @classmethod
    def tearDownClass(cls):
        services.th.term()
        pth.term()

    # --------------------
    # @pytest.mark.skip(reason='skip')
    def test_tp006(self):
        pth.proto.protocol('tp-006', 'check information for various widgets')
        pth.proto.add_objective('check informaion for root window is accurate')
        pth.proto.add_objective('check informaion for Frame widgets is accurate')
        pth.proto.add_objective('check informaion for Button widgets is accurate')
        pth.proto.add_objective('check informaion for Label widgets is accurate')
        pth.proto.add_objective('check informaion for Entry widgets is accurate')
        pth.proto.add_objective('check informaion for Radiobutton widgets is accurate')
        pth.proto.add_precondition('do_install has been run')
        pth.proto.add_precondition('latest versions of all modules have been retrieved')
        pth.proto.set_dut_version(f'v{version.version}')

        pth.proto.step('start gui')
        services.helper.start_process()
        pth.ver.verify_true(services.helper.gui_process.is_alive())
        pth.ver.verify_false(services.th.is_connected(), reqids=['SRS-009', 'SRS-030'])

        pth.proto.step('connect harness to GUI App server')
        services.th.connect()
        pth.ver.verify_true(services.th.is_connected(), reqids=['SRS-001', 'SRS-009'])

        pth.proto.step('get page content')
        services.th.get_screen()
        pth.ver.verify_gt(len(services.th.content), 0, reqids=['SRS-006', 'SRS-032', 'SRS-033'])

        # uncomment for debug
        # print(f'DBG {json.dumps(services.th.content, indent=4)}')

        pth.proto.step('check window information')
        item = services.th.search(['window1'])
        pth.ver.verify_equal('Tk', item['class'], reqids='SRS-040')
        pth.ver.verify_equal('window1', item['name'], reqids=['SRS-041', 'SRS-027'])
        pth.ver.verify_equal('Ver Version: Ver v1.2.3', item['title'], reqids='SRS-041')
        pth.ver.verify_equal('300x200+0+0', item['geometry'], reqids='SRS-041')

        pth.proto.step('check frame information')
        item = services.th.search(['window1', 'page1_frame'])
        pth.ver.verify_equal('Frame', item['class'], reqids='SRS-040')
        pth.ver.verify_equal('page1_frame', item['name'], reqids=['SRS-042', 'SRS-029'])
        pth.ver.verify_equal('<unknown>', item['value'], reqids='SRS-042')
        pth.ver.verify_equal('<unknown>', item['state'], reqids='SRS-042')

        pth.proto.step('check button information')
        item = services.th.search(['window1', 'page1_frame', 'button_frame', 'button1'])
        pth.ver.verify_equal('Button', item['class'], reqids='SRS-040')
        pth.ver.verify_equal('button1', item['name'], reqids=['SRS-043', 'SRS-029'])
        pth.ver.verify_equal('press me!', item['value'], reqids='SRS-043')
        pth.ver.verify_equal('normal', item['state'], reqids='SRS-043')

        pth.proto.step('check label information')
        item = services.th.search(['window1', 'page1_frame', 'button_frame', 'label1'])
        pth.ver.verify_equal('Label', item['class'], reqids='SRS-040')
        pth.ver.verify_equal('label1', item['name'], reqids=['SRS-044', 'SRS-029'])
        pth.ver.verify_equal('state: 0', item['value'], reqids='SRS-044')
        pth.ver.verify_equal('normal', item['state'], reqids='SRS-044')

        pth.proto.step('check entry information')
        item = services.th.search(['window1', 'page1_frame', 'button_frame', 'entry1'])
        pth.ver.verify_equal('Entry', item['class'], reqids='SRS-040')
        pth.ver.verify_equal('entry1', item['name'], reqids=['SRS-047', 'SRS-029'])
        pth.ver.verify_equal('', item['value'], reqids='SRS-047')
        pth.ver.verify_equal('normal', item['state'], reqids='SRS-047')

        pth.proto.step('check radiobutton information')
        item = services.th.search(['window1', 'page1_frame', 'button_frame', 'rb1'])
        pth.ver.verify_equal('Radiobutton', item['class'], reqids='SRS-040')
        pth.ver.verify_equal('rb1', item['name'], reqids=['SRS-047', 'SRS-029'])
        pth.ver.verify_equal('option1', item['value'], reqids='SRS-047')
        pth.ver.verify_equal('normal', item['state'], reqids='SRS-047')
