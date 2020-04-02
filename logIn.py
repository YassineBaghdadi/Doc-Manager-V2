from PyQt5 import QtWidgets, QtCore, QtGui, QtPrintSupport
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import *
import os
from os import path
import sys
import time
import sqlite3
import pymysql
from time import *

import hashlib
from admin_settings import *
from main import *
import noInternetAlert



logIn_ui,_ = loadUiType(path.join(path.dirname(__file__), "ui/logIn.ui"))

class LogIn(QWidget, logIn_ui):
    def __init__(self, parent = None):
        super(LogIn, self).__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)

        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        # self.admin_user = 'f986a7ef9eb3fa8b6ce6a46d5302adc3'#MOY
        # self.admin_pass = '9d775cbd1a1a75b7b9ac184d0d12489e'#MOY1
        self.admin_user, self.admin_pass = str(open('ss.txt', 'r').readline()).split('.')
        self.cnx.setEnabled(False)
        self.getInfo()
        self.today = str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))

        # palette = QPalette()
        # palette.setBrush(QPalette.Background, QBrush(QImage("img/pack.png")))
        # self.setPalette(palette)
        self.label.setPixmap(QtGui.QPixmap('src/img/login.png'))
        self.label.setScaledContents(True)
        self.setWindowTitle('Bienvenue')

        self.username_in.setPlaceholderText('User Name')
        self.passwrd_in.setPlaceholderText('Password')

        self.cnx.clicked.connect(self.cnnx)
        self.username_in.textChanged.connect(self.typing)
        self.passwrd_in.textChanged.connect(self.typing1)
        self.passwrd_in.returnPressed.connect(self.cnnx)

        try:
            self.dblocal = sqlite3.connect('src/setting.db')
            self.curs = self.dblocal.cursor()
            self.curs.execute('select host, db_user, db_pass, port, db_name from admin_setting')
            # data = self.curs.fetchone()
            # self.host_db = data[0]
            # self.user_db = data[1]
            # self.passwrd_db = data[2]
            # self.port_db = data[3]
            # self.DBname = data[4]
            self.host_db, self.user_db, self.passwrd_db, self.port_db, self.DBname = self.curs.fetchone()
            # try:
            #     self.db_ = pymysql.connect(self.host_db, self.user_db, self.passwrd_db, self.DBname, int(self.port_db))
            #
            #
            # except Exception as e:
            #     err_log = open('src/logs.txt', 'a')
            #     err_log.write('\n' + self.today + ' ' + str(e))
            #     self.err = noInternetAlert.NoInternetAlert(err_content=e)
            #     self.err.show()
            #     self.close()

        except Exception as e:
            err_log = open('src/logs.txt', 'a')
            err_log.write('\n' + self.today + ' '  + str(e))
            self.err = noInternetAlert.NoInternetAlert(err_content=e)
            self.err.show()
            self.close()
        self.db_ = pymysql.connect(self.host_db, self.user_db, self.passwrd_db, self.DBname, int(self.port_db))
        self.mysqlCur = self.db_.cursor()
    def getInfo(self):
        return self.admin_user, self.admin_pass

    def cnnx(self):
        if str(hashlib.md5(self.username_in.text().encode()).hexdigest()) == self.admin_user and str(
                hashlib.md5(self.passwrd_in.text().encode()).hexdigest()) == self.admin_pass:
            self.AS = AdminSetting()
            self.AS.show()
            self.close()

        else:
            try:
                self.mysqlCur.execute('select role from users where username = "{}" and passwrd = "{}"'.format(self.username_in.text(), self.passwrd_in.text()))
                self.acc_type = self.mysqlCur.fetchone()[0]
                print(self.acc_type)
                if self.acc_type:

                        self.main_ = Main(self.acc_type)
                        self.main_.show()
                        self.close()

                else:
                        self.passwrd_in.setText('')
                        self.username_in.setText('')
                        self.passwrd_in.setStyleSheet('border : 2px solid red')
                        self.username_in.setStyleSheet('border : 2px solid red')

            except Exception as e:
                    err_log = open('src/logs.txt', 'a')
                    err_log.write('\n{}, {}, username used : {}'.format(self.today, str(e), self.username_in.text()))
                    self.err = noInternetAlert.NoInternetAlert(err_content=e)
                    self.err.show()
                    self.close()





    def typing(self):
        if len(self.username_in.text()) > 2:
            self.username_in.setStyleSheet('border : 2px solid white')
        else:
            self.username_in.setStyleSheet('border : 2px solid red')

        if len(self.username_in.text()) > 2 and len(self.passwrd_in.text()) > 2:
            self.cnx.setEnabled(True)
        else:
            self.cnx.setEnabled(False)



    def typing1(self):
        if len(self.passwrd_in.text()) > 2:
            self.passwrd_in.setStyleSheet('border : 2px solid white')
            self.cnx.setEnabled(True)
        else:
            self.passwrd_in.setStyleSheet('border : 2px solid red')
            self.cnx.setEnabled(False)

        if len(self.username_in.text()) > 2 and len(self.passwrd_in.text()) > 2:
            self.cnx.setEnabled(True)
        else:
            self.cnx.setEnabled(False)



