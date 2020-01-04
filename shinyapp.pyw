from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore
import requests
import pathlib

app = QApplication([])

count_label = QLabel()
count_label.setText("0")

encounters_box = QLineEdit()
pokemon_box = QLineEdit()
top_box = QCheckBox()
title_box = QCheckBox()

pokedex = {}
with open("pokedex.txt", "r") as f:
    for line in f:
        (val, key) = line.strip().split(" ", 1)
        pokedex[str(key.lower())] = val


with open("preferences.txt", "r") as f:
    lines = f.readlines()
    if lines == []:
        pokemon = "unknown"
    elif lines[1].strip() == "":
        pokemon = "unknown"
    else:
        pokemon = lines[1].strip().lower()
        pokemon_box.setText(lines[1].strip())


if pokemon != "unknown":
    path = pathlib.Path(pokemon + ".png")
    if path.exists() == False:
        id = str(pokedex[pokemon])
        if "a" in id:
            gen = "SM/"
        if "g" in id:
            gen = "SWSH/"
        if "a" not in id and "g" not in id:
            if int(id) < 810:
                gen = "SM/"
            else:
                gen = "SWSH/"

        url = "https://www.serebii.net/Shiny/" + gen + id + ".png"
        shinyfile = requests.get(url)
        shinyname = pokemon + ".png"
        open(shinyname, "wb").write(shinyfile.content)

image_label = QLabel()
mon_pixmap = QPixmap(pokemon + ".png")
mon_pixmap = mon_pixmap.scaled(128, 128, QtCore.Qt.KeepAspectRatio)
image_label.setPixmap(mon_pixmap)




shine_pixmap = QPixmap("shine.png")

gear_icon = QPixmap("settings.png")
gear_icon = gear_icon.scaled(96, 96, QtCore.Qt.KeepAspectRatio)

settings = QWidget()
settings.setWindowTitle("Settings")
settings.setWindowIcon(QIcon(gear_icon))
settings_layout = QFormLayout()

def encounters_changed():
    count_label.setText(str(encounters_box.text()))



def save_clicked():
    with open("preferences.txt", "w") as f:
        f.write(str(encounters_box.text()))
        f.write("\n")
        f.write(str(pokemon_box.text()))
        f.write("\n")
        f.write(str(top_box.isChecked()))
        f.write("\n")
        f.write(str(title_box.isChecked()))

    count_label.setText(str(encounters_box.text()))

    if top_box.isChecked() == True:
        window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        settings.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        if title_box.isChecked() == True:
            window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
    if title_box.isChecked() == True and top_box.isChecked() == False:
        window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    if top_box.isChecked() == False and title_box.isChecked() == False:
        window.setWindowFlags(window.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
        window.setWindowFlags(window.windowFlags() & ~QtCore.Qt.FramelessWindowHint)

    pokemon = pokemon_box.text().lower()
    if pokemon != "unknown":
        path = pathlib.Path(pokemon + ".png")
        if path.exists() == False:
            id = str(pokedex[pokemon])
            if "a" in id:
                gen = "SM/"
            if "g" in id:
                gen = "SWSH/"
            if "a" not in id and "g" not in id:
                if int(id) < 810:
                    gen = "SM/"
                else:
                    gen = "SWSH/"

            url = "https://www.serebii.net/Shiny/" + gen + id + ".png"
            shinyfile = requests.get(url)
            shinyname = pokemon + ".png"
            open(shinyname, "wb").write(shinyfile.content)
    mon_pixmap = QPixmap(pokemon + ".png")
    mon_pixmap = mon_pixmap.scaled(128, 128, QtCore.Qt.KeepAspectRatio)
    image_label.setPixmap(mon_pixmap)

    window.show()

    settings.hide()

save_button = QPushButton()
save_button.setText("Save changes")
save_button.clicked.connect(save_clicked)

settings_layout.addRow("Encounters:", encounters_box)
settings_layout.addRow("Pokemon:", pokemon_box)
settings_layout.addRow(QLabel("Please specify regional forms eg 'Darumaka-Galar'"))
settings_layout.addRow("Always on top", top_box)
settings_layout.addRow("Remove title bar", title_box)
settings_layout.addRow(save_button)
settings.setLayout(settings_layout)



def settings_clicked():
    encounters_box.setText(count_label.text())
    settings.show()

settings_button = QPushButton()
settings_button.setIcon(QIcon(gear_icon))
settings_button.clicked.connect(settings_clicked)


def up_clicked():
    count_label.setText(str((int(count_label.text()) + 1)))

def down_clicked():
    if (int(count_label.text()) - 1) >= 0:
        count_label.setText(str((int(count_label.text()) - 1)))


up_button = QPushButton("+ 1")
up_button.clicked.connect(up_clicked)

down_button = QPushButton("- 1")
down_button.clicked.connect(down_clicked)


layout = QHBoxLayout()
layout.addWidget(image_label)
layout.addWidget(count_label)
layout.addWidget(up_button)
layout.addWidget(down_button)
layout.addWidget(settings_button)

window = QWidget()
window.setWindowTitle("Counter")
window.setWindowIcon(QIcon(shine_pixmap))
window.setLayout(layout)

with open("preferences.txt", "r") as f:
    lines = f.readlines()
    if lines != []:

        if lines[0].strip() == "":
            count_label.setText("0")
        else:
            count_label.setText(str(lines[0].strip()))

        if lines[2].strip() == "True" and lines[3].strip() == "True":
            window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
            settings.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            top_box.setChecked(True)
            title_box.setChecked(True)
        if lines[2].strip() == "True" and lines[3].strip() == "False":
            window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            settings.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            top_box.setChecked(True)
        if lines[2].strip() == "False" and lines[3].strip() == "True":
            window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            title_box.setChecked(True)

window.show()

def exit_process():
    with open("preferences.txt", "r") as f:
        lines = f.readlines()
    with open("preferences.txt", "w") as f:
        f.write(str(count_label.text()))
        f.write("\n")
        f.write(lines[1])
        f.write(lines[2])
        f.write(lines[3])


app.aboutToQuit.connect(exit_process)

app.exec_()



