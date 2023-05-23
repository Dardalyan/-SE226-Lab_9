import sys
import mysql.connector
from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QFont

#-----------------------------------------------------------------------------------------------------------------------
# TASK 1
try:
    f = open('Marvel.txt','r')
except:
    raise FileNotFoundError

marvelMovies = []

for i in f.readlines():
    temp = i.split()
    movie = dict()
    movie["id"]= temp[0]
    movie["movie"]=temp[1]
    movie["date"]=temp[2]
    movie["mcu phase"]= temp[3]
    marvelMovies.append(movie)
#-----------------------------------------------------------------------------------------------------------------------

# TASK 2
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

cursor = mydb.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS LAB9")

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="LAB9"
)

cursor = connection.cursor()
if connection.is_connected():
    print("Connected to mysql database, waiting for your orders...\n")


tableCommand = """
CREATE TABLE IF NOT EXISTS marvel(

id int NOT NULL,
movie varchar(255) NOT NULL,
movie_date varchar(255) NOT NULL,
phase varchar(255),
primary key(id)
)
"""
cursor.execute(tableCommand)
#-----------------------------------------------------------------------------------------------------------------------

# TASK 3
insertCommand = """
INSERT INTO marvel(id,movie,movie_date,phase) VALUES (%s,%s,%s,%s)
"""
for movie in marvelMovies:
    id = movie["id"]
    movie_name = movie["movie"]
    date = movie["date"]
    phase = movie["mcu phase"]
    cursor.execute(insertCommand,(id,movie_name,date,phase))

selectById = """
SELECT * FROM marvel WHERE id = %s
"""

selectAll = """
SELECT * FROM marvel
"""
#-----------------------------------------------------------------------------------------------------------------------

# TASK 4

application = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
window.setFixedSize(600,800)

addButton = QtWidgets.QPushButton("ADD")
listAllButton = QtWidgets.QPushButton("LIST ALL")
dropDownList = QtWidgets.QComboBox()
textBox = QtWidgets.QTextBrowser()

#Textbox Font
textBox.setFont(QFont("Times New Roman",12))


#-----------------------------------------------------------------------------------------------------------------------

# TASK 5

#Drop Down List with ids'
dropDownList.setFixedSize(50,30)
cursor.execute(selectAll)
movies= cursor.fetchall()
length = len(movies)
for i in range(1,length+1):
    dropDownList.addItem(str(i))

def getId(text):
    try:
        cursor.execute(selectById,(text,))
        movie = cursor.fetchone()
    except:
        raise mysql.connector.errors.Error()

    textBox.clear()
    movie_content = ""
    for i in movie:
        movie_content += str(i)
        movie_content+="  "

    textBox.append(movie_content)


dropDownList.activated[str].connect(getId)
#-----------------------------------------------------------------------------------------------------------------------


# TASK 6
addButton.setFixedSize(200,50)

def addNewMovie():
    popUp = QtWidgets.QDialog()
    popUp.setFixedSize(400,500)

    OK = QtWidgets.QPushButton("OK")
    CANCEL = QtWidgets.QPushButton("Cancel")

    name_input = QtWidgets.QLineEdit()
    name_label = QtWidgets.QLabel("MOVIE NAME:")

    date_input = QtWidgets.QLineEdit()
    date_label = QtWidgets.QLabel("DATE:")

    phase_input = QtWidgets.QLineEdit()
    phase_label = QtWidgets.QLabel("PHASE:")

    name_layout = QtWidgets.QHBoxLayout()
    name_layout.addWidget(name_label)
    name_layout.addWidget(name_input)

    date_layout = QtWidgets.QHBoxLayout()
    date_layout.addWidget(date_label)
    date_layout.addWidget(date_input)

    phase_layout = QtWidgets.QHBoxLayout()
    phase_layout.addWidget(phase_label)
    phase_layout.addWidget(phase_input)

    horizantal_layout = QtWidgets.QHBoxLayout()
    vertical_layout = QtWidgets.QVBoxLayout()
    upper_layout = QtWidgets.QVBoxLayout()

    upper_layout.addLayout(name_layout)
    upper_layout.addLayout(date_layout)
    upper_layout.addLayout(phase_layout)

    vertical_layout.addLayout(upper_layout)
    vertical_layout.addLayout(horizantal_layout)
    horizantal_layout.addWidget(OK)
    horizantal_layout.addWidget(CANCEL)

    popUp.setLayout(vertical_layout)

    def popUpOk():
        """
            You need to click the button "List All" to see new added item .
        """
        cursor.execute(selectAll)
        movielist = cursor.fetchall()
        length = len(movielist)
        new_id = length+1

        name = name_input.text()
        date = date_input.text()
        phase = phase_input.text()

        cursor.execute(insertCommand,(new_id,name,date,phase))

        cursor.execute(selectAll)
        movies = cursor.fetchall()
        length = len(movies)
        for i in range(1, length + 1):
            dropDownList.addItem(str(i))

        popUp.close()

    def popUpCancel():
        popUp.close()

    OK.clicked.connect(popUpOk)
    CANCEL.clicked.connect(popUpCancel)

    popUp.show()
    popUp.exec_()

addButton.clicked.connect(addNewMovie)



#-----------------------------------------------------------------------------------------------------------------------

# TASK 7
listAllButton.setFixedSize(200,50)
def listAllMovies():
    cursor.execute(selectAll)
    moviesList = cursor.fetchall()
    textBox.clear()
    for i in moviesList:
        movie = ""
        for j in i :
            movie+= str(j)
            movie+="  "
        textBox.append(movie)

listAllButton.clicked.connect(listAllMovies)

#-----------------------------------------------------------------------------------------------------------------------


#Layouts
context = QtWidgets.QVBoxLayout()
layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.LeftToRight)
textLayout = QtWidgets.QHBoxLayout()

#Layout Process
layout.addWidget(addButton)
layout.addWidget(dropDownList)
layout.addWidget(listAllButton)
textLayout.addWidget(textBox)
context.addLayout(layout)
context.addLayout(textLayout)


window.setLayout(context)
window.show()
sys.exit(application.exec_())








