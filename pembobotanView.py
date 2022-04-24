# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pembobotanView.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from library import connection, messagebox
import subprocess


class Ui_PembobotanWindow(object):
    def scraping_view(self):
        subprocess.Popen(['python', 'scrapingView.py'], shell=True)
        sys.quit()

    def preprocessing_view(self):
        from preprocessingView import Ui_Preprocessing
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Preprocessing()
        self.ui.setupUi(self.window)
        self.window.show()

    def show_data_testing(self):
        try:
            cur, con = connection()
            cur.execute("SELECT komentar FROM preprocessing_testing")
            result = cur.fetchall()
            self.tableTesting.setRowCount(0)
            self.tableTesting.setHorizontalHeaderLabels(['komentar'])

            for row_number, row_data in enumerate(result):
                self.tableTesting.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableTesting.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
            con.close()
        except Exception as e:
            print(e)

    def show_data_uji(self):
        try:
            cur, con = connection()
            cur.execute("SELECT komentar FROM preprocessing_uji")
            result = cur.fetchall()
            self.tableUji.setRowCount(0)
            self.tableUji.setHorizontalHeaderLabels(['komentar'])

            for row_number, row_data in enumerate(result):
                self.tableUji.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableUji.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
            con.close()
        except Exception as e:
            print(e)

    def pembobotan(self):
        cur, con = connection()
        cur.execute("SELECT kata, positive, negative, neutral FROM pembobotan")
        data = cur.fetchall()

        self.tableBobot.setRowCount(0)
        self.tableBobot.setHorizontalHeaderLabels(['kata', 'positif', 'negatif', 'netral'])

        for row_number, row_data in enumerate(data):
            self.tableBobot.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableBobot.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

    def probabilitasLikehood(self):
        cur, con = connection()
        cur.execute("SELECT kata, positive, negative, neutral FROM pembobotan")
        pembobotan = cur.fetchall()

        positive = 0
        negative = 0
        neutral = 0
        total = 0
        for p in pembobotan:
            positive = positive + p[1]
            negative = negative + p[2]
            neutral = neutral + p[3]

            total = positive + negative + neutral

        likehood = []
        for pem in pembobotan:
            likePositif = (pem[1] + 1) / (positive + total)
            likeNegatif = (pem[2] + 1) / (negative + total)
            likeNetral = (pem[3] + 1) / (neutral + total)

            likehood.append([pem[0], likePositif, likeNegatif, likeNetral])

        return likehood

    def processAlgoritma(self):
        prior = 1 / 3
        likehood = self.probabilitasLikehood()

        cur, con = connection()
        cur.execute('Select komentar, id_komentar from preprocessing_uji')
        komentar_uji = cur.fetchall()

        tes = []
        for k in komentar_uji:
            if k[0] in [l[0] for l in likehood]:
                tes.append(k[0])
        print(likehood[0][0])

    def setupUi(self, PembobotanWindow):
        PembobotanWindow.setObjectName("PembobotanWindow")
        PembobotanWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(PembobotanWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 801, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: rgb(119, 119, 119);\n"
"color: rgb(255, 255, 255);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.tableTesting = QtWidgets.QTableWidget(self.centralwidget)
        self.tableTesting.setGeometry(QtCore.QRect(40, 110, 341, 171))
        self.tableTesting.setObjectName("tableTesting")
        self.tableTesting.setColumnCount(1)
        self.tableTesting.setRowCount(0)
        self.show_data_testing()
        header = self.tableTesting.horizontalHeader()
        header.setStretchLastSection(True)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableTesting.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableTesting.setHorizontalHeaderItem(1, item)
        self.tableUji = QtWidgets.QTableWidget(self.centralwidget)
        self.tableUji.setGeometry(QtCore.QRect(40, 330, 341, 161))
        self.tableUji.setObjectName("tableUji")
        self.tableUji.setColumnCount(1)
        self.tableUji.setRowCount(0)
        self.show_data_uji()
        header = self.tableUji.horizontalHeader()
        header.setStretchLastSection(True)
        self.tableBobot = QtWidgets.QTableWidget(self.centralwidget)
        self.tableBobot.setGeometry(QtCore.QRect(410, 110, 351, 381))
        self.tableBobot.setObjectName("tableBobot")
        self.tableBobot.setColumnCount(4)
        self.tableBobot.setRowCount(0)
        self.pembobotan()
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 75, 341, 21))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(40, 300, 341, 21))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(410, 80, 351, 21))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.btnAlgoritma = QtWidgets.QPushButton(self.centralwidget)
        self.btnAlgoritma.setGeometry(QtCore.QRect(40, 510, 721, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.btnAlgoritma.setFont(font)
        self.btnAlgoritma.setObjectName("btnAlgoritma")
        self.btnAlgoritma.clicked.connect(self.processAlgoritma)
        PembobotanWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(PembobotanWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuHome = QtWidgets.QMenu(self.menubar)
        self.menuHome.setObjectName("menuHome")
        self.menuDataset = QtWidgets.QMenu(self.menubar)
        self.menuDataset.setObjectName("menuDataset")
        self.menuPreprocessing = QtWidgets.QMenu(self.menubar)
        self.menuPreprocessing.setObjectName("menuPreprocessing")
        self.menuPembobotan = QtWidgets.QMenu(self.menubar)
        self.menuPembobotan.setObjectName("menuPembobotan")
        self.menuNaive_Bayes = QtWidgets.QMenu(self.menubar)
        self.menuNaive_Bayes.setObjectName("menuNaive_Bayes")
        self.menuPengujian = QtWidgets.QMenu(self.menubar)
        self.menuPengujian.setObjectName("menuPengujian")
        PembobotanWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(PembobotanWindow)
        self.statusbar.setObjectName("statusbar")
        PembobotanWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuHome.menuAction())
        self.menubar.addAction(self.menuDataset.menuAction())
        self.menubar.addAction(self.menuPreprocessing.menuAction())
        self.menubar.addAction(self.menuPembobotan.menuAction())
        self.menubar.addAction(self.menuNaive_Bayes.menuAction())
        self.menubar.addAction(self.menuPengujian.menuAction())

        self.retranslateUi(PembobotanWindow)
        QtCore.QMetaObject.connectSlotsByName(PembobotanWindow)

    def retranslateUi(self, PembobotanWindow):
        _translate = QtCore.QCoreApplication.translate
        PembobotanWindow.setWindowTitle(_translate("PembobotanWindow", "MainWindow"))
        self.label.setText(_translate("PembobotanWindow", "Preprocessing & Pembobotan"))
        item = self.tableTesting.horizontalHeaderItem(0)
        item.setText(_translate("PembobotanWindow", "Komentar"))
        self.label_2.setText(_translate("PembobotanWindow", "Preprocessing Testing"))
        self.label_3.setText(_translate("PembobotanWindow", "Preprocessing Uji"))
        self.label_4.setText(_translate("PembobotanWindow", "Pembobotan Testing"))
        self.btnAlgoritma.setText(_translate("PembobotanWindow", "Perhitungan Algoritma Naive Bayes"))
        self.menuHome.setTitle(_translate("PembobotanWindow", "Home"))
        self.menuDataset.setTitle(_translate("PembobotanWindow", "Dataset"))
        self.menuPreprocessing.setTitle(_translate("PembobotanWindow", "Preprocessing"))
        self.menuPembobotan.setTitle(_translate("PembobotanWindow", "Pembobotan"))
        self.menuNaive_Bayes.setTitle(_translate("PembobotanWindow", "Naive Bayes"))
        self.menuPengujian.setTitle(_translate("PembobotanWindow", "Pengujian"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PembobotanWindow = QtWidgets.QMainWindow()
    ui = Ui_PembobotanWindow()
    ui.setupUi(PembobotanWindow)
    PembobotanWindow.show()
    sys.exit(app.exec_())
