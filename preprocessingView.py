# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'preprocessingView.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import string

import nltk.tokenize
from PyQt5 import QtCore, QtGui, QtWidgets
from library import connection, messagebox
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import itertools
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import csv
import subprocess
import os
import sys

class Ui_Preprocessing(object):
    def scraping_view(self):
        subprocess.Popen(['python', 'scrapingView.py'], shell=True)
        sys.quit()

    def pembobotan_view(self):
        from pembobotanView import Ui_PembobotanWindow
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_PembobotanWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        Ui_Preprocessing.hide()

    def show_data(self):
        try:
            cur, con = connection()
            cur.execute("SELECT komentar, suka, waktu, userlink, user FROM komentar")
            result = cur.fetchall()
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.setHorizontalHeaderLabels(['komentar', 'suka', 'waktu', 'userlink', 'user'])

            for row_number, row_data in enumerate(result):
                self.tableWidget_2.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget_2.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
            con.close()
        except Exception as e:
            print(e)

    def show_dataset(self):
        try:
            cur, con = connection()
            cur.execute("select label, komentar from dataset")
            result = cur.fetchall()
            self.tableWidget.setRowCount(0)
            self.tableWidget.setHorizontalHeaderLabels(['sentimen', 'komentar'])

            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
            con.close()
        except Exception as e:
            print(e)

    def import_file(self):
        try:
            Tk().withdraw()
            filename = askopenfilename()
            with open(filename) as csvfile:
                reader = csv.DictReader(csvfile, delimiter = ',')
                cur, con = connection()
                for row in reader:
                    sentimen = row['sentimen'].replace('|', '')
                    komentar = row['komentar'].replace('|', '')
                    sql = "Insert into dataset (label, komentar) values (%s, %s)"
                    data = cur.execute(sql, (sentimen, komentar))
                if(data):
                    messagebox('Sukses', 'Import berhasil')
                    cur.execute('Select label, komentar from dataset')
                    result = cur.fetchall()
                    self.tableWidget.setRowCount(0)
                    self.tableWidget.setHorizontalHeaderLabels(['label', 'komentar'])

                    for row_number, row_data in enumerate(result):
                        self.tableWidget.insertRow(row_number)
                        for column_number, data in enumerate(row_data):
                            self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                    con.close()
        except Exception as e:
            print(e)

    def preprocessing_uji(self):
        try:
            cur, con = connection()
            cur.execute('select komentar from komentar')
            komentar_uji = cur.fetchall()

            tuple_uji = []
            for row in komentar_uji:
                tuple_uji.append(row)
                print(tuple_uji)

            dataset_uji = list(itertools.chain(*tuple_uji))

            filtering_uji = []
            for list_tokenizing in dataset_uji:
                filtering_uji.append(list_tokenizing.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation))).lower())
                print(filtering_uji)

            stopFactory = StopWordRemoverFactory()
            stopword = stopFactory.create_stop_word_remover()

            stopword_uji = []
            for f in filtering_uji:
                stopword_uji.append(stopword.remove(f))
                print(stopword_uji)

            tokenizing_uji = []
            for list_uji in stopword_uji:
                tokenizing_uji.extend(nltk.tokenize.word_tokenize(list_uji))
                print(tokenizing_uji)

            stemFactory = StemmerFactory()
            stemmer = stemFactory.create_stemmer()

            stemming_uji = []
            for s in tokenizing_uji:
                stemming_uji.append(stemmer.stem(s))
                print(stemming_uji)

            stemming_uji = list(filter(None, stemming_uji))
            return stemming_uji
        except Exception as e:
            print(e)

    def preprocessing_testing(self):
        try:
            cur, con = connection()
            cur.execute('select komentar from dataset')
            komentar_testing = cur.fetchall()

            tuple_testing = []
            for row in komentar_testing:
                tuple_testing.append(row)
                print(tuple_testing)

            dataset_testing = list(itertools.chain(*tuple_testing))

            filtering_testing = []
            for data in dataset_testing:
                filtering_testing.append(data.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation))).lower())
                print(filtering_testing)

            stopFactory = StopWordRemoverFactory()
            stopword = stopFactory.create_stop_word_remover()

            stopword_testing = []
            for f in filtering_testing:
                stopword_testing.append(stopword.remove(f))
                print(stopword_testing)

            tokenizing_testing = []
            for f in stopword_testing:
                tokenizing_testing.extend(nltk.tokenize.word_tokenize(f))
                print(tokenizing_testing)

            stemFactory = StemmerFactory()
            stemmer = stemFactory.create_stemmer()

            stemming_testing = []
            for t in tokenizing_testing:
                stemming_testing.append(stemmer.stem(t))
                print(stemming_testing)

            stemming_testing = list(filter(None, stemming_testing))
            return stemming_testing
        except Exception as e:
            print(e)

    def getKomentar(self):
        try:
            cur, con = connection()
            cur.execute("SELECT komentar, label FROM dataset")
            komentar = cur.fetchall()

            return komentar
        except Exception as e:
            print(e)

    def getPreprocessingTesting(self):
        try:
            cur, con = connection()
            cur.execute("SELECT komentar FROM preprocessing_testing")
            data = cur.fetchall()

            preprocessing_testing = []
            for row in data:
                preprocessing_testing.extend(row)

            return preprocessing_testing
        except Exception as e:
            print(e)

    def pembobotan(self):
        try:
            cur, con = connection()
            preprocessing_testing = self.getPreprocessingTesting()
            komentar = self.getKomentar()

            filter_comment = []
            for j in preprocessing_testing:
                if j not in [f[0] for f in filter_comment]:
                    data = [j, 0, 0, 0]
                    filter_comment.append(data)

            for f in filter_comment:
                for k in komentar:
                    if f[0] in k[0].lower():
                        if k[1] == 'positive':
                            f[1] = f[1] + 1
                        elif k[1] == 'negative':
                            f[2] = f[2] + 1
                        else:
                            f[3] = f[3] + 1

            for f in filter_comment:
                sql_pembobotan = "insert into pembobotan (kata, positive, negative, neutral) values (%s, %s, %s, %s)"
                save_pembobotan = cur.execute(sql_pembobotan, (f[0], f[1], f[2], f[3]))

            return save_pembobotan
        except Exception as e:
            print(e)

    def processPreprocessing(self, data):
        try:
            # tuple_testing = []
            # for row in data:
            #     value = [str(row[0]), row[1]]
            #     tuple_testing.append(value)
            #
            # dataset_testing = list(itertools.chain(*tuple_testing))

            stopFactory = StopWordRemoverFactory()
            stopword = stopFactory.create_stop_word_remover()
            stemFactory = StemmerFactory()
            stemmer = stemFactory.create_stemmer()

            data_proses = []
            for d in data:
                tokenize_tempo = []
                data_tempo = d[1].translate(str.maketrans(string.punctuation, ' '*len(string.punctuation))).lower()
                stopword_tempo = stopword.remove(data_tempo)
                tokenize_tempo.extend(nltk.tokenize.word_tokenize(stopword_tempo))
                for t in tokenize_tempo:
                    if len(t) != 1:
                        value = [stemmer.stem(t), d[0]]
                        data_proses.append(value)

            return list(filter(None, data_proses))
        except Exception as e:
            print(e)

    def preprocessing(self):
        try:
            cur, con = connection()
            cur.execute('select id, komentar from dataset')
            komentar_testing = cur.fetchall()

            cur.execute('select id, komentar from komentar')
            komentar_uji = cur.fetchall()

            uji = self.processPreprocessing(komentar_uji)
            testing = self.processPreprocessing(komentar_testing)

            for data_uji in uji:
                if len(data_uji) != 1:
                    sql_uji = "insert into preprocessing_uji (komentar, id_komentar) values (%s, %s)"
                    save_uji = cur.execute(sql_uji, data_uji)

            for data_testing in testing:
                if len(data_testing) != 1:
                    sql_testing = "insert into preprocessing_testing (komentar, id_komentar) values (%s, %s)"
                    save_testing = cur.execute(sql_testing, data_testing)

            pembobotan = self.pembobotan()

            if (save_uji and save_testing and pembobotan):
                messagebox("SUKSES", "Data Preprocessing Tersimpan")
            else:
                messagebox("GAGAL", "Data Preprocessing Gagal Disimpan")
        except Exception as e:
            print(e)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 597)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
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
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 180, 371, 311))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        self.show_dataset()
        header = self.tableWidget.horizontalHeader()
        header.setStretchLastSection(True)
        self.tableWidget_2 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_2.setGeometry(QtCore.QRect(410, 130, 371, 361))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(5)
        self.tableWidget_2.setRowCount(0)
        self.show_data()
        self.btnImport = QtWidgets.QPushButton(self.centralwidget)
        self.btnImport.setGeometry(QtCore.QRect(30, 140, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.btnImport.setFont(font)
        self.btnImport.setObjectName("btnImport")
        self.btnImport.clicked.connect(self.import_file)
        self.btnUpdate = QtWidgets.QPushButton(self.centralwidget)
        self.btnUpdate.setGeometry(QtCore.QRect(150, 140, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.btnUpdate.setFont(font)
        self.btnUpdate.setObjectName("btnUpdate")
        self.btnDelete = QtWidgets.QPushButton(self.centralwidget)
        self.btnDelete.setGeometry(QtCore.QRect(270, 140, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.btnDelete.setFont(font)
        self.btnDelete.setObjectName("btnDelete")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(20, 510, 761, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.preprocessing)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 80, 361, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(410, 80, 361, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuHome = QtWidgets.QMenu(self.menubar)
        self.menuHome.setObjectName("menuHome")
        self.menuHome.addAction('Scraping View', self.scraping_view)
        self.menuDataset = QtWidgets.QMenu(self.menubar)
        self.menuDataset.setObjectName("menuDataset")
        self.menuPreprocessing = QtWidgets.QMenu(self.menubar)
        self.menuPreprocessing.setObjectName("menuPreprocessing")
        self.menuPreprocessing.addAction('Pembobotan View', self.pembobotan_view)
        self.menuNaive_Bayes = QtWidgets.QMenu(self.menubar)
        self.menuNaive_Bayes.setObjectName("menuNaive_Bayes")
        self.menuPengujian = QtWidgets.QMenu(self.menubar)
        self.menuPengujian.setObjectName("menuPengujian")
        self.menuPengujian_2 = QtWidgets.QMenu(self.menubar)
        self.menuPengujian_2.setObjectName("menuPengujian_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuHome.menuAction())
        self.menubar.addAction(self.menuDataset.menuAction())
        self.menubar.addAction(self.menuPreprocessing.menuAction())
        self.menubar.addAction(self.menuNaive_Bayes.menuAction())
        self.menubar.addAction(self.menuPengujian.menuAction())
        self.menubar.addAction(self.menuPengujian_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Preprocessing"))
        self.btnImport.setText(_translate("MainWindow", "Import"))
        self.btnUpdate.setText(_translate("MainWindow", "Update"))
        self.btnDelete.setText(_translate("MainWindow", "Delete"))
        self.pushButton_4.setText(_translate("MainWindow", "Preprocessing"))
        self.label_2.setText(_translate("MainWindow", "Dataset Testing"))
        self.label_3.setText(_translate("MainWindow", "Dataset Uji"))
        self.menuHome.setTitle(_translate("MainWindow", "Home"))
        self.menuDataset.setTitle(_translate("MainWindow", "Dataset"))
        self.menuPreprocessing.setTitle(_translate("MainWindow", "Preprocessing"))
        self.menuNaive_Bayes.setTitle(_translate("MainWindow", "Pembobotan"))
        self.menuPengujian.setTitle(_translate("MainWindow", "Naive Bayes"))
        self.menuPengujian_2.setTitle(_translate("MainWindow", "Pengujian"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Preprocessing()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
