import pymysql
from PyQt5 import QtCore, QtGui, QtWidgets


def connection():
    con = pymysql.connect(db='pythontest', user='root',
                          passwd='', host='localhost', port=3306, autocommit=True)
    cur = con.cursor()
    return cur, con

def messagebox(title, message):
    mess = QtWidgets.QMessageBox()
    mess.setWindowTitle(title)
    mess.setText(message)
    mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
    mess.exec_()