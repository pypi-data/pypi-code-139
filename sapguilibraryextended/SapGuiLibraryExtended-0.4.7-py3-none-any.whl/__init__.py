

__version__ = '0.4.7'
__author__ = 'Daniela Silva'


from ast import keyword
from operator import index
import pythoncom
import win32com.client
import time
from pythoncom import com_error
import robot.libraries.Screenshot as screenshot
import os
from robot.api import logger

class SapGuiLibraryExtended():

    def __init__(self, screenshots_on_error=True, screenshot_directory=None):
        super(SapGuiLibraryExtended).__init__()
        self.explicit_wait = float(0.0)

        self.sapapp = -1
        self.session = -1
        self.connection = -1

        self.take_screenshots = screenshots_on_error
        self.screenshot = screenshot.Screenshot()

        if screenshot_directory is not None:
            if not os.path.exists(screenshot_directory):
                os.makedirs(screenshot_directory)
            self.screenshot.set_screenshot_directory(screenshot_directory)

    def select_context_menu_item(self, element_id, menu_or_button_id, item_id):
        """Selects an item from the context menu by clicking a button or right-clicking in the node context menu.
        """
        self.element_should_be_present(element_id)

        # The function checks if the element has an attribute "nodeContextMenu" or "pressContextButton" or "pressToolbarContextButton"
        if hasattr(self.session.findById(element_id), "nodeContextMenu"):
            self.session.findById(element_id).nodeContextMenu(menu_or_button_id)
        elif hasattr(self.session.findById(element_id), "pressContextButton"):
            self.session.findById(element_id).pressContextButton(menu_or_button_id)
        elif hasattr(self.session.findById(element_id), "pressToolbarContextButton"):
            self.session.findById(element_id).pressToolbarContextButton(menu_or_button_id)
        # The element has neither attributes, give an error message
        else:
            self.take_screenshot()
            element_type = self.get_element_type(element_id)
            message = "Cannot use keyword 'select context menu item' for element type '%s'" % element_type
            raise ValueError(message)
        self.session.findById(element_id).selectContextMenuItem(item_id)
        time.sleep(self.explicit_wait)

    def click_toolbar_context_button(self, table_id, button_id):
        """Clicks a context button of a toolbar within a GridView 'table_id' which is contained within a shell object.
        Use the Scripting tracker recorder to find the 'button_id' of the button to click
        """
        self.element_should_be_present(table_id)
        try:
            self.session.findById(table_id).pressToolbarContextButton(button_id)
        except AttributeError:
            self.take_screenshot()
            self.session.findById(table_id).pressButton(button_id)
        except com_error:
            self.take_screenshot()
            message = "Cannot find Button_id '%s'." % button_id
            raise ValueError(message)
        time.sleep(self.explicit_wait)

    def doubleclick_cell(self, element_id, item_id, column_id):
        """Performs a double-click on a cell within a grid view object. Used only for shell objects.
        """
        # Performing the correct method on an element, depending on the type of element
        element_type = self.get_element_type(element_id)
        if element_type == "GuiShell":
            self.session.findById(element_id).doubleClick(item_id, column_id)
        else:
            self.take_screenshot()
            message = "You cannot use 'doubleclick cell' on element type '%s', maybe use 'click element' instead?" % element_type
            raise Warning(message)
        time.sleep(self.explicit_wait)

    def doubleclick(self, element_id):
        """Performs a double-click on a sbar object. Used only for gui status bar objects.
        """
        # Performing the correct method on an element, depending on the type of element
        element_type = self.get_element_type(element_id)
        if element_type == "GuiStatusbar":
            self.session.findById(element_id).doubleClick()
        else:
            self.take_screenshot()
            message = "You cannot use 'doubleclick' on element type '%s', maybe use 'click element' instead?" % element_type
            raise Warning(message)
        time.sleep(self.explicit_wait)

    def click_cell(self, element_id, item_id, column_id):
        """Performs a single click on a cell within a grid view object. Used only for shell objects.
        """
        # Performing the correct method on an element, depending on the type of element
        element_type = self.get_element_type(element_id)
        if element_type == "GuiShell":
            self.session.findById(element_id).click(item_id, column_id)
        else:
            self.take_screenshot()
            message = "You cannot use 'click cell' on element type '%s', maybe use 'click element' instead?" % element_type
            raise Warning(message)
        time.sleep(self.explicit_wait)

    def select_radio_button (self, element_id):
        """Performs a single click on a radio button. Used only for gui radio button objects.
        """
        # Performing the correct method on an element, depending on the type of element
        element_type = self.get_element_type(element_id)
        if element_type == "GuiRadioButton": #GuiUserArea
            self.session.findById(element_id).select()
        else:
            self.take_screenshot()
            message = "You cannot use 'select radiobutton' on element type '%s', maybe use 'click element' instead?" % element_type
            raise Warning(message)
        time.sleep(self.explicit_wait)

    def press_enter_in_shell_object(self, table_id, col_id):
        """Press Enter on a GridView 'table_id' which is contained within a shell object.

        Use the Scripting tracker recorder to find the 'col_id'.
        """
        self.element_should_be_present(table_id)

        try:
            self.session.findById(table_id).pressEnter()
            time.sleep(self.explicit_wait)
            logger.info("Pressing enter into object '%s'" % (table_id))
        except com_error:
            self.take_screenshot()
            message = "Cannot press enter into object '%s'" % (table_id)
            raise ValueError(message)

    def get_node_icon_code(self, shell_id, key_id, item_id):
        """Get the ABAP icon code from the node 'key_id' which is contained within a shell 'shell_id' tree object.

        Use the Scripting tracker recorder to find the 'key_id' and 'shell_id'.
        """
        self.element_should_be_present(shell_id)

        try:
            logger.info("Getting ABAP icon code from tree '%s' and node '%s'" % (shell_id, key_id))
            # iconCode = self.session.findById(shell_id).GetNodeAbapImage(key_id)            
            iconCode = self.session.findById(shell_id).GetAbapImage(key_id, item_id)
            # iconCode = self.session.findById(shell_id).GetAbapImage(key_id, '1')
            time.sleep(self.explicit_wait)
            return iconCode
        except com_error:
            self.take_screenshot()
            message = "Cannot get icon code from '%s'" % (shell_id)
            raise ValueError(message)

    def get_tree_type(self, shell_id):
        """Get the ABAP icon code from the node 'key_id' which is contained within a shell 'shell_id' tree object.

        Use the Scripting tracker recorder to find the 'key_id' and 'shell_id'.
        """
        self.element_should_be_present(shell_id)

        try:
            logger.info("Getting tree type '%s'" % (shell_id))
            treeType = self.session.findById(shell_id).GetTreeType()
            time.sleep(self.explicit_wait)
            return treeType
        except com_error:
            self.take_screenshot()
            message = "Cannot get tree type '%s'" % (shell_id)
            raise ValueError(message)

    def get_tree_nodes_keys(self, shell_id):
        """The collection contains the node keys of all the nodes in the 'shell_id' tree object.

        Use the Scripting tracker recorder to find the 'shell_id'.
        """
        self.element_should_be_present(shell_id)

        try:
            logger.info("Getting tree nodes keys from '%s'" % (shell_id))
            treeNodes = self.session.findById(shell_id).GetNodesCol()
            time.sleep(self.explicit_wait)
            return treeNodes
        except com_error:
            self.take_screenshot()
            message = "Cannot get tree type '%s'" % (shell_id)
            raise ValueError(message)

    def get_tree_node_text(self, shell_id, key_id):
        """This function returns the text of the node specified by the given key from shell object 'shell_id' and node 'key_id'.

        Use the Scripting tracker recorder to find the 'shell_id'.
        """
        self.element_should_be_present(shell_id)

        try:
            logger.info("Getting tree node text from '%s'" % (shell_id))
            noteText = self.session.findById(shell_id).GetNodeTextByKey(key_id)
            time.sleep(self.explicit_wait)
            return noteText
        except com_error:
            self.take_screenshot()
            message = "Cannot get node text from '%s'" % (shell_id)
            raise ValueError(message)

    def get_exclusive_path(self, basename, fileext, directory):
        directory = self._norm_path(directory)
        index = 0
        while True:
            index += 1
            path = os.path.join(directory, "%s_%d.%s" % (basename, index, fileext))
            if not os.path.exists(path):
                return path

    def _norm_path(self, path):
        if not path:
            return path
        return os.path.normpath(path.replace('/', os.sep))

    def get_filled_rows_count(self, table_id):
        """Return the number of rows with data from a GuiTableControl object.
           It does use a non documented way to retrieve row count with data, as VisibleRowCount and RowCount 
           properties include empty rows.
        """
        # Performing the correct method on an element, depending on the type of element
        element_type = self.get_element_type(table_id)
        if element_type == "GuiTableControl":
            rowCount = self.session.findById(table_id).VerticalScrollbar.Maximum + 1
            return rowCount
        else:
            self.take_screenshot()
            message = "You cannot get row count on element type '%s'?" % element_type
            raise Warning(message)
        time.sleep(self.explicit_wait)

    def send_key_property(self, element_id, key_id):
        """Performs a double-click on a sbar object. Used only for gui status bar objects.
        """
        # Performing the correct method on an element, depending on the type of element
        element_type = self.get_element_type(element_id)
        if element_type == "GuiComboBox":
          self.session.findById(element_id).key = key_id  
        else:
            self.take_screenshot()
            message = "You cannot use 'Send Key Propriety' on element type '%s', maybe use 'click element' instead?" % element_type
            raise Warning(message)
        time.sleep(self.explicit_wait)
    
    def run_exit_transaction(self, transaction):
        """Runs a Sap transaction. An error is given when an unknown transaction is specified.
        """
        self.session.findById("wnd[0]/tbar[0]/okcd").text = transaction
        time.sleep(self.explicit_wait)
        self.send_vkey(0)
        if transaction == '/NEX':
            exit_message = "/NEX transaction force SAP Gui to exit"
            return  exit_message
        else:    
            self.take_screenshot()
            message = "Unknown transaction: '%s'" % transaction
            raise ValueError(message)
    
    def click_tab(self, element_id):
        """Performs a click_tab on a guitab object.
        """
        # Performing the correct method on an element, depending on the type of element
        element_type = self.get_element_type(element_id)
        try:
            element_selected = self.session.findById(element_id).select()
            return  element_selected
        except com_error:
            self.take_screenshot()
            message = "Cannot click_tab from '%s'" % (element_id)
            raise ValueError(message)
    
    def click_current_cell(self, element_id, tab_name):
        """Performs a click_tab on a guitab object.
        """
        # Performing the correct method on an element, depending on the type of element
        element_type = self.get_element_type(element_id)
        try:
            self.session.findById(element_id).currentCellColumn = tab_name
        except com_error:
            self.take_screenshot()
            message = "Cannot click_tab from '%s'" % (element_id)
            raise ValueError(message)

    def double_click_custom(self, element_id):
        """Performs a double-click custom on a given element. Used only for shell objects.
        """

        # Performing the correct method on an element, depending on the type of element
        element_type = self.get_element_type(element_id)
        if element_type == "GuiShell":
            self.session.findById(element_id).doubleClickCurrentCell()
        else:
            self.take_screenshot()
            message = "You cannot use 'double-click custom element' on element type '%s', maybe use 'click element' instead?" % element_type
            raise Warning(message)
        time.sleep(self.explicit_wait)
    
    def select_row(self, element_id, row_num):
        """Selects an entire row of a element id. The row is an index to select the row, starting from 0.
        """
        element_type = self.get_element_type(element_id)
        if (element_type == "GuiTabStrip"):
            id = self.session.findById(element_id).getAbsoluteRow(row_num)
            id.selected = -1
        try:
            self.session.findById(element_id).selectedRows = row_num
        except com_error:
            self.take_screenshot()
            message = "Cannot use keyword 'select row' for element type '%s', maybe use 'select table row' instead?" % element_type
            raise ValueError(message)
        time.sleep(self.explicit_wait)

    def test(self, name):
        a = print("Hello", name)
        return(a)