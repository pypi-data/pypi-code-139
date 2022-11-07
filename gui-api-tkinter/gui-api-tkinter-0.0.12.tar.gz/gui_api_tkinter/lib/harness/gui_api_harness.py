import time

from .client import Client
from .. import services
from ..cfg import Cfg
from ..logger_null import LoggerNull


# --------------------
## test harness used to communicate with GuiApi Server
class GuiApiHarness:
    # --------------------
    ## constructor
    def __init__(self):
        ## holds reference to common configuration information
        self.cfg = None
        ## holds reference to logger object
        self.logger = None
        ## holds current screen content
        self._content = None
        ## holds reference to the socket client
        self._client = None

    # --------------------
    ## initialize
    #
    # @param logger   (optional) a reference to a logger object
    # @return None
    def init(self, logger=None):
        self.cfg = Cfg()
        services.cfg = self.cfg
        if logger is None:
            self.logger = LoggerNull()
        else:
            self.logger = logger
        services.logger = self.logger

        services.cfg.init()
        self._client = Client()

    # --------------------
    ## terminate
    #
    # @return None
    def term(self):
        if self._client is not None:
            self._client.term()
            self._client = None

    # --------------------
    ## connect to the GUI API server running inside the GUI
    #
    # @return False
    def connect(self):
        ok = False
        if self.is_connected():
            self.logger.info(f'connect(): already connected, ignoring')
        else:
            self._client.init()
            time.sleep(0.5)
            ok = True

        return ok

    # --------------------
    ## check if connected to the server
    #
    # @return True if connected, False otherwise
    def is_connected(self):
        if self._client is None:
            return False

        return self._client.is_connected()

    # --------------------
    ## send a command and wait for a response
    #
    # @param cmd  the command to send
    # @return the response
    def send_recv(self, cmd: dict) -> dict:
        return self._client.send_recv(cmd)

    # --------------------
    ## get the current screen contents in JSON format
    #
    # @return screen content in JSON format
    def get_screen(self) -> list:
        screen = self._client.get_screen()
        # currently can only handle 1 root window,
        # therefore content is a list of one item
        self._content = [screen]
        return self._content

    # --------------------
    ## the current screen contents in JSON format
    #
    # @return the current screen contents in JSON format
    @property
    def content(self) -> dict:
        return self._content

    # --------------------
    ## find the widget matching the path given in the search list
    #
    # @param search_path  a list of widget names
    # @return the widget item if found, None otherwise
    def search(self, search_path: list):
        tag = 'search'
        ack_nak = self._check_init(tag)
        err_msg = 'content'
        if self._check_is_none(ack_nak, self._content, err_msg): return ack_nak

        err_msg = 'search path'
        if self._check_is_none(ack_nak, search_path, err_msg): return ack_nak
        if self._check_is_empty(ack_nak, search_path, err_msg): return ack_nak

        item = self._search_content(self._content, search_path, 0)
        if self._check_is_not_found(ack_nak, item, err_msg): return ack_nak

        # it was found, no errors
        return item

    # --------------------
    ## recursive function to find the widget item that matches the search list
    #
    # @param content      the screen content to search
    # @param search_path  the list of widget names to search
    # @param index        the current entry in the search_list
    # @return the widget item if matches the last entry in search_list, None otherwise
    def _search_content(self, content, search_path, index=0):
        if content is None or \
                search_path is None or \
                len(search_path) == 0:
            return None

        # uncomment to debug
        # self.logger.info(f'DBG searching index={index} srch={search_path}')
        search_name = search_path[index]
        for item in content:
            if item['name'] == search_name:
                if index == len(search_path) - 1:
                    # uncomment to debug
                    # self.logger.info(f'DBG found it  index={index} node={item}')
                    return item

                # it matched, but not at the end of the search list, so check the children
                # uncomment to debug
                # self.logger.info(f'DBG children  index={index} srch={search_name} curr={item["name"]}')
                node = self._search_content(item['children'], search_path, index + 1)
                if node is not None:
                    return node

        # uncoment to debug
        # self.logger.info(f'DBG not_found index={index} {search_name}')
        return None

    # --------------------
    ## click left mouse button at given screen coordinates
    #
    # @param x   the x value in screen coordinates
    # @param y   the y value in screen coordinates
    # @return ack_nak response
    def click_left_at(self, x: int, y: int):
        tag = 'click_left_at'
        ack_nak = self._check_init(tag)

        err_msg = 'click'
        if self._check_is_not_int(ack_nak, x, 'x', err_msg): return ack_nak
        if self._check_is_not_int(ack_nak, y, 'y', err_msg): return ack_nak

        ack_nak = self._client.click_left(x, y)
        if self._check_reset_tag(tag, ack_nak): return ack_nak

        return self._check_ack(tag)

    # --------------------
    ## click the left mouse button on the given widget item
    #
    # @param item  the widget item to click on
    # @return ack_nak response
    def click_left_on(self, item: dict):
        tag = 'click_left_on'
        ack_nak = self._check_init(tag)

        err_msg = 'click item'
        if self._check_is_none(ack_nak, item, err_msg): return ack_nak
        if self._check_missing_coord(ack_nak, item, err_msg): return ack_nak

        x = int((item['coordinates']['x1'] + item['coordinates']['x2']) / 2)
        y = int((item['coordinates']['y1'] + item['coordinates']['y2']) / 2)
        ack_nak = self.click_left_at(x, y)
        if self._check_reset_tag(tag, ack_nak): return ack_nak

        return self._check_ack(tag)

    # --------------------
    ## click the left mouse button on the widget at the given search list
    #
    # @param click_path  the path to the widget
    # @return ack_nak response
    def click_left(self, click_path: list):
        tag = 'click_left'
        ack_nak = self._check_init(tag)

        err_msg = 'click path'
        if self._check_is_none(ack_nak, click_path, err_msg): return ack_nak
        if self._check_is_empty(ack_nak, click_path, err_msg): return ack_nak

        item = self.search(click_path)
        if self._check_reset_tag(tag, item): return item

        ack_nak = self.click_left_on(item)
        if self._check_reset_tag(tag, ack_nak): return ack_nak

        return self._check_ack(tag)

    # --------------------
    ## select the menu item at the given menu path
    #
    # @param menu_path   the list of menu indicies to search
    # @return ack_nak response
    def menu_click(self, menu_path: list):
        tag = 'menu_click'
        ack_nak = self._check_init(tag)

        err_msg = 'menu path'
        if self._check_is_none(ack_nak, menu_path, err_msg): return ack_nak
        if self._check_is_empty(ack_nak, menu_path, err_msg): return ack_nak

        ack_nak = self._client.menu_click(menu_path)

        return ack_nak

    # --------------------
    ## set text in widget at given screen coordinates
    #
    # @param x    the x value in screen coordinates
    # @param y    the y value in screen coordinates
    # @param msg  the text to set
    # @return ack_nak response
    def set_text_at(self, x: int, y: int, msg: str):
        tag = 'set_text_at'
        ack_nak = self._check_init(tag)

        err_msg = 'set text msg'
        if self._check_is_none(ack_nak, msg, err_msg): return ack_nak
        if self._check_is_empty(ack_nak, msg, err_msg): return ack_nak

        err_msg = 'set text'
        if self._check_is_not_int(ack_nak, x, 'x', err_msg): return ack_nak
        if self._check_is_not_int(ack_nak, y, 'y', err_msg): return ack_nak

        ack_nak = self._client.set_text(x, y, msg)
        if self._check_reset_tag(tag, ack_nak): return ack_nak

        return self._check_ack(tag)

    # --------------------
    ## set text on the given item
    #
    # @param item  the widget item to set the text on
    # @param msg   the text to set
    # @return ack_nak response
    def set_text_on(self, item: dict, msg: str):
        tag = 'set_text_on'
        ack_nak = self._check_init(tag)

        err_msg = 'set text msg'
        if self._check_is_none(ack_nak, msg, err_msg): return ack_nak
        if self._check_is_empty(ack_nak, msg, err_msg): return ack_nak

        err_msg = 'set text item'
        if self._check_is_none(ack_nak, item, err_msg): return ack_nak
        if self._check_missing_coord(ack_nak, item, err_msg): return ack_nak

        x = int((item['coordinates']['x1'] + item['coordinates']['x2']) / 2)
        y = int((item['coordinates']['y1'] + item['coordinates']['y2']) / 2)
        ack_nak = self.set_text_at(x, y, msg)
        if self._check_reset_tag(tag, ack_nak): return ack_nak

        return self._check_ack(tag)

    # --------------------
    ## set text on the widget at the given search list
    #
    # @param set_path  the path to the widget
    # @param msg       the text to set
    # @return ack_nak response
    def set_text(self, set_path: list, msg: str):
        tag = 'set_text'
        ack_nak = self._check_init(tag)

        err_msg = 'set text path'
        if self._check_is_none(ack_nak, set_path, err_msg): return ack_nak
        if self._check_is_empty(ack_nak, set_path, err_msg): return ack_nak

        err_msg = 'set text msg'
        if self._check_is_none(ack_nak, msg, err_msg): return ack_nak
        if self._check_is_empty(ack_nak, msg, err_msg): return ack_nak

        item = self.search(set_path)
        if self._check_reset_tag(tag, item): return item

        ack_nak = self.set_text_on(item, msg)
        if self._check_reset_tag(tag, ack_nak): return ack_nak

        return self._check_ack(tag)

    # --------------------
    def _check_init(self, tag):
        rsp = {
            'rsp': tag,
        }
        return rsp

    # --------------------
    def _check_is_none(self, ack_nak, val, err_msg):
        if val is None:
            ack_nak['value'] = 'nak'
            ack_nak['reason'] = f'{err_msg} is None'
            return True

        return False

    # --------------------
    def _check_is_empty(self, ack_nak, val, err_msg):
        if not val:
            ack_nak['value'] = 'nak'
            ack_nak['reason'] = f'{err_msg} is empty'
            return True

        return False

    # --------------------
    def _check_missing_coord(self, ack_nak, item, err_msg):
        if 'coordinates' not in item:
            ack_nak['value'] = 'nak'
            ack_nak['reason'] = f'{err_msg} missing coordinates values'
            return True

        return False

    # --------------------
    def _check_is_not_int(self, ack_nak, val, name, err_msg):
        if not isinstance(val, int):
            ack_nak['value'] = 'nak'
            ack_nak['reason'] = f'{err_msg} {name}-coordinate is not an integer'
            return True

        return False

    # --------------------
    def _check_is_not_found(self, ack_nak, item, err_msg):
        if item is None:
            ack_nak['value'] = 'nak'
            ack_nak['reason'] = f'{err_msg} is not found'
            return True

        return False

    # --------------------
    def _check_reset_tag(self, tag, rsp):
        if 'reason' in rsp:
            rsp['rsp'] = tag
            return True

        return False

    # --------------------
    def _check_ack(self, tag):
        rsp = {
            'rsp': tag,
            'value': 'ack',
        }
        return rsp
