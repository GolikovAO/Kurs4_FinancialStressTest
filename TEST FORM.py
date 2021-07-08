from PyQt5 import QtWidgets, uic
import sys

app = QtWidgets.QApplication([])
app.setStyle('Fusion')
win = uic.loadUi("design.ui")  # расположение вашего файла .ui

win.show()
sys.exit(app.exec())

# class AlignDelegate(QtWidgets.QStyledItemDelegate):
#     def initStyleOption(self, option, index):
#         super(AlignDelegate, self).initStyleOption(option, index)
#         option.displayAlignment = QtCore.Qt.AlignCenter


# self.table2019.setVisible(False)
# self.label2019.setVisible(False)
# self.table2020.setVisible(False)
# self.table_k.setVisible(False)
# self.radioButton1.setVisible(False)
# self.radioButton2.setVisible(False)
# self.label_OrgName.setVisible(False)
# self.label_OrgAddress.setVisible(False)
# self.textOrgName.setVisible(False)
# self.textOrgAddress.setVisible(False)
# self.tableResult.setVisible(False)
# self.buttonResult.setVisible(False)
# self.labelResult.setVisible(False)
# self.labelZLP.setVisible(False)
# self.labelIdex.setVisible(False)
# self.tableZLP.setVisible(False)
# self.buttonZLP.setVisible(False)
# self.balancetable2019.setVisible(False)
# self.balancetable2020.setVisible(False)

# delegate1 = AlignDelegate(self.table2019)
# delegate2 = AlignDelegate(self.table2020)
# self.table2019.setItemDelegateForColumn(1, delegate1)
# self.table2019.setItemDelegateForColumn(2, delegate1)
# self.table2020.setItemDelegateForColumn(1, delegate2)
# self.table2020.setItemDelegateForColumn(2, delegate2)