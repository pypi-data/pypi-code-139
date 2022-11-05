import os
import sys

from pyipcore.ipui_ipc_lib import *
from pyipcore.ui_main import Ui_MainWindow

class TextEditRedirect:
    def __init__(self, textedit:QTextEdit):
        self.te = textedit
    def write(self, content):
        self.te.insertPlainText(content)

hoffset = 10

class UI_Main(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.btn_fromlib.clicked.connect(self.openLib)
        self.btn_last_page.clicked.connect(self.goLastPage)
        self.btn_next_page.clicked.connect(self.goNextPage)
        self.btn_select.clicked.connect(self.selectIPCoreFile)
        self.actionlibrary.triggered.connect(self.openLib)
        self.actionclear_output.triggered.connect(lambda :self.ipc_output.clear())
        self.actionquit.triggered.connect(lambda :exit(0))
        self.actionexport.triggered.connect(self.outputRebuild)
        self.actionnew.triggered.connect(self.selectIPCoreFile)

        env = GetEnviron()
        # self.file = None
        self.stdout = sys.stdout
        self.path = None
        self.ipc_dir = getattr(env, "ipc_path", None)
        self.ipc_name = getattr(env, "ipc_name", None)
        self.ipc_param_widgets = {}
        self.font12 = QFont('3ds', 12)
        self.font14 = QFont('3ds', 14)
        self.font16 = QFont('3ds', 16)
        self.select_ip_name = None
        # self.content = None
        self.rebuilder = None
        # self.stack_index = 0
        self.ipc_scene = QGraphicsScene(self)

        sys.stdout = TextEditRedirect(self.ipc_output)

        self.lbl_show_index.setText("")
        self.ipc_view.setScene(self.ipc_scene)
        self.ipc_view.setDragMode(self.ipc_view.RubberBandDrag)
        # self.tree.setHeaderLabels(["Python IP Core"])

        self.updatePageSwitch()

    def __del__(self):
        sys.stdout = self.stdout

    def openLib(self):
        # self.setEnabled(False)
        self.one = UI_IPC_LIB(self)
        self.one.show()

    def onReceiveUpdate(self):
        env = GetEnviron()

        if hasattr(env, "ipc_name") and hasattr(env, "ipc_path"):
            self.ipc_dir, self.ipc_name = env.ipc_path, env.ipc_name
            self.path = os.path.join(env.ipc_path, env.ipc_name + IPCTYPE)
            self.ipc_path.setText(self.path)

            self.updatePath()
        else:
            print("[ERROR]: No receive valid.")

    def goLastPage(self):
        self.ipc_stack.setCurrentIndex(self.ipc_stack.currentIndex() - 1)
        self.updatePageSwitch()

    def goNextPage(self):
        self.ipc_stack.setCurrentIndex(self.ipc_stack.currentIndex() + 1)
        self.updatePageSwitch()

    def updatePageSwitch(self):
        max_num = self.ipc_stack.count()
        index = self.ipc_stack.currentIndex()
        if index > 0:
            self.btn_last_page.setEnabled(True)
        else:
            self.btn_last_page.setEnabled(False)

        if (index + 1) < max_num:
            self.btn_next_page.setEnabled(True)
        else:
            self.btn_next_page.setEnabled(False)

        show = f"{index + 1}/{self.ipc_stack.count()}"
        self.lbl_show_index.setText(show if self.ipc_stack.count() != 0 else "")

    def updatePath(self):
        file = files(self.ipc_dir, IPCTYPE)
        if file.get(self.ipc_name) != False:
            #self.ipc_widget.setEnabled(True)  #
            self.rebuilder = IPCoreReBuilder(self.ipc_dir, "")  # self.work_dir)
            self.rebuilder.loadIPCore(self.ipc_name)
            self.rebuilder.analyseAll()  #
            self.loadIPCoreFile()  #
        else:
            # self.ipc_widget.setEnabled(False)  #
            self.rebuilder = None  #
            self.clearIPCoreFile()  #

        self.updatePageSwitch()

    def createNewPage(self):
        widget = QWidget()
        widget.setGeometry(0, 0, self.ipc_stack.width(), self.ipc_stack.height())
        widget.move(0, 0)
        # self.ipc_stack.addWidget(widget)
        return widget

    def clearIPCoreFile(self):
        while self.ipc_stack.count():
            self.ipc_stack.removeWidget(self.ipc_stack.currentWidget())

    def loadIPCoreFile(self):
        # self.ipc_stack.width()
        # self.ipc_stack.height()
        self.ipc_param_widgets = {}
        self.clearIPCoreFile()

        # create frame for each $param
        index_height, hspan = 20, 60
        current_page = self.createNewPage()
        avs = self.rebuilder.getVariables()
        nivars = self.rebuilder.getVariables_WhichNoInputs()

        need, no_need = [], []
        # sort by whether need input
        for each in avs:
            if each in nivars:
                no_need += [each]
            else:
                need += [each]
        avs = need + no_need

        # create paramFrames
        for rvar_name in avs:
            res = self.createParamFrame(current_page, (0, index_height), rvar_name, self.rebuilder,
                                        "black" if rvar_name in need else "gray")
            self.ipc_param_widgets[rvar_name] = res

            index_height += res["pf"].height()

            if index_height >= current_page.height():
                index_height = 20
                self.ipc_stack.addWidget(current_page)
                current_page = self.createNewPage()
                res["pf"].setParent(current_page)
                res["pf"].setGeometry(hoffset, index_height, res["pf"].width(), res["pf"].height())
                index_height += res["pf"].height()

        self.ipc_stack.addWidget(current_page)
        self.ipc_stack.setCurrentIndex(0)

        # ------------------------------------------------
        self.updateModuleImage()

    def createParamFrame(self, parent: QWidget, pos, raw_param_name, rebuilder: IPCoreReBuilder, color="black"):
        width = parent.width()
        param_name = raw_param_name[1:]
        res = {}

        pf = QGroupBox(parent)
        pf.setTitle(f"Param: {param_name}")
        pf.setFont(self.font14)
        pf.setStyleSheet(f"color:{color}")
        res["pf"] = pf

        # horizon and vertical, not width and height
        hspan = 10
        vspan = 10
        index_height = int(vspan + 26 / 2)  # 24 is the group title height

        # rebuilder.getAllNeedInputVariables()
        # value
        if (raw_param_name in rebuilder.getVariables_WhichNeedInputs()):
            dh = 22

            v_label = QLabel(pf)
            v_label.setGeometry(5, index_height, 60, dh)
            v_label.setText("value: ")
            v_label.setFont(self.font12)
            v_label.setStyleSheet(f"color:{color}")

            v_lineEdit = QLineEdit(pf)
            v_lineEdit.setGeometry(v_label.width() + 5, index_height,
                                   width - 2 * hspan - v_label.width(), dh)
            v_lineEdit.setText(rebuilder.getVariable_Default(raw_param_name, ""))
            v_lineEdit.setFont(self.font12)
            v_lineEdit.setStyleSheet(f"color:{color}")
            v_lineEdit.editingFinished.connect(self.onInputChange)

            res["v"] = [v_label, v_lineEdit]
            index_height += dh + vspan
        # refunc
        raw_all_refuncs = rebuilder.getVariables_RawRefuncs()
        if (raw_param_name in raw_all_refuncs):
            dh = 22

            rf_label = QLabel(pf)
            rf_label.setGeometry(5, index_height, 60, dh)
            rf_label.setText("refunc: ")
            rf_label.setFont(self.font12)
            rf_label.setStyleSheet(f"color:gray")

            rf_lineEdit = QLineEdit(pf)
            rf_lineEdit.setGeometry(rf_label.width() + 5, index_height, width - 2 * hspan - rf_label.width(), dh)
            rf_lineEdit.setText(raw_all_refuncs[raw_param_name])
            rf_lineEdit.setReadOnly(True)
            rf_lineEdit.setFont(self.font12)
            rf_lineEdit.setStyleSheet(f"color:gray")

            index_height += dh + vspan
            res["rf"] = [rf_label, rf_lineEdit]

        # help
        var_hlp = rebuilder.getVariable_Help(raw_param_name)
        if var_hlp:
            dh = 66

            hlp_textEdit = QTextEdit(pf)
            hlp_textEdit.setGeometry(5, index_height, width - 2 * hspan, dh)
            hlp_textEdit.setText("    " + var_hlp)
            hlp_textEdit.setReadOnly(True)
            hlp_textEdit.setFont(self.font12)
            hlp_textEdit.setStyleSheet(f"color:#365036")

            index_height += dh + vspan
            res["hlp"] = hlp_textEdit

        pf.setGeometry(pos[0] + hoffset, pos[1], width, index_height)
        return res

    def collectUserInput(self):
        inputs = {}
        for k, each in self.ipc_param_widgets.items():
            if each.get('v'):
                inputs[k] = each['v'][1].text()
        return inputs

    def onInputChange(self):
        self.updateModuleImage()

    def updateModuleImage(self):
        inputs = self.collectUserInput()
        self.rebuilder.fillVariables(inputs)
        self.rebuilder.refuncVariables()
        self.rebuilder.doRebuild()
        # self.rebuilder.removeNotes()
        rebuild = self.rebuilder.getRebuild()

        vb = GetVerilogParser()
        try:
            ast = vb.parse(rebuild)
        except Exception as err:
            print(f"{err}\n\n[ERROR]: Occur an error when parse your verilog file. (Parser == pyverilog)|(see output.log for more information.)")
            
            open(os.path.join(self.ipc_dir, "output.log"), 'w').write(rebuild)
            return

        ipcg = IPCoreGraphic(ast)
        img = ipcg.draw()
        img.save("temp.png")

        self.ipc_scene.clear()
        pix = QPixmap("temp.png")
        pix_item = QGraphicsPixmapItem(pix)
        pix_item.setFlag(QGraphicsItem.ItemIsSelectable)
        pix_item.setFlag(QGraphicsItem.ItemIsMovable)
        pix_item.setPos(int(self.ipc_view.width() / 2), int(self.ipc_view.height() / 2))
        # pix_item.setScale( CalcScale(img.size, [self.ipc_view.width(), self.ipc_view.height()]) )
        self.ipc_scene.addItem(pix_item)

    def outputRebuild(self):
        if self.rebuilder is None:
            print("[ERROR]: Select and redfined an ip core before you export.")
            return
        inputs = self.collectUserInput()
        self.rebuilder.fillVariables(inputs)
        self.rebuilder.refuncVariables()
        self.rebuilder.doRebuild()
        self.rebuilder.removeNotes()
        self.rebuilder.addVariablesValueNote()
        rebuild = self.rebuilder.getRebuild()

        ast = GetVerilogParser().parse(rebuild)
        ipcp = IPCoreParse(ast)

        df_path = os.path.join(os.path.expanduser("~"), 'Desktop', ipcp.getModuleName() + ".v")
        filepath, _ = QFileDialog.getSaveFileName(self, "Select Saved File", df_path, "Verilog HDL Files(*.v)")

        try:
            open(filepath, 'w').write(rebuild)
        except Exception as err:
            print(f"{err}\n\n[ERROR]: Failed to save rebuild.")
            return

        print(f"[INFO]: Successfully saved at: {filepath}. ")

        self.rebuilder.analyseInstCode()
        inst_code = self.rebuilder.getInstCode()
        if inst_code is not None:
            pyperclip.copy(inst_code)
            print(f"[INFO]: Copy INST_CODE into your clipboard.")
        else:
            print(f"[ERROR]: Failed copy INST_CODE.")

    def selectIPCoreFile(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Select Python IP Core File", self.ipc_dir if self.ipc_dir else "", "IP Core File(*.pyipc)")

        env = GetEnviron()
        env.ipc_path, env.ipc_name = os.path.dirname(filepath), os.path.basename(filepath)[:-6]

        #print(env.ipc_path, env.ipc_name)

        self.onReceiveUpdate()


def UI_IPRebuild():
    app = QApplication(sys.argv)
    myWin = UI_Main()
    myWin.show()
    app.exec_()


if __name__ == "__main__":
    GetEnviron().ipc_path = r"C:\Users\CIE2018\Desktop\ipcore"
    UI_IPRebuild()
