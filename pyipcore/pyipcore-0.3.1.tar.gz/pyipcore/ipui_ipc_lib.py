import sys
import shutil
from pyipcore.ipg import *
from pyipcore.ipc_img import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from pyipcore.ui_ipc_lib import Ui_Form


 
class UI_IPC_LIB(QMainWindow, Ui_Form):
    def __init__(self,parent =None):
        super(UI_IPC_LIB,self).__init__(parent)
        self.setupUi(self)
        self.btn_update.clicked.connect(self.updateDirectory)
        self.btn_addlib.clicked.connect(self.addLibrary)
        self.btn_rebuild.clicked.connect(self.rebuildIPCore)
        self.tree.itemDoubleClicked.connect(self.selectIPCore)

        env = GetEnviron()
        self.file = None
        self.path = getattr(env, "ipc_path", None)
        self.data = {}
        self.select_ip_name = None
        self.ipc_scene = QGraphicsScene(self)

        self.tree.setColumnCount(1)
        self.ipc_view.setScene(self.ipc_scene)
        self.ipc_view.setDragMode(self.ipc_view.RubberBandDrag)
        # self.tree.setHeaderLabels(["Python IP Core"])

        # ---------------------
        if self.path is not None:
            self.ipc_path.setText(self.path)
            self.updateDirectory()

    def updateDirectory(self):
        path = self.ipc_path.text()
        if not (os.path.exists(path) and os.path.isdir(path)):
            QMessageBox.information(self,"Not Valid Path", f"path: {path} is not a valid path. please check it and retry.")
            # set disable
            self.widget.setEnabled(False)
            return
        self.file = files(path, ".pyipc")
        self.path = path

        ###############
        GetEnviron().ipc_path = path
        SaveEnvrionKey("ipc_path")

        # set enable
        self.widget.setEnabled(True)

        self.updateIPCore2Tree()

    def addLibrary(self):
        filepath, _ = QFileDialog.getOpenFileNames(self, "Open Source File", getattr(GetEnviron(), "ipc_path", ""), "Verilog HDL Files(*.v);;Python IPCore Files(*.pyipc)")
        # print(filepath, _)
        if _[:3] == "Pyt":
            for path in filepath:
                name = os.path.basename(path)
                desc_path = os.path.join(self.path, name)
                if desc_path != path:
                    shutil.copy(path, desc_path)
        elif _[:3] == "Ver":
            ipcr = IPCoreReBuilder(self.path, ".")
            err_flag = 0
            for path in filepath:
                name = os.path.basename(path)[:-2]
                fread = open(path, 'r').read()
                if ipcr.doDefaultRebuild(name):
                    self.file.set(name, fread)
                    print(f"[INFO]: Successfully binary compile file: {name}.pyipc")
                else:
                    print(f"[ERROR]: Failed to build .pyipc for {name}.v")
                    err_flag += 1
            if err_flag:
                QMessageBox.information(self,"Some Compile Failed.", f"Some files failed. \n{len(filepath) - err_flag} Success, {err_flag} Failed.")
            
        self.updateIPCore2Tree()

    def updateIPCore2Tree(self):
        self.tree.clear()
        root = QTreeWidgetItem(self.tree)
        root.setText(0, "Python IP Core")
        data = {"$":[]}
        for key in self.file.list():
            content = self.file[key]
            paths = []
            fda = FindAll("//\s*[cC(cls)(Cls)(CLS)(Class)(class)(CLASS)]\$\s*:.*", content)
            if fda:
                fd = fda[0]
                fd = re.sub("^\s*", "", fd[1][fd[1].find(":") + 1:])
                for each in fd.split("/"):
                    if each:
                        paths += ["| " + each]

            try:
                target = data
                for node in paths:
                    if target.get(node) is None:
                        target[node] = {"$":[]}
                    target = target[node]
                if isinstance(target, list):
                    target.append(key)
                else:
                    target["$"].append(key)
            except Exception as err:
                print(f"{err}\n\n[ERROR]: Failed to load class info for {key}.pyipc")
                continue
        
        self.data = data

        self.tree.expandItem(root)

        # insert
        def insert(node, target):
            for k, v in target.items():
                if k == "$":
                    continue
                else:
                    child = QTreeWidgetItem(node)
                    child.setText(0, k)
                    insert(child, v)

            for txt in target.get("$", []):
                child = QTreeWidgetItem(node)
                child.setText(0, txt)
        insert(root, data)

    def selectIPCore(self, tree_item:QTreeWidgetItem, b):
        if tree_item.text(0)[0] == '|': return
        self.select_ip_name = tree_item.text(0)
        self.ipc_scene.clear()

        rebuilder = IPCoreReBuilder(self.path, ".")
        rebuilder.doDefaultRebuild(tree_item.text(0))
        rebuilder.removeNotes()
        rebuild = rebuilder.getRebuild()

        vb = GetVerilogParser()
        try:
            ast = vb.parse(rebuild)
        except Exception as err:
            print(f"{err}\n\n[ERROR]: Occur an error when parse your verilog file. (Parser == pyverilog)|(see output.log for more information.)")
            
            open(os.path.join(self.path, "output.log"), 'w').write(rebuild)
            return

        ipcg = IPCoreGraphic(ast)
        img = ipcg.draw()
        img.save("temp.png")

        pix = QPixmap("temp.png")
        pix_item = QGraphicsPixmapItem(pix)
        pix_item.setFlag(QGraphicsItem.ItemIsSelectable)
        pix_item.setFlag(QGraphicsItem.ItemIsMovable)
        pix_item.setPos(int(self.ipc_view.width() / 2), int(self.ipc_view.height() / 2))
        # pix_item.setScale( CalcScale(img.size, [self.ipc_view.width(), self.ipc_view.height()]) )
        self.ipc_scene.addItem(pix_item)

        # --------------------------------------------------
        green_color = QColor()
        black_color = QColor()
        gray_color = QColor()
        green_color.setNamedColor("#EE008B45")
        black_color.setNamedColor("#000000")
        gray_color.setNamedColor("#DD000000")

        green_tcf = QTextCharFormat()
        gray_tcf = QTextCharFormat()
        black_tcf = QTextCharFormat()
        green_tcf.setForeground(green_color)
        gray_tcf.setForeground(gray_color)
        black_tcf.setFontWeight(QFont.Bold)
        black_tcf.setForeground(black_color)

        try:
            rebuilder.analyseInstCode()
            inst_code = rebuilder.getInstCode()
            info = "[PREVIEW]\n"
        except NoInstCodeException:
            inst_code = ipcg.ipcparse.module_name
            inst_code = f"{inst_code} {inst_code}_inst(\n   ...\n);"
            info = "[MISSING]\n"

        value_note = rebuilder.buildVariablesValueNote()
        self.ipc_desc.setText("")
        cursor = self.ipc_desc.textCursor()
        cursor.insertText(info, gray_tcf)
        cursor.insertText(value_note.replace("\n\n", "\n"), green_tcf)
        cursor.insertText(inst_code.replace("\n\n", "\n"), black_tcf)

    def rebuildIPCore(self):
        if self.select_ip_name is None or self.file.get(self.select_ip_name) == False:
            QMessageBox.information(self, "Not Valid IP name",
                                    f"Please retry after you select an IP Core from left table. ")
        env = GetEnviron()
        env.ipc_path = self.path
        env.ipc_name = self.select_ip_name
        self.destroy()

    def destroy(self, *args, **kwargs):
        super(UI_IPC_LIB, self).destroy(*args, **kwargs)
        parent = self.parent()
        if parent:
            parent.onReceiveUpdate()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = UI_IPC_LIB()
    myWin.show()
    app.exec_()






