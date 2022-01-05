from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from DB import DB
import pathlib
import os
import time
from datetime import datetime
import configparser

from JSON_to_DB import JSON_to_DB


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1036, 646)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(370, 10, 281, 61))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.label.setFont(font)
        self.label.setAutoFillBackground(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(320, 90, 701, 521))
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tournament_table = QtWidgets.QTableWidget(self.tab)
        self.tournament_table.setGeometry(QtCore.QRect(10, 10, 671, 471))
        self.tournament_table.setObjectName("tableView_2")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.players_table = QtWidgets.QTableWidget(self.tab_2)
        self.players_table.setGeometry(QtCore.QRect(10, 10, 671, 471))
        self.players_table.setObjectName("tableView")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.player_dropdown = QtWidgets.QComboBox(self.tab_3)
        self.player_dropdown.setGeometry(QtCore.QRect(90, 10, 241, 31))
        self.player_dropdown.setObjectName("comboBox")
        self.label_4 = QtWidgets.QLabel(self.tab_3)
        self.label_4.setGeometry(QtCore.QRect(20, 10, 61, 31))
        self.label_4.setObjectName("label_4")
        self.player_table = QtWidgets.QTableWidget(self.tab_3)
        self.player_table.setGeometry(QtCore.QRect(20, 50, 661, 431))
        self.player_table.setObjectName("tableView_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.game_dropdown = QtWidgets.QComboBox(self.tab_4)
        self.game_dropdown.setGeometry(QtCore.QRect(60, 10, 271, 31))
        self.game_dropdown.setObjectName("comboBox_2")
        self.game_table = QtWidgets.QTableWidget(self.tab_4)
        self.game_table.setGeometry(QtCore.QRect(20, 50, 661, 431))
        self.game_table.setObjectName("tableView_4")
        self.label_5 = QtWidgets.QLabel(self.tab_4)
        self.label_5.setGeometry(QtCore.QRect(20, 10, 41, 31))
        self.label_5.setObjectName("label_5")
        self.tabWidget.addTab(self.tab_4, "")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 30, 281, 121))
        self.groupBox.setObjectName("groupBox")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(80, 40, 180, 21))
        self.label_8.setObjectName("label_8")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 91, 21))
        self.label_2.setObjectName("label_2")
        self.db_name = QtWidgets.QLabel(self.groupBox)
        self.db_name.setGeometry(QtCore.QRect(110, 20, 120, 21))
        self.db_name.setObjectName("label_3")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(10, 40, 131, 21))
        self.label_7.setObjectName("label_7")
        self.load_db = QtWidgets.QPushButton(self.groupBox)
        self.load_db.setGeometry(QtCore.QRect(20, 70, 251, 31))
        self.load_db.setObjectName("pushButton")
        self.new_tournament = QtWidgets.QPushButton(self.centralwidget)
        self.new_tournament.setGeometry(QtCore.QRect(20, 310, 131, 41))
        self.new_tournament.setObjectName("pushButton_3")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 180, 281, 111))
        self.groupBox_2.setObjectName("groupBox_2")
        self.player_count = QtWidgets.QLabel(self.groupBox_2)
        self.player_count.setGeometry(QtCore.QRect(120, 80, 21, 21))
        self.player_count.setObjectName("label_13")
        self.label_10 = QtWidgets.QLabel(self.groupBox_2)
        self.label_10.setGeometry(QtCore.QRect(10, 50, 101, 21))
        self.label_10.setObjectName("label_10")
        self.label_12 = QtWidgets.QLabel(self.groupBox_2)
        self.label_12.setGeometry(QtCore.QRect(10, 80, 101, 21))
        self.label_12.setObjectName("label_12")
        self.game_count = QtWidgets.QLabel(self.groupBox_2)
        self.game_count.setGeometry(QtCore.QRect(120, 20, 21, 21))
        self.game_count.setObjectName("label_9")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(10, 20, 101, 21))
        self.label_6.setObjectName("label_6")
        self.team_count = QtWidgets.QLabel(self.groupBox_2)
        self.team_count.setGeometry(QtCore.QRect(120, 50, 21, 21))
        self.team_count.setObjectName("label_11")
        self.add_game_btn = QtWidgets.QPushButton(self.centralwidget)
        self.add_game_btn.setGeometry(QtCore.QRect(170, 310, 131, 41))
        self.add_game_btn.setObjectName("pushButton_6")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 430, 281, 171))
        self.groupBox_3.setObjectName("groupBox_3")
        self.progressBar = QtWidgets.QProgressBar(self.groupBox_3)
        self.progressBar.setGeometry(QtCore.QRect(10, 140, 261, 23))
        self.progressBar.setProperty("value", 100)
        self.progressBar.setObjectName("progressBar")
        self.program_log = QtWidgets.QTextEdit(self.groupBox_3)
        self.program_log.setGeometry(QtCore.QRect(10, 20, 261, 111))
        self.program_log.setObjectName("textEdit")
        self.program_log.setDisabled(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.populate_table_headers()
        self.cfg = 'config.ini'

        if(os.path.exists(self.cfg) == False):
            self.modify_cfg('DEFAULT','db','tournament_stats.db')
        else:
            db_path = self.fetch_cfg('DEFAULT', 'db')
            if os.path.exists(db_path):
                self.db = db_path
            else: 
                self.new_db()
                
        self.reload_data()
        self.add_functions()
        self.db_name.setText(self.db.split("/")[-1])
        self.label_8.setText(time.ctime(os.path.getmtime(self.db)))
        self.log_status("Loaded DB: {}".format(self.db.split("/")[-1]))

        self.tournament_table.verticalHeader().setVisible(False)
        self.players_table.verticalHeader().setVisible(False)
        self.player_table.verticalHeader().setVisible(False)
        self.game_table.verticalHeader().setVisible(False)
        self.player_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.game_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def add_functions(self):
        self.player_dropdown.currentTextChanged.connect(self.populate_player_table)
        self.game_dropdown.currentTextChanged.connect(self.populate_game_table)

        self.load_db.clicked.connect(self.load_existing_db)
        self.new_tournament.clicked.connect(self.new_db)
        self.add_game_btn.clicked.connect(self.add_game)    
    
    def modify_cfg(self, section, key, value):
        config = configparser.ConfigParser()
        config.read(self.cfg)
        config[section][key] = str(value)
        with open(self.cfg, 'w') as configfile: config.write(configfile)
    
    def fetch_cfg(self, section, key):
        config = configparser.ConfigParser()
        config.read(self.cfg)
        return config[section][key]

    def load_existing_db(self):
        mypath = pathlib.Path().resolve()
        db_path = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, 'Open file', str(mypath), "Database files (*.db)")[0]
        if db_path != '':
            self.db_name.setText(db_path.split("/")[-1])
            self.label_8.setText(time.ctime(os.path.getmtime(db_path)))
            self.reload_data(db_path=db_path)
            self.modify_cfg('DEFAULT','db',db_path.split("/")[-1])
            self.log_status("Loaded DB: {}".format(db_path.split("/")[-1]))

    def new_db(self):
        mypath = pathlib.Path().resolve()
        self.db = QtWidgets.QFileDialog.getSaveFileName(self.centralwidget, 'Save file', str(mypath), "Database files (*.db)")[0]
        if self.db != '':
            self.reload_data(db_path=self.db, empty = True)
            self.db_name.setText(self.db.split("/")[-1])
            self.label_8.setText(time.ctime(os.path.getmtime(self.db)))
            self.modify_cfg('DEFAULT','db', self.db.split("/")[-1])
            self.clear_all()
            self.log_status("Loaded DB: {}".format(self.db.split("/")[-1]))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "LFL Analīze"))
        self.label.setText(_translate("MainWindow", "LFL Analīze"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Turnīra tabula"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Rezultatīvāko spēlētāju tabula"))
        self.label_4.setText(_translate("MainWindow", "Spēlētājs:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Spēlētāja vēsture"))
        self.label_5.setText(_translate("MainWindow", "Spēle:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Spēļu gaita"))
        self.groupBox.setTitle(_translate("MainWindow", "Izmantotie dati:"))
        self.label_8.setText(_translate("MainWindow", "-"))
        self.label_2.setText(_translate("MainWindow", "Šobrīd izmanto:"))
        self.db_name.setText(_translate("MainWindow", "-"))
        self.label_7.setText(_translate("MainWindow", "Atjaunots:"))
        self.load_db.setText(_translate("MainWindow", "Ielādēt"))
        self.new_tournament.setText(_translate("MainWindow", "Jauns turnīrs"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Izmantoto datu kopskats"))
        self.player_count.setText(_translate("MainWindow", "-"))
        self.label_10.setText(_translate("MainWindow", "Komandu skaits:"))
        self.label_12.setText(_translate("MainWindow", "Spēlētāju skaits:"))
        self.game_count.setText(_translate("MainWindow", "-"))
        self.label_6.setText(_translate("MainWindow", "Ielādētas spēles:"))
        self.team_count.setText(_translate("MainWindow", "-"))
        self.add_game_btn.setText(_translate("MainWindow", "Pievienot spēles"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Programmas statuss"))

    def populate_dropdowns(self):
        db = DB(test_mode=False, db_path=self.db)
        games, players = db.get_dropdown_data()
        self.player_dropdown.clear()
        self.game_dropdown.clear()
        for line in players:
            self.player_dropdown.addItem("{}, {} ({}) - {}".format(line[0], line[1], line[2], line[3]))
        teams = []
        for game in games:
            self.game_dropdown.addItem("{} - {}".format(game[0], game[1]))
            teams.append(game[0])
            teams.append(game[1])
        teams = list(dict.fromkeys(teams))
        self.player_count.setText(str(len(players)))
        self.game_count.setText(str(len(games)))
        self.team_count.setText(str(len(teams)))
        db.close_connecton()

    def log_status(self, text):
        current_time = datetime.now().strftime("%H:%M:%S")
        log_message = "[{}]: {}\n".format(current_time, text)
        existing_log = self.program_log.toPlainText()
        self.program_log.setText(existing_log + log_message)

    def add_game(self):
        self.progressBar.setProperty("value", 0)
        mypath = pathlib.Path().resolve()
        game_path = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, 'Open file', str(mypath), "Database files (*.json)")[0]
        if game_path != '':
            db = DB(db_path=self.db)
            JSON_to_DB(db, game_path)
            self.reload_data()
            self.progressBar.setProperty("value", 100)
            db.close_connecton()

    def clear_all(self):
        self.tournament_table.setRowCount(0)
        self.player_table.setRowCount(0)
        self.players_table.setRowCount(0)
        self.game_table.setRowCount(0)
        self.player_dropdown.clear()
        self.game_dropdown.clear()
        self.player_count.setText("-")
        self.game_count.setText("-")
        self.team_count.setText("-")

    def reload_data(self, db_path = None, empty = False):
        if db_path == None:
            db = DB(db_path = self.db, empty = empty)
        else: 
            db = DB(db_path = db_path, empty = empty)
            self.db = db_path
        if not empty: 
            self.populate_dropdowns()
            self.populate_tournament_table(db)
            self.populate_players_table(db)
            self.populate_player_table()
            self.populate_game_table()
        db.close_connecton()

    def populate_tournament_table(self, db):
        self.tournament_table.setRowCount(0)

        data = db.get_tournament_data()
        tp = {}
        for game in data:
            otwin = game[1]
            points_dict = game[0]
            w = max(points_dict)
            l = min(points_dict)
            # Structure: [points, wins_base, wins_extra, loss_base, loss_extra]
            if otwin:
                if w in tp.keys():
                    tp[w][0] += 3
                    tp[w][2] += 1
                else:
                    tp[w] = [3,0,1,0,0]
                if l in tp.keys():
                    tp[l][0] += 2
                    tp[l][4] += 1
                else:
                    tp[l] = [2,0,0,0,1]
            else:
                if w in tp.keys():
                    tp[w][0] += 5
                    tp[w][1] += 1
                else:
                    tp[w] = [5,1,0,0,0]
                if w in tp.keys():
                    tp[l][0] += 1
                    tp[l][3] += 1
                else:
                    tp[l] = [1,0,0,1,0]
        spots = []
        places = {}
        for t in tp: spots.append(tp[t][0])
        curr_place = 1
        for spot in list(reversed(sorted(spots))):
            if spot in places.keys(): 
                curr_place += 1
            else: 
                places[spot] = curr_place
                curr_place += 1

        for t in tp:
            self.addTableRow(self.tournament_table, [places[tp[t][0]], t, tp[t][0], tp[t][1], tp[t][3], tp[t][2], tp[t][4]])
        self.tournament_table.sortItems(0, QtCore.Qt.AscendingOrder)

    def populate_players_table(self,db):
        self.players_table.setRowCount(0)

        from operator import itemgetter
        players_data = db.get_players_data()
        places = []
        for p in players_data: places.append((p, players_data[p][0] + players_data[p][2], players_data[p][1]))
        order = {}
        for idx, spot in enumerate(list(reversed(sorted(places, key=itemgetter(1,2))))):
            order[spot[0]] = idx + 1
        for p in players_data:
            self.addTableRow(self.players_table, [order[p], players_data[p][3]
                                                , players_data[p][4]
                                                , players_data[p][5]
                                                , players_data[p][0] + players_data[p][2]
                                                , players_data[p][1]])

        self.players_table.sortItems(0, QtCore.Qt.AscendingOrder)
        self.players_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def populate_player_table(self):
        self.player_table.setRowCount(0)
        db = DB(test_mode=False, db_path=self.db)
        p_cred = self.player_dropdown.currentText()
        if p_cred != None and p_cred != "":
            Nr = p_cred.split('(')[1].split(')')[0]
            team = p_cred.split(' - ')[1]
            data = db.get_player_data(Nr, team)
            if data != None:
                for d in data:
                    self.addTableRow(self.player_table, [d[2], d[1], d[0]])
        db.close_connecton()

    def populate_game_table(self):
        self.game_table.setRowCount(0)
        db = DB(test_mode=False, db_path=self.db)
        game = self.game_dropdown.currentText()
        if game != None and game != "":
            [team_A, team_B] = game.split(' - ')

            data = db.get_game_data(team_A, team_B)
            if data != None:
                for d in data:
                    self.addTableRow(self.game_table, [d[0], d[1], d[2], d[3]])
        db.close_connecton()

    def addTableRow(self, table, row_data):
        row = table.rowCount()
        table.setRowCount(row+1)
        col = 0
        for item in row_data:
            if type(item) == int:
                new_item = QtWidgets.QTableWidgetItem()
                new_item.setData(QtCore.Qt.DisplayRole, item)
                cell = QTableWidgetItem(new_item)
            else:
                cell = QTableWidgetItem(str(item))
            table.setItem(row, col, cell)
            col += 1

    def populate_table_headers(self):
        # Tournament table
        cols = ['Vieta','Komanda','Punkti','Uzvaras \npamatlaikā','Zaudējumi \npamatlaikā','Uzvaras \npapildlaikā','Zaudējumi \npapildlaikā']
        self.tournament_table.setColumnCount(len(cols))
        self.tournament_table.setHorizontalHeaderLabels(cols)
        col_width = int(self.tournament_table.width() / len(cols))
        for i in range(len(cols)):
            self.tournament_table.setColumnWidth(i, col_width)

        # All-players table
        cols = ['Vieta','Vārds','Uzvārds','Komanda','Gūtie vārti','Rezultatīvās\n piespēles']
        self.players_table.setColumnCount(len(cols))
        self.players_table.setHorizontalHeaderLabels(cols)
        col_width = int(self.players_table.width() / len(cols))
        for i in range(len(cols)):
            self.players_table.setColumnWidth(i, col_width)

        # Game events table
        cols = ['Spēlētājs', 'Nr', 'Laiks','Notikums']
        self.game_table.setColumnCount(len(cols))
        self.game_table.setHorizontalHeaderLabels(cols)
        col_width = int(self.game_table.width() / len(cols))
        for i in range(len(cols)):
            self.game_table.setColumnWidth(i, col_width)

        # Single player table
        cols = ['Spēle','Laiks','Notikums']
        self.player_table.setColumnCount(len(cols))
        self.player_table.setHorizontalHeaderLabels(cols)
        col_width = int(self.player_table.width() / len(cols))
        for i in range(len(cols)):
            self.player_table.setColumnWidth(i, col_width)

def run_UI():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

