# Form implementation generated from reading ui file 'qt/aqt/forms/preview.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from aqt.utils import tr



class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(717, 636)
        Form.setWindowTitle("Form")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.preview_box = QtWidgets.QGroupBox(Form)
        self.preview_box.setTitle("GroupBox")
        self.preview_box.setObjectName("preview_box")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.preview_box)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.preview_front = QtWidgets.QRadioButton(self.preview_box)
        self.preview_front.setText("FRONT")
        self.preview_front.setChecked(True)
        self.preview_front.setObjectName("preview_front")
        self.horizontalLayout.addWidget(self.preview_front, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.preview_back = QtWidgets.QRadioButton(self.preview_box)
        self.preview_back.setText("BACK")
        self.preview_back.setObjectName("preview_back")
        self.horizontalLayout.addWidget(self.preview_back, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.preview_settings = QtWidgets.QPushButton(self.preview_box)
        self.preview_settings.setText("")
        self.preview_settings.setAutoDefault(False)
        self.preview_settings.setDefault(False)
        self.preview_settings.setObjectName("preview_settings")
        self.horizontalLayout.addWidget(self.preview_settings)
        self.cloze_number_combo = QtWidgets.QComboBox(self.preview_box)
        self.cloze_number_combo.setObjectName("cloze_number_combo")
        self.horizontalLayout.addWidget(self.cloze_number_combo)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addWidget(self.preview_box)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass