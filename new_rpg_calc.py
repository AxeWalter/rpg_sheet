import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QMessageBox, QFileDialog, QGridLayout, QHBoxLayout, QVBoxLayout, QComboBox, QProgressBar
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
from PIL import Image
from random import randint
import io
import os
from project.configs.db_functions import CharactersTable, InitialInsert, BaseStatsTable, AttributesTable, AttributesProgressBarTable


img_blob = None

def check_positive(value, field):
    try:
        value = int(value)
        if value < 0:
            raise Exception(f"Please, insert a positive integer for {field}.")
        return value
    except ValueError:
        raise ValueError(f"Please insert an integer value for {field}. No points, commas, or letters!")


def create_character():
    name = new_char_box1.text().lower()
    if not name.strip():
        QMessageBox.warning(None, "NoNoNo!", "Please, insert a valid name.")
    elif len(name) < 2 or len(name) > 30:
        QMessageBox.warning(None, "NoNoNo!", "Please, name must be between 2 and 50 characters long.")
    elif len(CharactersTable().select_name(name)) != 0:
        QMessageBox.warning(None, "NoNoNo!", "This name is already taken. Try another one.")
    elif img_blob is None:
        QMessageBox.warning(None, "NoNoNo!", "Please, insert an image!")
    else:
        try:
            total_xp = check_positive(new_char_box2.text(), "Total_XP")
            hp = check_positive(new_char_box4.text(), "HP")
            stamina = check_positive(new_char_box5.text(), "Stamina")
            ac = check_positive(new_char_box6.text(), "AC")
            armor = check_positive(new_char_box7.text(), "Armor")
            strg = check_positive(new_char_box8.text(), "STR")
            wis = check_positive(new_char_box9.text(), "WIS")
            dex = check_positive(new_char_box10.text(), "DEX")
            inte = check_positive(new_char_box11.text(), "INT")
            cons = check_positive(new_char_box12.text(), "CONS")
            char = check_positive(new_char_box13.text(), "CHAR")
            str_bar = check_positive(new_char_box14.text(), "Progress for STR point")
            wis_bar = check_positive(new_char_box15.text(), "Progress for WIS point")
            dex_bar = check_positive(new_char_box16.text(), "Progress for DEX point")
            int_bar = check_positive(new_char_box17.text(), "Progress for INT point")
            cons_bar = check_positive(new_char_box18.text(), "Progress for CONS point")
            char_bar = check_positive(new_char_box19.text(), "Progress for CHAR point")

            InitialInsert().insert(name, total_xp, img_blob, hp, stamina, ac, armor, strg, dex, cons, wis, inte, char,
                                   str_bar, dex_bar, cons_bar, wis_bar, int_bar, char_bar)

            to_mw(new_char_window, name)
        except ValueError as error1:
            QMessageBox.warning(None, "NoNoNo!", str(error1))

        except Exception as error2:
            QMessageBox.warning(None, "NoNoNo!", str(error2))


def select_image():
    global img_blob
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    image_popup = QFileDialog.getOpenFileName(None, caption='Select Image', directory=desktop_path, filter='Image Files (*.png *.jpg)')
    image_path = image_popup[0]
    new_char_box3.setText(image_path)

    if image_path:
        file_extension = os.path.splitext(image_path)[1].lower()
        if file_extension == ".png":
            image_format = "PNG"
        elif file_extension == ".jpg" or file_extension == ".jpeg":
            image_format = "JPEG"

        try:
            with Image.open(image_path) as image:
                image_resized = image.resize((250, 250))
                byte_array = io.BytesIO()
                image_resized.save(fp= byte_array, format= image_format)
                img_blob = byte_array.getvalue()


        except Exception as e:
            QMessageBox.warning(None, "Big Error boy!", f"Error {e}")
    else:
        new_char_box3.setText("Image")
        QMessageBox.information(None, "NoNoNo!", "No images where selected.")


def dropdown_list():
    characters = CharactersTable().select_names()
    character_list = []
    for character in characters:
        character_list.append(character.name)
    return character_list


def iw_to_new_character():
    global img_blob
    iw.hide()
    for widget in new_char_window.findChildren(QLineEdit):
        widget.clear()
    img_blob = None
    new_char_box3.setText("Image")
    new_char_box1.setFocus()
    QTimer.singleShot(1, lambda: new_char_box1.clearFocus())
    new_char_window.show()


def new_character_to_iw():
    new_char_window.hide()
    iw_dropdown.setCurrentIndex(-1)
    iw.show()


def mw_to_iw():
    mw.hide()
    iw_dropdown.clear()
    iw_dropdown.addItems(dropdown_list())
    iw_dropdown.setCurrentIndex(-1)
    iw.show()


def dice_roll():
    sides = mw.sender()
    if sides.text() == "D10":
        mw_dice_result.setText(f"You rolled: {str(randint(1, 10))}")
        mw_dice_result.setStyleSheet("color: #0052cc; font-size: 20px; font-weight: bold")
    elif sides.text() == "D12":
        mw_dice_result.setText(f"You rolled: {str(randint(1, 12))}")
        mw_dice_result.setStyleSheet("color: #cc7a00; font-size: 20px; font-weight: bold")
    elif sides.text() == "D20":
        mw_dice_result.setText(f"You rolled: {str(randint(1, 20))}")
        mw_dice_result.setStyleSheet("color: #cc0000; font-size: 20px; font-weight: bold")
    mw_dice_result.adjustSize()


def calculate_level(total_xp):
    lvl = 0
    while total_xp >= (lvl + 1) * 100:
        total_xp = total_xp - ((lvl + 1) * 100)
        lvl += 1
    xp_nxt_level = ((lvl + 1) * 100) - total_xp
    return lvl, xp_nxt_level, total_xp


def to_mw(window, get_name):
    name = get_name

    if not name:
        QMessageBox.warning(None, "NoNoNo!", f"No characters were selected.")
        return

    window.hide()

    id = CharactersTable().select_id(name)

    mw_name.setText(f"NAME: {name.upper()}")

    img = CharactersTable().select_image(id)
    qp = QPixmap()
    qp.loadFromData(img)
    mw_image.setPixmap(qp)

    total_xp = CharactersTable().select_total_xp(id)
    mw_totalxp_level.setText(f"TOTAL XP: {total_xp}")

    level = calculate_level(total_xp)[0]
    mw_level.setText(f"LEVEL: {level}")

    xp_nxt_level = calculate_level(total_xp)[1]
    mw_xpnxt_level.setText(f"XP NEXT LEVEL: {xp_nxt_level}")

    hp = BaseStatsTable().select_all(id)[0].hp
    mw_hp.setText(f"HP: {hp}")

    stamina = BaseStatsTable().select_all(id)[0].stamina
    mw_stamina.setText(f"STAMINA: {stamina}")

    ac = BaseStatsTable().select_all(id)[0].ac
    mw_ac.setText(f"AC: {ac}")

    armor = BaseStatsTable().select_all(id)[0].armor
    mw_armor.setText(f"ARMOR: {armor}")

    str = AttributesTable().select_all(id)[0].str
    mw_str.setText(f"STR: {str}")

    wis = AttributesTable().select_all(id)[0].wis
    mw_wis.setText(f"WIS: {wis}")

    dex = AttributesTable().select_all(id)[0].dex
    mw_dex.setText(f"DEX: {dex}")

    int = AttributesTable().select_all(id)[0].int
    mw_int.setText(f"INT: {int}")

    cons = AttributesTable().select_all(id)[0].cons
    mw_cons.setText(f"CONS: {cons}")

    char = AttributesTable().select_all(id)[0].char
    mw_char.setText(f"CHAR: {char}")

    attributes_progress = AttributesProgressBarTable().select_all(id)[0]

    if str <= 20:
        mw_str_progress.setValue(attributes_progress.str_bar)
    else:
        mw_str_progress.setValue(round(attributes_progress.str_bar/2))

    if wis <= 20:
        mw_wis_progress.setValue(attributes_progress.wis_bar)
    else:
        mw_wis_progress.setValue(round(attributes_progress.wis_bar/2))

    if dex <= 20:
        mw_dex_progress.setValue(attributes_progress.dex_bar)
    else:
        mw_dex_progress.setValue(round(attributes_progress.dex_bar/2))

    if int <= 20:
        mw_int_progress.setValue(attributes_progress.int_bar)
    else:
        mw_int_progress.setValue(round(attributes_progress.int_bar/2))

    if cons <= 20:
        mw_cons_progress.setValue(attributes_progress.cons_bar)
    else:
        mw_cons_progress.setValue(round(attributes_progress.cons_bar/2))

    if char <= 20:
        mw_char_progress.setValue(attributes_progress.char_bar)
    else:
        mw_char_progress.setValue(round(attributes_progress.char_bar/2))

    mw_dice_result.clear()
    mw_ep_xp.clear()
    mw_lvl_info.clear()

    mw.show()


def add_xp():
    name = mw_name.text()[6:].lower()
    id = CharactersTable().select_id(name)
    try:
        new_xp_add = int(mw_ep_xp.text())
        if new_xp_add <= 0:
            raise Exception

        old_xp = CharactersTable().select_total_xp(id)
        old_level = calculate_level(old_xp)[0]

        new_xp = old_xp + new_xp_add
        CharactersTable().update_xp(id, new_xp)
        mw_totalxp_level.setText(f"TOTAL XP: {new_xp}")

        new_level = calculate_level(new_xp)[0]
        mw_level.setText(f"LEVEL: {new_level}")

        xp_nxt_level = calculate_level(new_xp)[1]
        mw_xpnxt_level.setText(f"XP NEXT LEVEL: {xp_nxt_level}")

        level_up = new_level - old_level
        if level_up == 0:
            mw_lvl_info.setText("Unfortunately, you didn't level today \n No level up points :)")
            mw_lvl_info.move(390, 240)
        elif level_up == 1:
            mw_lvl_info.setText(f"You have level up {level_up} level \n You have +{level_up} point")
            mw_lvl_info.move(430, 240)
        else:
            mw_lvl_info.setText(f"You have level up {level_up} levels \n You have +{level_up} points")
            mw_lvl_info.move(430, 240)

        mw_lvl_info.adjustSize()

    except ValueError:
        QMessageBox.warning(None, "NoNoNo!", "Please, insert an integer value!")
    except Exception:
        QMessageBox.warning(None, "NoNoNo!", "Please, insert a positive integer value!")


def confirmation():
    confirmation_box = QMessageBox()
    confirmation_box.setWindowTitle("Confirmation")
    confirmation_box.setText("Are you sure you want to perform this action?\nThis will clear all your current level "
                             "progress!")
    confirmation_box.setIcon(QMessageBox.Icon.Question)

    confirmation_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    confirmation_box.setDefaultButton(QMessageBox.StandardButton.No)

    response = confirmation_box.exec()

    if response == QMessageBox.StandardButton.Yes:
        name = mw_name.text()[6:].lower()
        id = CharactersTable().select_id(name)
        old_total_xp = CharactersTable().select_total_xp(id)

        # Here we subtract the surplus XP (lost_xp) of the level (example: LVL 30 with +800XP for next level,
        # we take the 800) from the total old_total_xp. The new value is the total_xp of the character after death.
        lost_xp = calculate_level(old_total_xp)[2]
        new_total_xp = old_total_xp - lost_xp

        # I don't update the level because it's not necessary. When you die you only lose surplus XP, so you can't
        # go down in levels.

        CharactersTable().update_xp(id, new_total_xp)
        mw_totalxp_level.setText(f"TOTAL XP: {new_total_xp}")

        xp_nxt_level = calculate_level(new_total_xp)[1]
        mw_xpnxt_level.setText(f"XP NEXT LEVEL: {xp_nxt_level}")

        mw_lvl_info.setText(f"Died? OMEGALUUUUL!\n You lost {lost_xp} XP")
        mw_lvl_info.move(440, 240)
        mw_lvl_info.adjustSize()


def mw_to_pw():
    if pw.isVisible():
        pw.raise_()
    else:
        for widget in pw.findChildren(QLineEdit):
            widget.clear()
        for widget in pw.findChildren(QLabel):
            widget.setText("")
        pw.show()
        QTimer.singleShot(1, lambda: pw_add_str.clearFocus())


def mw_to_update():
    if update.isVisible():
        update.raise_()
    else:
        for widget in update.findChildren(QLineEdit):
            widget.clear()
        for widget in update.findChildren(QLabel):
            widget.setText("")
        update.show()
        QTimer.singleShot(1, lambda: update_name.clearFocus())

def progress_bar_handling(attribute, progress_bar, pw_add, progress_bar_db, attribute_db, id, mw_attribute, mw_progress_bar):
    #attribute is the attribute we'll be dealing with: str, wis, dex, int, cons, char
    #progress_bar is the progress_bar attribute we'll be dealing: str_bar, wis_bar, dex_bar, int_bar, const_bar, char_bar
    #pw_add is on QLineEdit from the pw window that the users inserts the + value for the progress bar
    #progress_bar_db is the one of the attributes progress bar from the attributes_progress_bar table of the DB
    #attribute_db is one of the attributes from the attributes table of the DB
    #id is the ID from the characters table of the db
    #mw_attribute is one QLineEdit from the mw window that displays the attribute value
    #mw_progress-bar is on QLineEdit ffrom the mw window that dispalys the attribute progress bar

    try:
        add_progress_bar = int(pw_add.text())
        if add_progress_bar < 0:
            raise ValueError
        total_attribute_bar = add_progress_bar + progress_bar_db
        CONST_TOTAL_ATTRIBUTE = attribute_db
        total_attribute = attribute_db
        while total_attribute_bar >= 100:
            if total_attribute <= 20:
                total_attribute_bar = total_attribute_bar - 100
                total_attribute += 1
            elif total_attribute > 20 and total_attribute_bar >= 200:
                total_attribute_bar = total_attribute_bar - 200
                total_attribute += 1
            else:
                break

        AttributesTable().update(attribute, total_attribute, id)
        AttributesProgressBarTable().update(progress_bar, total_attribute_bar, id)

        mw_attribute.setText(f"{attribute.upper()}: {total_attribute}")
        if total_attribute <= 20:
            mw_progress_bar.setValue(total_attribute_bar)
        else:
            mw_progress_bar.setValue(round(total_attribute_bar / 2))
        pw_text.setText(f"""You got {total_attribute - CONST_TOTAL_ATTRIBUTE} {attribute.upper()} points from your {add_progress_bar} {attribute.upper()} progress \nNo need to add them, they already there ;)""")

    except ValueError:
        QMessageBox.warning(None, "NoNoNo!", "Please, insert an integer positive value!")


def attribute_progress():
    button_select = pw.sender()
    name = mw_name.text()[6:].lower()
    id = CharactersTable().select_id(name)

    attributes = AttributesTable().select_all(id)[0]
    attributes_progress = AttributesProgressBarTable().select_all(id)[0]


    if button_select.text() == "ADD STR":
        progress_bar_handling("str", "str_bar", pw_add_str, attributes_progress.str_bar,
                              attributes.str, id, mw_str, mw_str_progress)
    elif button_select.text() == "ADD WIS":
        progress_bar_handling("wis", "wis_bar", pw_add_wis, attributes_progress.wis_bar,
                              attributes.wis, id, mw_wis, mw_wis_progress)
    elif button_select.text() == "ADD DEX":
        progress_bar_handling("dex", "dex_bar", pw_add_dex, attributes_progress.dex_bar,
                              attributes.dex, id, mw_dex, mw_dex_progress)
    elif button_select.text() == "ADD INT":
        progress_bar_handling("int", "int_bar", pw_add_int, attributes_progress.int_bar,
                              attributes.int, id, mw_int, mw_int_progress)
    elif button_select.text() == "ADD CONS":
        progress_bar_handling("cons", "cons_bar", pw_add_cons, attributes_progress.cons_bar,
                              attributes.cons, id, mw_cons, mw_cons_progress)
    elif button_select.text() == "ADD CHAR":
        progress_bar_handling("char", "char_bar", pw_add_char, attributes_progress.char_bar,
                              attributes.char, id, mw_char, mw_char_progress)


def confirmation_box(attribute_progress_bar):
    confirmation_box = QMessageBox()
    confirmation_box.setWindowTitle("Confirmation")
    confirmation_box.setText(
        f"Are you sure you want to perform this action?\nThis will clear all your current {attribute_progress_bar} "
        "progress!")
    confirmation_box.setIcon(QMessageBox.Icon.Question)

    confirmation_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    confirmation_box.setDefaultButton(QMessageBox.StandardButton.No)

    response = confirmation_box.exec()

    return response == QMessageBox.StandardButton.Yes


def update_stats():
    button_select = update.sender()
    name = mw_name.text()[6:].lower()
    id = CharactersTable().select_id(name)
    attributes_progress = AttributesProgressBarTable().select_all(id)[0]

    if button_select.text() == "Rename Character":
        new_name = update_name.text().lower()
        if not new_name.strip():
            QMessageBox.warning(None, "Invalid Name", "Name cannot be empty or just spaces.")
        elif len(new_name) < 2 or len(new_name) > 30:
            QMessageBox.warning(None, "Invalid Name", "Name must be between 2 and 50 characters long.")
        elif len(CharactersTable().select_name(new_name)) != 0:
            QMessageBox.warning(None, "Invalid Name", "This name is already taken. Try another one.")
        else:
            CharactersTable().update_name(id, new_name)
            mw_name.setText(f"NAME: {new_name.upper()}")
            update_text.setText("Character Successfully Renamed!")

    elif button_select.text() == "Update Total XP":
        try:
            new_xp = int(update_total_xp.text())
            if new_xp < 0:
                raise ValueError

            CharactersTable().update_xp(id, new_xp)

            mw_totalxp_level.setText(f"TOTAL XP: {new_xp}")

            new_level = calculate_level(new_xp)[0]
            mw_level.setText(f"LEVEL: {new_level}")

            new_xp_next_level = calculate_level(new_xp)[1]
            mw_xpnxt_level.setText(f"XP NEXT LEVEL: {new_xp_next_level}")

            update_text.setText("Total XP Successfully Updated!")
        except ValueError:
            QMessageBox.warning(None, "Invalid XP Value", "Please, insert an integer positive value!")

    elif button_select.text() == "Update HP":
        try:
            new_hp = int(update_hp.text())
            if new_hp < 0:
                raise ValueError

            BaseStatsTable().update_stats(id, "hp", new_hp)
            mw_hp.setText(f"HP: {new_hp}")
            update_text.setText("HP Successfully Updated!")

        except ValueError:
            QMessageBox.warning(None, "Invalid HP Value", "Please, insert an integer positive value!")

    elif button_select.text() == "Update Stamina":
        try:
            new_stamina = int(update_stamina.text())
            if new_stamina < 0:
                raise ValueError

            BaseStatsTable().update_stats(id, "stamina", new_stamina)
            mw_stamina.setText(f"STAMINA: {new_stamina}")
            update_text.setText("Stamina Successfully Updated!")

        except ValueError:
            QMessageBox.warning(None, "Invalid Stamina Value", "Please, insert an integer positive value!")

    elif button_select.text() == "Update AC":
        try:
            new_ac = int(update_ac.text())
            if new_ac < 0:
                raise ValueError

            BaseStatsTable().update_stats(id, "ac", new_ac)
            mw_ac.setText(f"AC: {new_ac}")
            update_text.setText("AC Successfully Updated!")

        except ValueError:
            QMessageBox.warning(None, "Invalid AC Value", "Please, insert an integer positive value!")

    elif button_select.text() == "Update Armor":
        try:
            new_armor = int(update_armor.text())
            if new_armor < 0:
                raise ValueError

            BaseStatsTable().update_stats(id, "armor", new_armor)
            mw_armor.setText(f"ARMOR: {new_armor}")
            update_text.setText("Armor Successfully Updated!")

        except ValueError:
            QMessageBox.warning(None, "Invalid Armor Value", "Please, insert an integer positive value!")

    elif button_select.text() == "Update STR":
        try:
            new_str = int(update_str.text())
            if new_str < 0:
                raise ValueError

            AttributesTable().update("str", new_str, id)
            mw_str.setText(f"STR: {new_str}")
            if new_str <= 20:
                mw_str_progress.setValue(attributes_progress.str_bar)
            else:
                mw_str_progress.setValue(round(attributes_progress.str_bar/2))
            update_text.setText("STR Successfully Updated!")

        except ValueError:
            QMessageBox.warning(None, "Invalid STR Value", "Please, insert an integer positive value!")

    elif button_select.text() == "Update WIS":
        try:
            new_wis = int(update_wis.text())
            if new_wis < 0:
                raise ValueError

            AttributesTable().update("wis", new_wis, id)
            mw_wis.setText(f"WIS: {new_wis}")
            if new_wis <= 20:
                mw_wis_progress.setValue(attributes_progress.wis_bar)
            else:
                mw_wis_progress.setValue(round(attributes_progress.wis_bar/2))
            update_text.setText("WIS Successfully Updated!")

        except ValueError:
            QMessageBox.warning(None, "Invalid WIS Value", "Please, insert an integer positive value!")

    elif button_select.text() == "Update DEX":
        try:
            new_dex = int(update_dex.text())
            if new_dex < 0:
                raise ValueError

            AttributesTable().update("dex", new_dex, id)
            mw_dex.setText(f"DEX: {new_dex}")
            if new_dex <= 20:
                mw_dex_progress.setValue(attributes_progress.dex_bar)
            else:
                mw_dex_progress.setValue(round(attributes_progress.dex_bar/2))
            update_text.setText("DEX Successfully Updated!")

        except ValueError:
            QMessageBox.warning(None, "Invalid DEX Value", "Please, insert an integer positive value!")

    elif button_select.text() == "Update INT":
        try:
            new_int = int(update_int.text())
            if new_int < 0:
                raise ValueError

            AttributesTable().update("int", new_int, id)
            mw_int.setText(f"INT: {new_int}")
            if new_int <= 20:
                mw_int_progress.setValue(attributes_progress.int_bar)
            else:
                mw_int_progress.setValue(round(attributes_progress.int_bar/2))
            update_text.setText("INT Successfully Updated!")

        except ValueError:
            QMessageBox.warning(None, "Invalid INT Value", "Please, insert an integer positive value!")

    elif button_select.text() == "Update CONS":
        try:
            new_cons = int(update_cons.text())
            if new_cons < 0:
                raise ValueError

            AttributesTable().update("cons", new_cons, id)
            mw_cons.setText(f"CONS: {new_cons}")
            if new_cons <= 20:
                mw_cons_progress.setValue(attributes_progress.cons_bar)
            else:
                mw_cons_progress.setValue(round(attributes_progress.cons_bar/2))
            update_text.setText("CONS Successfully Updated!")

        except ValueError:
            QMessageBox.warning(None, "Invalid CONS Value", "Please, insert an integer positive value!")

    elif button_select.text() == "Update CHAR":
        try:
            new_char = int(update_char.text())
            if new_char < 0:
                raise ValueError

            AttributesTable().update("char", new_char, id)
            mw_char.setText(f"CHAR: {new_char}")
            if new_char <= 20:
                mw_char_progress.setValue(attributes_progress.char_bar)
            else:
                mw_char_progress.setValue(round(attributes_progress.char_bar/2))
            update_text.setText("Char Successfully Updated!")

        except ValueError:
            QMessageBox.warning(None, "Invalid CHAR Value", "Please, insert an integer positive value!")

    elif button_select.text() == "Revert STR Progress to 0":
        if confirmation_box("STR"):
            AttributesProgressBarTable().update("str_bar", 0, id)
            mw_str_progress.setValue(0)
            update_text.setText("STR Progress set to 0")

    elif button_select.text() == "Revert WIS Progress to 0":
        if confirmation_box("WIS"):
            AttributesProgressBarTable().update("wis_bar", 0, id)
            mw_wis_progress.setValue(0)
            update_text.setText("WIS Progress set to 0")

    elif button_select.text() == "Revert DEX Progress to 0":
        if confirmation_box("DEX"):
            AttributesProgressBarTable().update("dex_bar", 0, id)
            mw_dex_progress.setValue(0)
            update_text.setText("DEX Progress set to 0")

    elif button_select.text() == "Revert INT Progress to 0":
        if confirmation_box("INT"):
            AttributesProgressBarTable().update("int_bar", 0, id)
            mw_int_progress.setValue(0)
            update_text.setText("INT Progress set to 0")

    elif button_select.text() == "Revert CONS Progress to 0":
        if confirmation_box("CONS"):
            AttributesProgressBarTable().update("cons_bar", 0, id)
            mw_cons_progress.setValue(0)
            update_text.setText("CONS Progress set to 0")

    elif button_select.text() == "Revert CHAR Progress to 0":
        if confirmation_box("CHAR"):
            AttributesProgressBarTable().update("char_bar", 0, id)
            mw_char_progress.setValue(0)
            update_text.setText("CHAR Progress set to 0")



app = QApplication(sys.argv) #Creates the application
# In case of needing to revert, here is where I enforce the border for the QLineEdits. Just delete border,
# border-radius and padding.
app.setStyleSheet("""
    QWidget {
    background-color: #1e1e1e;
    color: white
    }
    QLineEdit, QComboBox {
    background-color: #2d2c2c;
    border: 1px solid #1e1e1e;
    border-radius: 5px;
    padding: 0px 3px;
    color: white
    }
    QPushButton {
    background-color: #3d3c3d;
    color: white
    }
""")


#Creates the initial window
iw = QWidget()
iw.resize(400, 300)
iw.setWindowTitle("RPG Calculator 2.0")

iw_title = QLabel("Character Selection")
iw_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
iw_title.setStyleSheet("font-size: 20px; font-weight: bold")

iw_dropdown = QComboBox()
iw_dropdown.setMinimumHeight(40)
iw_dropdown.setStyleSheet("text-align: center")
iw_dropdown.setPlaceholderText("Select Character")
iw_dropdown.addItems(dropdown_list())

iw_new_btn = QPushButton("Submit")
iw_new_btn.setMinimumHeight(40)
iw_new_btn.clicked.connect(lambda: to_mw(iw, iw_dropdown.currentText()))

iw_new_character = QLabel("Don't have a character? <a href ='#'> Create one <a>")
iw_new_character.setAlignment(Qt.AlignmentFlag.AlignCenter)
iw_new_character.linkActivated.connect(iw_to_new_character)

iw_VLayout = QVBoxLayout()
iw_VLayout.addWidget(iw_title)
iw_VLayout.addWidget(iw_dropdown)
iw_VLayout.addWidget(iw_new_btn)
iw_VLayout.addWidget(iw_new_character)

iw.setLayout(iw_VLayout)


#Creates the new character window
new_char_window = QWidget()
new_char_window.resize(500, 800)
new_char_window.setWindowTitle("RPG Calculator 2.0")

new_char_back = QLabel("<a href ='#'> Back to Selection Menu<a>")
new_char_back.setAlignment(Qt.AlignmentFlag.AlignBottom)
new_char_back.linkActivated.connect(new_character_to_iw)

new_char_title = QLabel("New Character Creation")
new_char_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
new_char_title.setStyleSheet("font-size: 30px; font-weight: bold")

new_char_box1 = QLineEdit()
new_char_box1.setPlaceholderText("Name")
new_char_box1.setAlignment(Qt.AlignmentFlag.AlignCenter)
new_char_box1.setMinimumHeight(40)
new_char_box1.setStyleSheet("font-size: 15px")

new_char_box2 = QLineEdit()
new_char_box2.setPlaceholderText("Total XP")
new_char_box2.setAlignment(Qt.AlignmentFlag.AlignCenter)
new_char_box2.setMinimumHeight(40)
new_char_box2.setStyleSheet("font-size: 15px")
new_char_box2.setToolTip("Please, insert only integer values in the numeric fields.")

new_char_box3 = QPushButton("Image")
new_char_box3.setMinimumHeight(40)
new_char_box3.clicked.connect(select_image)
new_char_box3.setStyleSheet("font-size: 15px")
new_char_box3.setToolTip("Only JPG and PNG are supported.")

new_char_box4 = QLineEdit()
new_char_box4.setPlaceholderText("HP")
new_char_box4.setAlignment(Qt.AlignmentFlag.AlignCenter)
new_char_box4.setMinimumHeight(40)
new_char_box4.setStyleSheet("font-size: 15px")

new_char_box5 = QLineEdit()
new_char_box5.setPlaceholderText("Stamina")
new_char_box5.setAlignment(Qt.AlignmentFlag.AlignCenter)
new_char_box5.setMinimumHeight(40)
new_char_box5.setStyleSheet("font-size: 15px")

new_char_box6 = QLineEdit()
new_char_box6.setPlaceholderText("AC")
new_char_box6.setAlignment(Qt.AlignmentFlag.AlignCenter)
new_char_box6.setMinimumHeight(40)
new_char_box6.setStyleSheet("font-size: 15px")

new_char_box7 = QLineEdit()
new_char_box7.setPlaceholderText("Armor")
new_char_box7.setAlignment(Qt.AlignmentFlag.AlignCenter)
new_char_box7.setMinimumHeight(40)
new_char_box7.setStyleSheet("font-size: 15px")

#BOXES FOR STATS
new_char_box8 = QLineEdit()
new_char_box8.setPlaceholderText("STR")
new_char_box8.setAlignment(Qt.AlignmentFlag.AlignCenter)
new_char_box8.setMinimumHeight(40)
new_char_box8.setStyleSheet("color: #FF6961; font-size: 15px")

new_char_box9 = QLineEdit()
new_char_box9.setPlaceholderText("WIS")
new_char_box9.setAlignment(Qt.AlignmentFlag.AlignCenter)
new_char_box9.setMinimumHeight(40)
new_char_box9.setStyleSheet("color: #FDFD96; font-size: 15px")

new_char_box10 = QLineEdit()
new_char_box10.setPlaceholderText("DEX")
new_char_box10.setAlignment(Qt.AlignmentFlag.AlignCenter)
new_char_box10.setMinimumHeight(40)
new_char_box10.setStyleSheet("color: #77DD77; font-size: 15px")

new_char_box11 = QLineEdit()
new_char_box11.setPlaceholderText("INT")
new_char_box11.setAlignment(Qt.AlignmentFlag.AlignCenter)
new_char_box11.setMinimumHeight(40)
new_char_box11.setStyleSheet("color: #AEC6CF; font-size: 15px")

new_char_box12 = QLineEdit()
new_char_box12.setPlaceholderText("CONS")
new_char_box12.setAlignment(Qt.AlignmentFlag.AlignCenter)
new_char_box12.setMinimumHeight(40)
new_char_box12.setStyleSheet("color: #FAC898; font-size: 15px")

new_char_box13 = QLineEdit()
new_char_box13.setPlaceholderText("CHAR")
new_char_box13.setAlignment(Qt.AlignmentFlag.AlignCenter)
new_char_box13.setMinimumHeight(40)
new_char_box13.setStyleSheet("color: #C3B1E1; font-size: 15px")

#BOXES FOR TS PROGRESS BAR
new_char_box14 = QLineEdit()
new_char_box14.setPlaceholderText("Progress for STR point")
new_char_box14.setAlignment(Qt.AlignmentFlag.AlignCenter)
new_char_box14.setMinimumHeight(40)
new_char_box14.setStyleSheet("font-size: 15px")

new_char_box15 = QLineEdit()
new_char_box15.setPlaceholderText("Progress for WIS point")
new_char_box15.setAlignment(Qt.AlignmentFlag.AlignCenter)
new_char_box15.setMinimumHeight(40)
new_char_box15.setStyleSheet("font-size: 15px")

new_char_box16 = QLineEdit()
new_char_box16.setPlaceholderText("Progress for DEX point")
new_char_box16.setAlignment(Qt.AlignmentFlag.AlignCenter)
new_char_box16.setMinimumHeight(40)
new_char_box16.setStyleSheet("font-size: 15px")

new_char_box17 = QLineEdit()
new_char_box17.setPlaceholderText("Progress for INT point")
new_char_box17.setAlignment(Qt.AlignmentFlag.AlignCenter)
new_char_box17.setMinimumHeight(40)
new_char_box17.setStyleSheet("font-size: 15px")

new_char_box18 = QLineEdit()
new_char_box18.setPlaceholderText("Progress for CONS point")
new_char_box18.setAlignment(Qt.AlignmentFlag.AlignCenter)
new_char_box18.setMinimumHeight(40)
new_char_box18.setStyleSheet("font-size: 15px")

new_char_box19 = QLineEdit()
new_char_box19.setPlaceholderText("Progress for CHAR point")
new_char_box19.setAlignment(Qt.AlignmentFlag.AlignCenter)
new_char_box19.setMinimumHeight(40)
new_char_box19.setStyleSheet("font-size: 15px")

#ADD the stat and progress boxes to the grid layout
stats_layout = QGridLayout()
stats_layout.addWidget(new_char_box8, 0, 0)
stats_layout.addWidget(new_char_box9, 0, 1)
stats_layout.addWidget(new_char_box10, 1, 0)
stats_layout.addWidget(new_char_box11, 1, 1)
stats_layout.addWidget(new_char_box12, 2, 0)
stats_layout.addWidget(new_char_box13, 2, 1)
stats_layout.addWidget(new_char_box14, 3, 0)
stats_layout.addWidget(new_char_box15, 3, 1)
stats_layout.addWidget(new_char_box16, 4, 0)
stats_layout.addWidget(new_char_box17, 4, 1)
stats_layout.addWidget(new_char_box18, 5, 0)
stats_layout.addWidget(new_char_box19, 5, 1)


#Creates the insertion button
new_char_button = QPushButton("Create")
new_char_button.setMinimumHeight(40)
new_char_button.setMaximumSize(100, 40)
new_char_button.clicked.connect(create_character)

#THIS PART WILL TAKE CARE OF ALIGNING EVERYTHING

#First, center the new_char_button
button_layout = QHBoxLayout()
button_layout.addWidget(new_char_button)

#Then, we'll align horizontally all the boxes
new_char_VLayout = QVBoxLayout()
new_char_VLayout.setContentsMargins(30, 10, 20, 20)
new_char_VLayout.addWidget(new_char_title)
new_char_VLayout.addSpacing(30)
new_char_VLayout.addWidget(new_char_box1)
new_char_VLayout.addWidget(new_char_box2)
new_char_VLayout.addWidget(new_char_box3)
new_char_VLayout.addWidget(new_char_box4)
new_char_VLayout.addWidget(new_char_box5)
new_char_VLayout.addWidget(new_char_box6)
new_char_VLayout.addWidget(new_char_box7)
new_char_VLayout.addLayout(stats_layout)
new_char_VLayout.addSpacing(30)
new_char_VLayout.addLayout(button_layout)
new_char_VLayout.addWidget(new_char_back)

#Then, we'll actually set the layout for the new_char_window
new_char_window.setLayout(new_char_VLayout)

#Create the Main Window, to show character stats
mw = QWidget()
mw.resize(1030, 600)
mw.setWindowTitle("RPG Calculator 2.0")

mw_image = QLabel(mw)
mw_image.setGeometry(50, 40, 250, 250)

mw_edit = QPushButton("UPDATE STATS", mw)
mw_edit.setGeometry(780, 40, 200, 40)
mw_edit.clicked.connect(mw_to_update)

mw_lvl_clear = QPushButton("DIED? CLEAR LVL XP", mw)
mw_lvl_clear.setGeometry(780, 90, 200, 40)
mw_lvl_clear.clicked.connect(confirmation)

mw_insert_att = QPushButton("INSERT ATTRIBUTE PROGRESS", mw)
mw_insert_att.setGeometry(780, 140, 200, 40)
mw_insert_att.clicked.connect(mw_to_pw)

mw_d10 = QPushButton("D10", mw)
mw_d10.setGeometry(780, 190, 60, 40)
mw_d10.setStyleSheet("background-color: #002966")
mw_d10.clicked.connect(dice_roll)

mw_d12 = QPushButton("D12", mw)
mw_d12.setGeometry(850, 190, 60, 40)
mw_d12.setStyleSheet("background-color: #663d00")
mw_d12.clicked.connect(dice_roll)

mw_d20 = QPushButton("D20", mw)
mw_d20.setGeometry(920, 190, 60, 40)
mw_d20.setStyleSheet("background-color: #660000")
mw_d20.clicked.connect(dice_roll)

#This only shows if you click the D10, D12 or D20 buttons. This is connected to the dice_roll() function
mw_dice_result = QLabel(mw)
mw_dice_result.move(820, 240)

mw_name = QLineEdit("Name", mw)
mw_name.setGeometry(330, 40, 400, 40)
mw_name.setReadOnly(True)
mw_name.setStyleSheet("background-color: #333333; font-weight: bold; font-size: 18px")

mw_level = QLineEdit("Level", mw)
mw_level.setGeometry(330, 90, 195, 40)
mw_level.setReadOnly(True)
mw_level.setStyleSheet("background-color: #333333; font-weight: bold; font-size: 18px")

mw_xpnxt_level = QLineEdit("XP nxt level", mw)
mw_xpnxt_level.setGeometry(535, 90, 195, 40)
mw_xpnxt_level.setReadOnly(True)
mw_xpnxt_level.setStyleSheet("background-color: #333333; font-weight: bold; font-size: 14px")

mw_totalxp_level = QLineEdit("Total XP", mw)
mw_totalxp_level.setGeometry(330, 140, 400, 40)
mw_totalxp_level.setReadOnly(True)
mw_totalxp_level.setStyleSheet("background-color: #333333; font-weight: bold; font-size: 18px")

mw_ep_xp = QLineEdit(mw)
mw_ep_xp.setPlaceholderText("INSERT EPISODE XP")
mw_ep_xp.setGeometry(330, 190, 270, 40)
mw_ep_xp.setStyleSheet("background-color: #333333; font-weight: bold; font-size: 18px")
mw_ep_xp.setToolTip("Only integer values")

mw_xp_button = QPushButton("Add XP", mw)
mw_xp_button.setGeometry(610, 190, 120, 40)
mw_xp_button.clicked.connect(add_xp)

#This is to show the lvl_up after the XP is inserted. It uses the add_xp function.
mw_lvl_info = QLabel(mw)
mw_lvl_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
mw_lvl_info.setStyleSheet("font-weight: bold; font-size: 15px")

mw_stats_label = QLabel("STATS", mw)
mw_stats_label.move(227, 300)
mw_stats_label.setStyleSheet("font-size: 25px; font-weight: bold")

mw_hp = QLineEdit("HP", mw)
mw_hp.setGeometry(49, 340, 100, 50)
mw_hp.setAlignment(Qt.AlignmentFlag.AlignCenter)
mw_hp.setReadOnly(True)
mw_hp.setStyleSheet("background-color: #990800; font-weight: bold")

mw_stamina = QLineEdit("Stamina", mw)
mw_stamina.setGeometry(159, 340, 100, 50)
mw_stamina.setAlignment(Qt.AlignmentFlag.AlignCenter)
mw_stamina.setReadOnly(True)
mw_stamina.setStyleSheet("background-color: #937706; font-weight: bold")

mw_ac = QLineEdit("AC", mw)
mw_ac.setGeometry(269, 340, 100, 50)
mw_ac.setAlignment(Qt.AlignmentFlag.AlignCenter)
mw_ac.setReadOnly(True)
mw_ac.setStyleSheet("background-color: #395660; font-weight: bold")

mw_armor = QLineEdit("Armor", mw)
mw_armor.setGeometry(379, 340, 100, 50)
mw_armor.setAlignment(Qt.AlignmentFlag.AlignCenter)
mw_armor.setReadOnly(True)
mw_armor.setStyleSheet("background-color: #395660; font-weight: bold")

mw_str = QLineEdit("STR: ", mw)
mw_str.setGeometry(49, 400, 210, 50)
mw_str.setAlignment(Qt.AlignmentFlag.AlignCenter)
mw_str.setReadOnly(True)
mw_str.setStyleSheet("background-color: #4d0400; font-weight: bold")

mw_wis = QLineEdit("WIS: ", mw)
mw_wis.setGeometry(269, 400, 210, 50)
mw_wis.setAlignment(Qt.AlignmentFlag.AlignCenter)
mw_wis.setReadOnly(True)
mw_wis.setStyleSheet("background-color: #4d004d; font-weight: bold")

mw_dex = QLineEdit("DEX: ", mw)
mw_dex.setGeometry(49, 460, 210, 50)
mw_dex.setAlignment(Qt.AlignmentFlag.AlignCenter)
mw_dex.setReadOnly(True)
mw_dex.setStyleSheet("background-color: #103d10; font-weight: bold")

mw_int = QLineEdit("INT: ", mw)
mw_int.setGeometry(269, 460, 210, 50)
mw_int.setAlignment(Qt.AlignmentFlag.AlignCenter)
mw_int.setReadOnly(True)
mw_int.setStyleSheet("background-color: #00134d; font-weight: bold")

mw_cons = QLineEdit("CONS: ", mw)
mw_cons.setGeometry(49, 520, 210, 50)
mw_cons.setAlignment(Qt.AlignmentFlag.AlignCenter)
mw_cons.setReadOnly(True)
mw_cons.setStyleSheet("background-color: #492503; font-weight: bold")

mw_char = QLineEdit("CHAR: ", mw)
mw_char.setGeometry(269, 520, 210, 50)
mw_char.setAlignment(Qt.AlignmentFlag.AlignCenter)
mw_char.setReadOnly(True)
mw_char.setStyleSheet("background-color: #660011; font-weight: bold")

mw_back_iw = QLabel("<a href ='#'> Back to Selection Menu<a>", mw)
mw_back_iw.move(15, 580)
mw_back_iw.linkActivated.connect(mw_to_iw)

mw_progress_label = QLabel("Progress Towards Attribute", mw)
mw_progress_label.move(610, 300)
mw_progress_label.setStyleSheet("font-size: 25px; font-weight: bold")

mw_str_progress = QProgressBar(mw)
mw_str_progress.setGeometry(550, 374, 210, 50)
mw_str_progress.setTextVisible(True)
mw_str_progress.setStyleSheet("""
QProgressBar::chunk {background-color: #4d0400};
text-align: center;
border: 4px solid black;
border-radius: 5px;
font-weight: bold;
font-size: 13px;
background-color: gray;""")
mw_str_progress_label = QLabel("STR", mw)
mw_str_progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
mw_str_progress_label.setStyleSheet("""
background-color: black;
color: white; 
font-weight: bold; 
border: 4px solid black; 
border-radius: 7px""")
mw_str_progress_label.setGeometry(558, 361, 45, 25)

mw_wis_progress = QProgressBar(mw)
mw_wis_progress.setGeometry(770, 374, 210, 50)
mw_wis_progress.setTextVisible(True)
mw_wis_progress.setStyleSheet("""
QProgressBar::chunk {background-color: #4d004d};
text-align: center;
border: 4px solid black;
border-radius: 5px;
font-weight: bold;
font-size: 13px;
background-color: gray;""")
mw_wis_progress_label = QLabel("WIS", mw)
mw_wis_progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
mw_wis_progress_label.setStyleSheet("""
background-color: black;
color: white; 
font-weight: bold; 
border: 4px solid black; 
border-radius: 7px""")
mw_wis_progress_label.setGeometry(778, 361, 45, 25)

mw_dex_progress = QProgressBar(mw)
mw_dex_progress.setGeometry(550, 447, 210, 50)
mw_dex_progress.setTextVisible(True)
mw_dex_progress.setStyleSheet("""
QProgressBar::chunk {background-color: #103d10};
text-align: center;
border: 4px solid black;
border-radius: 5px;
font-weight: bold;
font-size: 13px;
background-color: gray;""")
mw_dex_progress_label = QLabel("DEX", mw)
mw_dex_progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
mw_dex_progress_label.setStyleSheet("""
background-color: black;
color: white; 
font-weight: bold; 
border: 4px solid black; 
border-radius: 7px""")
mw_dex_progress_label.setGeometry(558, 434, 45, 25)

mw_int_progress = QProgressBar(mw)
mw_int_progress.setGeometry(770, 447, 210, 50)
mw_int_progress.setTextVisible(True)
mw_int_progress.setStyleSheet("""
QProgressBar::chunk {background-color: #00134d};
text-align: center;
border: 4px solid black;
border-radius: 5px;
font-weight: bold;
font-size: 13px;
background-color: gray;""")
mw_int_progress_label = QLabel("INT", mw)
mw_int_progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
mw_int_progress_label.setStyleSheet("""
background-color: black;
color: white; 
font-weight: bold; 
border: 4px solid black; 
border-radius: 7px""")
mw_int_progress_label.setGeometry(778, 434, 45, 25)

mw_cons_progress = QProgressBar(mw)
mw_cons_progress.setGeometry(550, 520, 210, 50)
mw_cons_progress.setTextVisible(True)
mw_cons_progress.setStyleSheet("""
QProgressBar::chunk {background-color: #492503};
text-align: center;
border: 4px solid black;
border-radius: 5px;
font-weight: bold;
font-size: 13px;
background-color: gray;""")
mw_cons_progress_label = QLabel("CONS", mw)
mw_cons_progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
mw_cons_progress_label.setStyleSheet("""
background-color: black;
color: white; 
font-weight: bold; 
border: 4px solid black; 
border-radius: 7px""")
mw_cons_progress_label.setGeometry(558, 507, 45, 25)

mw_char_progress = QProgressBar(mw)
mw_char_progress.setGeometry(770, 520, 210, 50)
mw_char_progress.setTextVisible(True)
mw_char_progress.setStyleSheet("""
QProgressBar::chunk {background-color: #660011};
text-align: center;
border: 4px solid black;
border-radius: 5px;
font-weight: bold;
font-size: 13px;
background-color: gray;""")
mw_char_progress_label = QLabel("CHAR", mw)
mw_char_progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
mw_char_progress_label.setStyleSheet("""
background-color: black;
color: white; 
font-weight: bold; 
border: 4px solid black; 
border-radius: 7px""")
mw_char_progress_label.setGeometry(778, 507, 45, 25)

pw = QWidget()
pw.resize(320, 360)
pw.setWindowTitle("RPG Calculator 2.0")

pw_add_str = QLineEdit()
pw_add_str.setPlaceholderText("Enter STR Progress")
pw_add_str.setAlignment(Qt.AlignmentFlag.AlignCenter)
pw_add_str.setMinimumHeight(35)
pw_button_str = QPushButton("ADD STR")
pw_button_str.setMinimumHeight(35)
pw_button_str.clicked.connect(attribute_progress)

pw_add_wis = QLineEdit()
pw_add_wis.setPlaceholderText("Enter WIS Progress")
pw_add_wis.setMinimumHeight(35)
pw_add_wis.setAlignment(Qt.AlignmentFlag.AlignCenter)
pw_button_wis = QPushButton("ADD WIS")
pw_button_wis.setMinimumHeight(35)
pw_button_wis.clicked.connect(attribute_progress)

pw_add_dex = QLineEdit()
pw_add_dex.setPlaceholderText("Enter DEX Progress")
pw_add_dex.setMinimumHeight(35)
pw_add_dex.setAlignment(Qt.AlignmentFlag.AlignCenter)
pw_button_dex = QPushButton("ADD DEX")
pw_button_dex.setMinimumHeight(35)
pw_button_dex.clicked.connect(attribute_progress)

pw_add_int = QLineEdit()
pw_add_int.setPlaceholderText("Enter INT Progress")
pw_add_int.setMinimumHeight(35)
pw_add_int.setAlignment(Qt.AlignmentFlag.AlignCenter)
pw_button_int = QPushButton("ADD INT")
pw_button_int.setMinimumHeight(35)
pw_button_int.clicked.connect(attribute_progress)

pw_add_cons = QLineEdit()
pw_add_cons.setPlaceholderText("Enter CONS Progress")
pw_add_cons.setMinimumHeight(35)
pw_add_cons.setAlignment(Qt.AlignmentFlag.AlignCenter)
pw_button_cons = QPushButton("ADD CONS")
pw_button_cons.setMinimumHeight(35)
pw_button_cons.clicked.connect(attribute_progress)

pw_add_char = QLineEdit()
pw_add_char.setPlaceholderText("Enter CHAR Progress")
pw_add_char.setMinimumHeight(35)
pw_add_char.setAlignment(Qt.AlignmentFlag.AlignCenter)
pw_button_char = QPushButton("ADD CHAR")
pw_button_char.setMinimumHeight(35)
pw_button_char.clicked.connect(attribute_progress)

pw_text = QLabel()
pw_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
pw_text.setStyleSheet("font-weight: bold")

pw_layout = QGridLayout()
pw_layout.addWidget(pw_add_str, 0, 0)
pw_layout.addWidget(pw_button_str, 0, 1)
pw_layout.addWidget(pw_add_wis, 1, 0)
pw_layout.addWidget(pw_button_wis, 1, 1)
pw_layout.addWidget(pw_add_dex, 2, 0)
pw_layout.addWidget(pw_button_dex, 2, 1)
pw_layout.addWidget(pw_add_int, 3, 0)
pw_layout.addWidget(pw_button_int, 3, 1)
pw_layout.addWidget(pw_add_cons, 4, 0)
pw_layout.addWidget(pw_button_cons, 4, 1)
pw_layout.addWidget(pw_add_char, 5, 0)
pw_layout.addWidget(pw_button_char, 5, 1)
pw_layout.addWidget(pw_text, 6, 0, 1, 2)

pw.setLayout(pw_layout)

# Sets the update page
update = QWidget()
update.resize(420, 820)
update.setWindowTitle("RPG Calculator 2.0")

update_name = QLineEdit()
update_name.setPlaceholderText("New Name")
update_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
update_name.setMinimumHeight(35)
update_name_button = QPushButton("Rename Character")
update_name_button.setMinimumHeight(35)
update_name_button.clicked.connect(update_stats)

update_total_xp = QLineEdit()
update_total_xp.setPlaceholderText("New Total XP")
update_total_xp.setAlignment(Qt.AlignmentFlag.AlignCenter)
update_total_xp.setMinimumHeight(35)
update_total_xp_button = QPushButton("Update Total XP")
update_total_xp_button.setMinimumHeight(35)
update_total_xp_button.clicked.connect(update_stats)

update_hp = QLineEdit()
update_hp.setPlaceholderText("New HP Value")
update_hp.setAlignment(Qt.AlignmentFlag.AlignCenter)
update_hp.setMinimumHeight(35)
update_hp_button = QPushButton("Update HP")
update_hp_button.setMinimumHeight(35)
update_hp_button.clicked.connect(update_stats)

update_stamina = QLineEdit()
update_stamina.setPlaceholderText("New Stamina Value")
update_stamina.setAlignment(Qt.AlignmentFlag.AlignCenter)
update_stamina.setMinimumHeight(35)
update_stamina_button = QPushButton("Update Stamina")
update_stamina_button.setMinimumHeight(35)
update_stamina_button.clicked.connect(update_stats)

update_ac = QLineEdit()
update_ac.setPlaceholderText("New AC Value")
update_ac.setAlignment(Qt.AlignmentFlag.AlignCenter)
update_ac.setMinimumHeight(35)
update_ac_button = QPushButton("Update AC")
update_ac_button.setMinimumHeight(35)
update_ac_button.clicked.connect(update_stats)

update_armor = QLineEdit()
update_armor.setPlaceholderText("New Armor Value")
update_armor.setAlignment(Qt.AlignmentFlag.AlignCenter)
update_armor.setMinimumHeight(35)
update_armor_button = QPushButton("Update Armor")
update_armor_button.setMinimumHeight(35)
update_armor_button.clicked.connect(update_stats)

update_str = QLineEdit()
update_str.setPlaceholderText("New STR Value")
update_str.setAlignment(Qt.AlignmentFlag.AlignCenter)
update_str.setMinimumHeight(35)
update_str_button = QPushButton("Update STR")
update_str_button.setMinimumHeight(35)
update_str_button.clicked.connect(update_stats)

update_wis = QLineEdit()
update_wis.setPlaceholderText("New WIS Value")
update_wis.setAlignment(Qt.AlignmentFlag.AlignCenter)
update_wis.setMinimumHeight(35)
update_wis_button = QPushButton("Update WIS")
update_wis_button.setMinimumHeight(35)
update_wis_button.clicked.connect(update_stats)

update_dex = QLineEdit()
update_dex.setPlaceholderText("New DEX Value")
update_dex.setAlignment(Qt.AlignmentFlag.AlignCenter)
update_dex.setMinimumHeight(35)
update_dex_button = QPushButton("Update DEX")
update_dex_button.setMinimumHeight(35)
update_dex_button.clicked.connect(update_stats)

update_int = QLineEdit()
update_int.setPlaceholderText("New INT Value")
update_int.setAlignment(Qt.AlignmentFlag.AlignCenter)
update_int.setMinimumHeight(35)
update_int_button = QPushButton("Update INT")
update_int_button.setMinimumHeight(35)
update_int_button.clicked.connect(update_stats)

update_cons = QLineEdit()
update_cons.setPlaceholderText("New CONS Value")
update_cons.setAlignment(Qt.AlignmentFlag.AlignCenter)
update_cons.setMinimumHeight(35)
update_cons_button = QPushButton("Update CONS")
update_cons_button.setMinimumHeight(35)
update_cons_button.clicked.connect(update_stats)

update_char = QLineEdit()
update_char.setPlaceholderText("New CHAR Value")
update_char.setAlignment(Qt.AlignmentFlag.AlignCenter)
update_char.setMinimumHeight(35)
update_char_button = QPushButton("Update CHAR")
update_char_button.setMinimumHeight(35)
update_char_button.clicked.connect(update_stats)

update_str_progress_button = QPushButton("Revert STR Progress to 0")
update_str_progress_button.setMinimumHeight(35)
update_str_progress_button.clicked.connect(update_stats)

update_wis_progress_button = QPushButton("Revert WIS Progress to 0")
update_wis_progress_button.setMinimumHeight(35)
update_wis_progress_button.clicked.connect(update_stats)

update_dex_progress_button = QPushButton("Revert DEX Progress to 0")
update_dex_progress_button.setMinimumHeight(35)
update_dex_progress_button.clicked.connect(update_stats)

update_int_progress_button = QPushButton("Revert INT Progress to 0")
update_int_progress_button.setMinimumHeight(35)
update_int_progress_button.clicked.connect(update_stats)

update_cons_progress_button = QPushButton("Revert CONS Progress to 0")
update_cons_progress_button.setMinimumHeight(35)
update_cons_progress_button.clicked.connect(update_stats)

update_char_progress_button = QPushButton("Revert CHAR Progress to 0")
update_char_progress_button.setMinimumHeight(35)
update_char_progress_button.clicked.connect(update_stats)

update_text = QLabel()
update_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
update_text.setStyleSheet("font-weight: bold; font-size: 16px; color: yellow")


update_layout = QGridLayout()
update_layout.addWidget(update_name, 0, 0)
update_layout.addWidget(update_name_button, 0, 1)
update_layout.addWidget(update_total_xp, 1, 0)
update_layout.addWidget(update_total_xp_button, 1, 1)
update_layout.addWidget(update_hp, 2, 0)
update_layout.addWidget(update_hp_button, 2, 1)
update_layout.addWidget(update_stamina, 3, 0)
update_layout.addWidget(update_stamina_button, 3, 1)
update_layout.addWidget(update_ac, 4, 0)
update_layout.addWidget(update_ac_button, 4, 1)
update_layout.addWidget(update_armor, 5, 0)
update_layout.addWidget(update_armor_button, 5, 1)
update_layout.addWidget(update_str, 6, 0)
update_layout.addWidget(update_str_button, 6, 1)
update_layout.addWidget(update_wis, 7, 0)
update_layout.addWidget(update_wis_button, 7, 1)
update_layout.addWidget(update_dex, 8, 0)
update_layout.addWidget(update_dex_button, 8, 1)
update_layout.addWidget(update_int, 9, 0)
update_layout.addWidget(update_int_button, 9, 1)
update_layout.addWidget(update_cons, 10, 0)
update_layout.addWidget(update_cons_button, 10, 1)
update_layout.addWidget(update_char, 11, 0)
update_layout.addWidget(update_char_button, 11, 1)
update_layout.addWidget(update_str_progress_button, 12, 0, 1, 2)
update_layout.addWidget(update_wis_progress_button, 13, 0, 1, 2)
update_layout.addWidget(update_dex_progress_button, 14, 0, 1, 2)
update_layout.addWidget(update_int_progress_button, 15, 0, 1, 2)
update_layout.addWidget(update_cons_progress_button, 16, 0, 1, 2)
update_layout.addWidget(update_char_progress_button, 17, 0, 1, 2)
update_layout.addWidget(update_text, 18, 0, 1, 2)

update.setLayout(update_layout)



iw.show()
app.exec()

