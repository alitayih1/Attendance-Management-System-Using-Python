import sys
import os.path

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QIcon
import PyQt5.QtCore as QtCore
# from PyQt5.QtWidgets import QApplication, QWidget

import csv2mysql


class App(QWidget):
    
    def __init__(self):
        super().__init__()
        

        self.position = (300, 100)
        self.dimensions = (420, 300)
        
        self.setGeometry(*self.position, *self.dimensions)
        self.setWindowTitle('CSV to MySQL')
        self.setWindowIcon(QIcon('icon.svg'))
        QApplication.setFont(QFont('Helvetica', pointSize=10))
        QToolTip.setFont(QFont('Helvetica', pointSize=11))

        # 'User' field input
        self.usr_lbl = QLabel('User')
        self.usr_lbl.setToolTip('Name of the user of MySQL server.')
        self.usr_txtbox = QLineEdit()

        # 'Password' field input
        self.pswd_lbl = QLabel('Password')
        self.pswd_lbl.setToolTip('Password of the user of MySQL server.')
        self.pswd_txtbox = QLineEdit()

        # 'Database' field input
        self.db_lbl = QLabel('Database')
        self.db_lbl.setToolTip('Name of the database to access.')
        self.db_txtbox = QLineEdit()

        # 'Table' field input
        self.table_lbl = QLabel('Table')
        self.table_lbl.setToolTip('Name of the table into which to write values.')
        self.table_txtbox = QLineEdit()       

        self.connection_box = QGridLayout()
        self.connection_box.addWidget(self.usr_lbl, 0, 0, alignment=QtCore.Qt.Alignment(2))
        self.connection_box.addWidget(self.usr_txtbox, 0, 1)
        self.connection_box.addWidget(self.pswd_lbl, 0, 3, alignment=QtCore.Qt.Alignment(2))
        self.connection_box.addWidget(self.pswd_txtbox, 0, 4)
        self.connection_box.addWidget(self.db_lbl, 1, 0, alignment=QtCore.Qt.Alignment(2))
        self.connection_box.addWidget(self.db_txtbox, 1, 1)
        self.connection_box.addWidget(self.table_lbl, 1, 3, alignment=QtCore.Qt.Alignment(2))
        self.connection_box.addWidget(self.table_txtbox, 1, 4)

        self.connection_box.setColumnStretch(0, 4)
        self.connection_box.setColumnStretch(1, 12)
        self.connection_box.setColumnStretch(2, 1)
        self.connection_box.setColumnStretch(3, 4)
        self.connection_box.setColumnStretch(4, 12)

        self.connection_box.setVerticalSpacing(15)


        # 'Path' field input
        self.path_lbl = QLabel('Path to CSV file')
        self.path_lbl.setToolTip('Absolute path to the CSV file to be uploaded into MySQL table.')
        self.path_txtbox = QLineEdit()

        # 'Datatype' field input
        self.dtyp_lbl = QLabel('Datatype for columns')
        self.dtyp_lbl.setToolTip('Assign which datatypes each column contains. \n' +\
                                'If all collumns are same datatype then just type in one type (e.g. "int" for integers). \n' +\
                                'If all collumns aren\'t same datatype then seperate type for each column with ' +\
                                'a space[" "], a comma[","] or a semicolon[";"] \n' +\
                                '(e.g. "int str" for first column containing integers and second column containing strings).'
                                )
        self.dtyp_txtbox = QLineEdit()

        # 'Header' check box
        self.header_check = QCheckBox('first row in CSV file is header')
        self.header_check.setToolTip('Mark true if the first row in the CSV file contains names of columns in MySQL table.')
        
        # 'Enum' check box
        self.enum_check = QCheckBox('enumerate values from CSV file')
        self.enum_check.setToolTip('Mark true if the values from the CSV file are to be enumerated.')

        self.upload_box = QGridLayout()
        self.upload_box.addWidget(self.path_lbl, 0, 0, alignment=QtCore.Qt.Alignment(2))
        self.upload_box.addWidget(self.path_txtbox, 0, 1)
        self.upload_box.addWidget(self.dtyp_lbl, 1, 0, alignment=QtCore.Qt.Alignment(2))
        self.upload_box.addWidget(self.dtyp_txtbox, 1, 1)

        self.upload_box.setVerticalSpacing(15)

        # 'Upload' button
        self.up_btn = QPushButton('Upload')
        self.up_btn.setToolTip('Upload data from the CSV file to the MySQL database')
        self.up_btn.setDefault(True)
        self.up_btn.setAutoDefault(True)
        self.up_btn.clicked.connect(self.upload)


        self.window_layout = QVBoxLayout(self)
        self.window_layout.addLayout(self.connection_box)
        self.window_layout.addLayout(self.upload_box)
        self.window_layout.addWidget(self.header_check)
        self.window_layout.addWidget(self.enum_check)
        self.window_layout.addWidget(self.up_btn)

        self.window_layout.setContentsMargins(20, 20, 20, 20)

        self.show()

    def upload(self):
        user = self.usr_txtbox.displayText()
        passwd = self.pswd_txtbox.displayText()
        db = self.db_txtbox.displayText()
        table = self.table_txtbox.displayText()
        path2csv = self.path_txtbox.displayText().replace('"', '')

        castvartypes = self.dtyp_txtbox.displayText()
        if ',' in castvartypes or ';' in castvartypes or ' ' in castvartypes:
            castvartypes = castvartypes.replace(';', ',').replace(' ', ',')
            castvartypes = castvartypes.replace(',,', ',').replace(',,', ',').split(',')

        first_row_is_header = self.header_check.checkState()
        enum = self.enum_check.checkState()

        if os.path.isabs(path2csv):
            csv_loaded = csv2mysql.load_csv(path2csv, castvartypes=castvartypes, first_row_is_header=first_row_is_header)
            sql_commands = csv2mysql.plist2sql(csv_loaded, first_row_is_header=first_row_is_header, table=table, enum=enum)

            for row in sql_commands:
                print(row)

            csv2mysql.write2mysql(user, passwd, db, sql_commands)
        else:
            warning_dialog = QMessageBox()
            warning_dialog.setText('Path to CSV file must be an absolute path!!!')
            warning_dialog.setIcon(2)
            warning_dialog.exec()

        
        

        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())