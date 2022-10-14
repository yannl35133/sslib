# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'randogui.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListView,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1051, 738)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies(["Segoe UI"])
        font.setPointSize(9)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth()
        )
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.option_description = QLabel(self.centralwidget)
        self.option_description.setObjectName("option_description")
        self.option_description.setEnabled(True)
        self.option_description.setGeometry(QRect(10, 570, 931, 31))
        self.option_description.setWordWrap(True)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setGeometry(QRect(10, 10, 1031, 541))
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayoutWidget_9 = QWidget(self.tab)
        self.verticalLayoutWidget_9.setObjectName("verticalLayoutWidget_9")
        self.verticalLayoutWidget_9.setGeometry(QRect(10, 10, 1001, 115))
        self.verticalLayout_29 = QVBoxLayout(self.verticalLayoutWidget_9)
        self.verticalLayout_29.setObjectName("verticalLayout_29")
        self.verticalLayout_29.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_2 = QLabel(self.verticalLayoutWidget_9)
        self.label_2.setObjectName("label_2")
        self.label_2.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label_2)

        self.output_folder = QLineEdit(self.verticalLayoutWidget_9)
        self.output_folder.setObjectName("output_folder")

        self.horizontalLayout_7.addWidget(self.output_folder)

        self.ouput_folder_browse_button = QPushButton(self.verticalLayoutWidget_9)
        self.ouput_folder_browse_button.setObjectName("ouput_folder_browse_button")

        self.horizontalLayout_7.addWidget(self.ouput_folder_browse_button)

        self.verticalLayout_29.addLayout(self.horizontalLayout_7)

        self.verticalLayout_32 = QVBoxLayout()
        self.verticalLayout_32.setObjectName("verticalLayout_32")
        self.option_plando = QCheckBox(self.verticalLayoutWidget_9)
        self.option_plando.setObjectName("option_plando")

        self.verticalLayout_32.addWidget(self.option_plando)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.plando_file = QLineEdit(self.verticalLayoutWidget_9)
        self.plando_file.setObjectName("plando_file")

        self.horizontalLayout_19.addWidget(self.plando_file)

        self.plando_file_browse = QPushButton(self.verticalLayoutWidget_9)
        self.plando_file_browse.setObjectName("plando_file_browse")

        self.horizontalLayout_19.addWidget(self.plando_file_browse)

        self.verticalLayout_32.addLayout(self.horizontalLayout_19)

        self.verticalLayout_29.addLayout(self.verticalLayout_32)

        self.verticalSpacer_12 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_29.addItem(self.verticalSpacer_12)

        self.groupBox_12 = QGroupBox(self.tab)
        self.groupBox_12.setObjectName("groupBox_12")
        self.groupBox_12.setGeometry(QRect(10, 130, 181, 131))
        self.verticalLayoutWidget_13 = QWidget(self.groupBox_12)
        self.verticalLayoutWidget_13.setObjectName("verticalLayoutWidget_13")
        self.verticalLayoutWidget_13.setGeometry(QRect(10, 20, 169, 89))
        self.verticalLayout_33 = QVBoxLayout(self.verticalLayoutWidget_13)
        self.verticalLayout_33.setObjectName("verticalLayout_33")
        self.verticalLayout_33.setContentsMargins(0, 0, 0, 0)
        self.option_no_spoiler_log = QCheckBox(self.verticalLayoutWidget_13)
        self.option_no_spoiler_log.setObjectName("option_no_spoiler_log")

        self.verticalLayout_33.addWidget(self.option_no_spoiler_log)

        self.option_json_spoiler = QCheckBox(self.verticalLayoutWidget_13)
        self.option_json_spoiler.setObjectName("option_json_spoiler")

        self.verticalLayout_33.addWidget(self.option_json_spoiler)

        self.option_out_placement_file = QCheckBox(self.verticalLayoutWidget_13)
        self.option_out_placement_file.setObjectName("option_out_placement_file")

        self.verticalLayout_33.addWidget(self.option_out_placement_file)

        self.verticalSpacer_13 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_33.addItem(self.verticalSpacer_13)

        self.groupBox_13 = QGroupBox(self.tab)
        self.groupBox_13.setObjectName("groupBox_13")
        self.groupBox_13.setGeometry(QRect(210, 130, 131, 131))
        self.verticalLayoutWidget_14 = QWidget(self.groupBox_13)
        self.verticalLayoutWidget_14.setObjectName("verticalLayoutWidget_14")
        self.verticalLayoutWidget_14.setGeometry(QRect(10, 20, 111, 101))
        self.verticalLayout_34 = QVBoxLayout(self.verticalLayoutWidget_14)
        self.verticalLayout_34.setObjectName("verticalLayout_34")
        self.verticalLayout_34.setContentsMargins(0, 0, 0, 0)
        self.option_dry_run = QCheckBox(self.verticalLayoutWidget_14)
        self.option_dry_run.setObjectName("option_dry_run")

        self.verticalLayout_34.addWidget(self.option_dry_run)

        self.verticalSpacer_14 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_34.addItem(self.verticalSpacer_14)

        self.groupBox_14 = QGroupBox(self.tab)
        self.groupBox_14.setObjectName("groupBox_14")
        self.groupBox_14.setGeometry(QRect(360, 130, 131, 131))
        self.verticalLayoutWidget_8 = QWidget(self.groupBox_14)
        self.verticalLayoutWidget_8.setObjectName("verticalLayoutWidget_8")
        self.verticalLayoutWidget_8.setGeometry(QRect(10, 20, 111, 80))
        self.verticalLayout_17 = QVBoxLayout(self.verticalLayoutWidget_8)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.option_tunic_swap = QCheckBox(self.verticalLayoutWidget_8)
        self.option_tunic_swap.setObjectName("option_tunic_swap")

        self.verticalLayout_17.addWidget(self.option_tunic_swap)

        self.verticalSpacer_15 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_17.addItem(self.verticalSpacer_15)

        self.groupBox_15 = QGroupBox(self.tab)
        self.groupBox_15.setObjectName("groupBox_15")
        self.groupBox_15.setGeometry(QRect(510, 130, 181, 131))
        self.verticalLayoutWidget_11 = QWidget(self.groupBox_15)
        self.verticalLayoutWidget_11.setObjectName("verticalLayoutWidget_11")
        self.verticalLayoutWidget_11.setGeometry(QRect(10, 20, 161, 106))
        self.verticalLayout_35 = QVBoxLayout(self.verticalLayoutWidget_11)
        self.verticalLayout_35.setObjectName("verticalLayout_35")
        self.verticalLayout_35.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_36 = QVBoxLayout()
        self.verticalLayout_36.setObjectName("verticalLayout_36")
        self.label_for_option_music_rando = QLabel(self.verticalLayoutWidget_11)
        self.label_for_option_music_rando.setObjectName("label_for_option_music_rando")

        self.verticalLayout_36.addWidget(self.label_for_option_music_rando)

        self.option_music_rando = QComboBox(self.verticalLayoutWidget_11)
        self.option_music_rando.setObjectName("option_music_rando")

        self.verticalLayout_36.addWidget(self.option_music_rando)

        self.verticalLayout_35.addLayout(self.verticalLayout_36)

        self.option_cutoff_gameover_music = QCheckBox(self.verticalLayoutWidget_11)
        self.option_cutoff_gameover_music.setObjectName("option_cutoff_gameover_music")

        self.verticalLayout_35.addWidget(self.option_cutoff_gameover_music)

        self.option_allow_custom_music = QCheckBox(self.verticalLayoutWidget_11)
        self.option_allow_custom_music.setObjectName("option_allow_custom_music")

        self.verticalLayout_35.addWidget(self.option_allow_custom_music)

        self.verticalSpacer_16 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_35.addItem(self.verticalSpacer_16)

        self.groupBox_17 = QGroupBox(self.tab)
        self.groupBox_17.setObjectName("groupBox_17")
        self.groupBox_17.setGeometry(QRect(10, 270, 331, 101))
        self.verticalLayoutWidget_16 = QWidget(self.groupBox_17)
        self.verticalLayoutWidget_16.setObjectName("verticalLayoutWidget_16")
        self.verticalLayoutWidget_16.setGeometry(QRect(10, 20, 311, 78))
        self.verticalLayout_39 = QVBoxLayout(self.verticalLayoutWidget_16)
        self.verticalLayout_39.setObjectName("verticalLayout_39")
        self.verticalLayout_39.setContentsMargins(0, 0, 0, 0)
        self.label_7 = QLabel(self.verticalLayoutWidget_16)
        self.label_7.setObjectName("label_7")

        self.verticalLayout_39.addWidget(self.label_7)

        self.presets_list = QComboBox(self.verticalLayoutWidget_16)
        self.presets_list.setObjectName("presets_list")

        self.verticalLayout_39.addWidget(self.presets_list)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.load_preset = QPushButton(self.verticalLayoutWidget_16)
        self.load_preset.setObjectName("load_preset")

        self.horizontalLayout_12.addWidget(self.load_preset)

        self.save_preset = QPushButton(self.verticalLayoutWidget_16)
        self.save_preset.setObjectName("save_preset")

        self.horizontalLayout_12.addWidget(self.save_preset)

        self.delete_preset = QPushButton(self.verticalLayoutWidget_16)
        self.delete_preset.setObjectName("delete_preset")

        self.horizontalLayout_12.addWidget(self.delete_preset)

        self.verticalLayout_39.addLayout(self.horizontalLayout_12)

        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName("tab_3")
        self.groupBox_4 = QGroupBox(self.tab_3)
        self.groupBox_4.setObjectName("groupBox_4")
        self.groupBox_4.setGeometry(QRect(10, 10, 1001, 51))
        self.horizontalLayoutWidget_3 = QWidget(self.groupBox_4)
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(10, 20, 981, 25))
        self.horizontalLayout_4 = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.progression_skyloft = QCheckBox(self.horizontalLayoutWidget_3)
        self.progression_skyloft.setObjectName("progression_skyloft")

        self.horizontalLayout_4.addWidget(self.progression_skyloft)

        self.progression_sky = QCheckBox(self.horizontalLayoutWidget_3)
        self.progression_sky.setObjectName("progression_sky")

        self.horizontalLayout_4.addWidget(self.progression_sky)

        self.progression_thunderhead = QCheckBox(self.horizontalLayoutWidget_3)
        self.progression_thunderhead.setObjectName("progression_thunderhead")

        self.horizontalLayout_4.addWidget(self.progression_thunderhead)

        self.progression_faron = QCheckBox(self.horizontalLayoutWidget_3)
        self.progression_faron.setObjectName("progression_faron")

        self.horizontalLayout_4.addWidget(self.progression_faron)

        self.progression_eldin = QCheckBox(self.horizontalLayoutWidget_3)
        self.progression_eldin.setObjectName("progression_eldin")

        self.horizontalLayout_4.addWidget(self.progression_eldin)

        self.progression_lanayru = QCheckBox(self.horizontalLayoutWidget_3)
        self.progression_lanayru.setObjectName("progression_lanayru")

        self.horizontalLayout_4.addWidget(self.progression_lanayru)

        self.groupBox = QGroupBox(self.tab_3)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setGeometry(QRect(10, 70, 1001, 191))
        self.gridLayoutWidget_3 = QWidget(self.groupBox)
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayoutWidget_3.setGeometry(QRect(10, 20, 981, 164))
        self.gridLayout_3 = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.progression_freestanding = QCheckBox(self.gridLayoutWidget_3)
        self.progression_freestanding.setObjectName("progression_freestanding")

        self.gridLayout_3.addWidget(self.progression_freestanding, 1, 4, 1, 1)

        self.progression_miscellaneous = QCheckBox(self.gridLayoutWidget_3)
        self.progression_miscellaneous.setObjectName("progression_miscellaneous")

        self.gridLayout_3.addWidget(self.progression_miscellaneous, 1, 5, 1, 1)

        self.progression_spiral_charge = QCheckBox(self.gridLayoutWidget_3)
        self.progression_spiral_charge.setObjectName("progression_spiral_charge")

        self.gridLayout_3.addWidget(self.progression_spiral_charge, 3, 0, 1, 1)

        self.progression_bombable = QCheckBox(self.gridLayoutWidget_3)
        self.progression_bombable.setObjectName("progression_bombable")

        self.gridLayout_3.addWidget(self.progression_bombable, 2, 3, 1, 1)

        self.progression_silent_realm = QCheckBox(self.gridLayoutWidget_3)
        self.progression_silent_realm.setObjectName("progression_silent_realm")

        self.gridLayout_3.addWidget(self.progression_silent_realm, 2, 0, 1, 1)

        self.progression_long = QCheckBox(self.gridLayoutWidget_3)
        self.progression_long.setObjectName("progression_long")

        self.gridLayout_3.addWidget(self.progression_long, 4, 2, 1, 1)

        self.progression_song = QCheckBox(self.gridLayoutWidget_3)
        self.progression_song.setObjectName("progression_song")

        self.gridLayout_3.addWidget(self.progression_song, 2, 5, 1, 1)

        self.progression_minigame = QCheckBox(self.gridLayoutWidget_3)
        self.progression_minigame.setObjectName("progression_minigame")

        self.gridLayout_3.addWidget(self.progression_minigame, 3, 2, 1, 1)

        self.progression_scrapper = QCheckBox(self.gridLayoutWidget_3)
        self.progression_scrapper.setObjectName("progression_scrapper")

        self.gridLayout_3.addWidget(self.progression_scrapper, 4, 5, 1, 1)

        self.progression_dungeon = QCheckBox(self.gridLayoutWidget_3)
        self.progression_dungeon.setObjectName("progression_dungeon")

        self.gridLayout_3.addWidget(self.progression_dungeon, 1, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.option_max_batreaux_reward = QComboBox(self.gridLayoutWidget_3)
        self.option_max_batreaux_reward.setObjectName("option_max_batreaux_reward")

        self.horizontalLayout_6.addWidget(self.option_max_batreaux_reward)

        self.label_for_option_max_batreaux_reward = QLabel(self.gridLayoutWidget_3)
        self.label_for_option_max_batreaux_reward.setObjectName(
            "label_for_option_max_batreaux_reward"
        )

        self.horizontalLayout_6.addWidget(self.label_for_option_max_batreaux_reward)

        self.gridLayout_3.addLayout(self.horizontalLayout_6, 3, 3, 1, 1)

        self.progression_crystal_quest = QCheckBox(self.gridLayoutWidget_3)
        self.progression_crystal_quest.setObjectName("progression_crystal_quest")

        self.gridLayout_3.addWidget(self.progression_crystal_quest, 4, 4, 1, 1)

        self.progression_peatrice = QCheckBox(self.gridLayoutWidget_3)
        self.progression_peatrice.setObjectName("progression_peatrice")

        self.gridLayout_3.addWidget(self.progression_peatrice, 3, 5, 1, 1)

        self.progression_expensive = QCheckBox(self.gridLayoutWidget_3)
        self.progression_expensive.setObjectName("progression_expensive")

        self.gridLayout_3.addWidget(self.progression_expensive, 5, 5, 1, 1)

        self.progression_combat = QCheckBox(self.gridLayoutWidget_3)
        self.progression_combat.setObjectName("progression_combat")

        self.gridLayout_3.addWidget(self.progression_combat, 2, 4, 1, 1)

        self.progression_crystal = QCheckBox(self.gridLayoutWidget_3)
        self.progression_crystal.setObjectName("progression_crystal")

        self.gridLayout_3.addWidget(self.progression_crystal, 3, 4, 1, 1)

        self.progression_cheap = QCheckBox(self.gridLayoutWidget_3)
        self.progression_cheap.setObjectName("progression_cheap")

        self.gridLayout_3.addWidget(self.progression_cheap, 5, 3, 1, 1)

        self.progression_free_gift = QCheckBox(self.gridLayoutWidget_3)
        self.progression_free_gift.setObjectName("progression_free_gift")

        self.gridLayout_3.addWidget(self.progression_free_gift, 1, 3, 1, 1)

        self.progression_mini_dungeon = QCheckBox(self.gridLayoutWidget_3)
        self.progression_mini_dungeon.setObjectName("progression_mini_dungeon")

        self.gridLayout_3.addWidget(self.progression_mini_dungeon, 1, 2, 1, 1)

        self.progression_fetch = QCheckBox(self.gridLayoutWidget_3)
        self.progression_fetch.setObjectName("progression_fetch")

        self.gridLayout_3.addWidget(self.progression_fetch, 4, 3, 1, 1)

        self.progression_digging = QCheckBox(self.gridLayoutWidget_3)
        self.progression_digging.setObjectName("progression_digging")

        self.gridLayout_3.addWidget(self.progression_digging, 2, 2, 1, 1)

        self.progression_beedle = QCheckBox(self.gridLayoutWidget_3)
        self.progression_beedle.setObjectName("progression_beedle")

        self.gridLayout_3.addWidget(self.progression_beedle, 5, 2, 1, 1)

        self.progression_medium = QCheckBox(self.gridLayoutWidget_3)
        self.progression_medium.setObjectName("progression_medium")

        self.gridLayout_3.addWidget(self.progression_medium, 5, 4, 1, 1)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.option_shopsanity = QComboBox(self.gridLayoutWidget_3)
        self.option_shopsanity.setObjectName("option_shopsanity")

        self.horizontalLayout_11.addWidget(self.option_shopsanity)

        self.label_10 = QLabel(self.gridLayoutWidget_3)
        self.label_10.setObjectName("label_10")

        self.horizontalLayout_11.addWidget(self.label_10)

        self.gridLayout_3.addLayout(self.horizontalLayout_11, 5, 0, 1, 1)

        self.progression_short = QCheckBox(self.gridLayoutWidget_3)
        self.progression_short.setObjectName("progression_short")

        self.gridLayout_3.addWidget(self.progression_short, 4, 0, 1, 1)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.option_rupeesanity = QComboBox(self.gridLayoutWidget_3)
        self.option_rupeesanity.setObjectName("option_rupeesanity")

        self.horizontalLayout_9.addWidget(self.option_rupeesanity)

        self.label_for_option_rupeesanity = QLabel(self.gridLayoutWidget_3)
        self.label_for_option_rupeesanity.setObjectName("label_for_option_rupeesanity")

        self.horizontalLayout_9.addWidget(self.label_for_option_rupeesanity)

        self.gridLayout_3.addLayout(self.horizontalLayout_9, 6, 0, 1, 1)

        self.progression_flooded_faron = QCheckBox(self.gridLayoutWidget_3)
        self.progression_flooded_faron.setObjectName("progression_flooded_faron")

        self.gridLayout_3.addWidget(self.progression_flooded_faron, 6, 2, 1, 1)

        self.groupBox_3 = QGroupBox(self.tab_3)
        self.groupBox_3.setObjectName("groupBox_3")
        self.groupBox_3.setGeometry(QRect(10, 270, 1001, 111))
        self.gridLayoutWidget_4 = QWidget(self.groupBox_3)
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.gridLayoutWidget_4.setGeometry(QRect(10, 20, 981, 83))
        self.gridLayout_4 = QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.progression_eldin_goddess = QCheckBox(self.gridLayoutWidget_4)
        self.progression_eldin_goddess.setObjectName("progression_eldin_goddess")

        self.gridLayout_4.addWidget(self.progression_eldin_goddess, 1, 1, 1, 1)

        self.progression_goddess = QCheckBox(self.gridLayoutWidget_4)
        self.progression_goddess.setObjectName("progression_goddess")

        self.gridLayout_4.addWidget(self.progression_goddess, 0, 0, 1, 1)

        self.progression_faron_goddess = QCheckBox(self.gridLayoutWidget_4)
        self.progression_faron_goddess.setObjectName("progression_faron_goddess")

        self.gridLayout_4.addWidget(self.progression_faron_goddess, 1, 0, 1, 1)

        self.progression_lanayru_goddess = QCheckBox(self.gridLayoutWidget_4)
        self.progression_lanayru_goddess.setObjectName("progression_lanayru_goddess")

        self.gridLayout_4.addWidget(self.progression_lanayru_goddess, 1, 2, 1, 1)

        self.progression_summit_goddess = QCheckBox(self.gridLayoutWidget_4)
        self.progression_summit_goddess.setObjectName("progression_summit_goddess")

        self.gridLayout_4.addWidget(self.progression_summit_goddess, 2, 1, 1, 1)

        self.progression_floria_goddess = QCheckBox(self.gridLayoutWidget_4)
        self.progression_floria_goddess.setObjectName("progression_floria_goddess")

        self.gridLayout_4.addWidget(self.progression_floria_goddess, 2, 0, 1, 1)

        self.progression_sand_sea_goddess = QCheckBox(self.gridLayoutWidget_4)
        self.progression_sand_sea_goddess.setObjectName("progression_sand_sea_goddess")

        self.gridLayout_4.addWidget(self.progression_sand_sea_goddess, 2, 2, 1, 1)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName("tab_4")
        self.groupBox_5 = QGroupBox(self.tab_4)
        self.groupBox_5.setObjectName("groupBox_5")
        self.groupBox_5.setGeometry(QRect(10, 10, 201, 251))
        self.verticalLayoutWidget = QWidget(self.groupBox_5)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 19, 181, 221))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_for_option_got_starting_state = QLabel(self.verticalLayoutWidget)
        self.label_for_option_got_starting_state.setObjectName(
            "label_for_option_got_starting_state"
        )

        self.verticalLayout_3.addWidget(self.label_for_option_got_starting_state)

        self.option_got_starting_state = QComboBox(self.verticalLayoutWidget)
        self.option_got_starting_state.setObjectName("option_got_starting_state")

        self.verticalLayout_3.addWidget(self.option_got_starting_state)

        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_for_option_got_sword_requirement = QLabel(self.verticalLayoutWidget)
        self.label_for_option_got_sword_requirement.setObjectName(
            "label_for_option_got_sword_requirement"
        )

        self.verticalLayout_4.addWidget(self.label_for_option_got_sword_requirement)

        self.option_got_sword_requirement = QComboBox(self.verticalLayoutWidget)
        self.option_got_sword_requirement.setObjectName("option_got_sword_requirement")

        self.verticalLayout_4.addWidget(self.option_got_sword_requirement)

        self.verticalLayout.addLayout(self.verticalLayout_4)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_for_option_got_dungeon_requirement = QLabel(
            self.verticalLayoutWidget
        )
        self.label_for_option_got_dungeon_requirement.setObjectName(
            "label_for_option_got_dungeon_requirement"
        )

        self.verticalLayout_5.addWidget(self.label_for_option_got_dungeon_requirement)

        self.option_got_dungeon_requirement = QComboBox(self.verticalLayoutWidget)
        self.option_got_dungeon_requirement.setObjectName(
            "option_got_dungeon_requirement"
        )

        self.verticalLayout_5.addWidget(self.option_got_dungeon_requirement)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_for_option_required_dungeon_count = QLabel(self.verticalLayoutWidget)
        self.label_for_option_required_dungeon_count.setObjectName(
            "label_for_option_required_dungeon_count"
        )

        self.horizontalLayout_8.addWidget(self.label_for_option_required_dungeon_count)

        self.option_required_dungeon_count = QSpinBox(self.verticalLayoutWidget)
        self.option_required_dungeon_count.setObjectName(
            "option_required_dungeon_count"
        )
        self.option_required_dungeon_count.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(
            self.option_required_dungeon_count.sizePolicy().hasHeightForWidth()
        )
        self.option_required_dungeon_count.setSizePolicy(sizePolicy2)
        self.option_required_dungeon_count.setMaximumSize(QSize(41, 16777215))

        self.horizontalLayout_8.addWidget(self.option_required_dungeon_count)

        self.verticalLayout_5.addLayout(self.horizontalLayout_8)

        self.verticalLayout.addLayout(self.verticalLayout_5)

        self.verticalSpacer_3 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.groupBox_7 = QGroupBox(self.tab_4)
        self.groupBox_7.setObjectName("groupBox_7")
        self.groupBox_7.setGeometry(QRect(630, 10, 191, 251))
        self.verticalLayoutWidget_7 = QWidget(self.groupBox_7)
        self.verticalLayoutWidget_7.setObjectName("verticalLayoutWidget_7")
        self.verticalLayoutWidget_7.setGeometry(QRect(10, 20, 181, 236))
        self.verticalLayout_10 = QVBoxLayout(self.verticalLayoutWidget_7)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_for_option_map_mode = QLabel(self.verticalLayoutWidget_7)
        self.label_for_option_map_mode.setObjectName("label_for_option_map_mode")

        self.verticalLayout_11.addWidget(self.label_for_option_map_mode)

        self.option_map_mode = QComboBox(self.verticalLayoutWidget_7)
        self.option_map_mode.setObjectName("option_map_mode")

        self.verticalLayout_11.addWidget(self.option_map_mode)

        self.verticalLayout_10.addLayout(self.verticalLayout_11)

        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.label_for_option_small_key_mode = QLabel(self.verticalLayoutWidget_7)
        self.label_for_option_small_key_mode.setObjectName(
            "label_for_option_small_key_mode"
        )

        self.verticalLayout_12.addWidget(self.label_for_option_small_key_mode)

        self.option_small_key_mode = QComboBox(self.verticalLayoutWidget_7)
        self.option_small_key_mode.setObjectName("option_small_key_mode")

        self.verticalLayout_12.addWidget(self.option_small_key_mode)

        self.verticalLayout_10.addLayout(self.verticalLayout_12)

        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.label_for_option_boss_key_mode = QLabel(self.verticalLayoutWidget_7)
        self.label_for_option_boss_key_mode.setObjectName(
            "label_for_option_boss_key_mode"
        )

        self.verticalLayout_13.addWidget(self.label_for_option_boss_key_mode)

        self.option_boss_key_mode = QComboBox(self.verticalLayoutWidget_7)
        self.option_boss_key_mode.setObjectName("option_boss_key_mode")

        self.verticalLayout_13.addWidget(self.option_boss_key_mode)

        self.verticalLayout_10.addLayout(self.verticalLayout_13)

        self.option_empty_unrequired_dungeons = QCheckBox(self.verticalLayoutWidget_7)
        self.option_empty_unrequired_dungeons.setObjectName(
            "option_empty_unrequired_dungeons"
        )

        self.verticalLayout_10.addWidget(self.option_empty_unrequired_dungeons)

        self.verticalLayout_40 = QVBoxLayout()
        self.verticalLayout_40.setObjectName("verticalLayout_40")
        self.label_for_option_sword_reward = QLabel(self.verticalLayoutWidget_7)
        self.label_for_option_sword_reward.setObjectName(
            "label_for_option_sword_reward"
        )

        self.verticalLayout_40.addWidget(self.label_for_option_sword_reward)

        self.option_sword_dungeon_reward = QComboBox(self.verticalLayoutWidget_7)
        self.option_sword_dungeon_reward.setObjectName("option_sword_dungeon_reward")

        self.verticalLayout_40.addWidget(self.option_sword_dungeon_reward)

        self.verticalLayout_10.addLayout(self.verticalLayout_40)

        self.verticalSpacer_4 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_10.addItem(self.verticalSpacer_4)

        self.groupBox_8 = QGroupBox(self.tab_4)
        self.groupBox_8.setObjectName("groupBox_8")
        self.groupBox_8.setGeometry(QRect(830, 10, 181, 251))
        self.verticalLayoutWidget_3 = QWidget(self.groupBox_8)
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(10, 20, 161, 221))
        self.verticalLayout_14 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.option_imp_2 = QCheckBox(self.verticalLayoutWidget_3)
        self.option_imp_2.setObjectName("option_imp_2")

        self.verticalLayout_14.addWidget(self.option_imp_2)

        self.option_horde = QCheckBox(self.verticalLayoutWidget_3)
        self.option_horde.setObjectName("option_horde")

        self.verticalLayout_14.addWidget(self.option_horde)

        self.option_g3 = QCheckBox(self.verticalLayoutWidget_3)
        self.option_g3.setObjectName("option_g3")

        self.verticalLayout_14.addWidget(self.option_g3)

        self.option_demise = QCheckBox(self.verticalLayoutWidget_3)
        self.option_demise.setObjectName("option_demise")

        self.verticalLayout_14.addWidget(self.option_demise)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.label_for_option_demise_count = QLabel(self.verticalLayoutWidget_3)
        self.label_for_option_demise_count.setObjectName(
            "label_for_option_demise_count"
        )

        self.horizontalLayout_20.addWidget(self.label_for_option_demise_count)

        self.option_demise_count = QSpinBox(self.verticalLayoutWidget_3)
        self.option_demise_count.setObjectName("option_demise_count")
        self.option_demise_count.setMaximumSize(QSize(41, 16777215))

        self.horizontalLayout_20.addWidget(self.option_demise_count)

        self.verticalLayout_14.addLayout(self.horizontalLayout_20)

        self.verticalSpacer_5 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_14.addItem(self.verticalSpacer_5)

        self.groupBox_2 = QGroupBox(self.tab_4)
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_2.setGeometry(QRect(220, 10, 191, 251))
        self.verticalLayoutWidget_2 = QWidget(self.groupBox_2)
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 20, 171, 221))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_for_option_open_thunderhead = QLabel(self.verticalLayoutWidget_2)
        self.label_for_option_open_thunderhead.setObjectName(
            "label_for_option_open_thunderhead"
        )

        self.verticalLayout_6.addWidget(self.label_for_option_open_thunderhead)

        self.option_open_thunderhead = QComboBox(self.verticalLayoutWidget_2)
        self.option_open_thunderhead.setObjectName("option_open_thunderhead")

        self.verticalLayout_6.addWidget(self.option_open_thunderhead)

        self.verticalLayout_2.addLayout(self.verticalLayout_6)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_for_option_open_lmf = QLabel(self.verticalLayoutWidget_2)
        self.label_for_option_open_lmf.setObjectName("label_for_option_open_lmf")

        self.verticalLayout_8.addWidget(self.label_for_option_open_lmf)

        self.option_open_lmf = QComboBox(self.verticalLayoutWidget_2)
        self.option_open_lmf.setObjectName("option_open_lmf")

        self.verticalLayout_8.addWidget(self.option_open_lmf)

        self.verticalLayout_2.addLayout(self.verticalLayout_8)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_for_option_starting_tablet_count = QLabel(
            self.verticalLayoutWidget_2
        )
        self.label_for_option_starting_tablet_count.setObjectName(
            "label_for_option_starting_tablet_count"
        )

        self.horizontalLayout_10.addWidget(self.label_for_option_starting_tablet_count)

        self.option_starting_tablet_count = QSpinBox(self.verticalLayoutWidget_2)
        self.option_starting_tablet_count.setObjectName("option_starting_tablet_count")
        self.option_starting_tablet_count.setMaximumSize(QSize(41, 16777215))

        self.horizontalLayout_10.addWidget(self.option_starting_tablet_count)

        self.verticalLayout_2.addLayout(self.horizontalLayout_10)

        self.option_open_et = QCheckBox(self.verticalLayoutWidget_2)
        self.option_open_et.setObjectName("option_open_et")

        self.verticalLayout_2.addWidget(self.option_open_et)

        self.verticalSpacer_2 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.groupBox_6 = QGroupBox(self.tab_4)
        self.groupBox_6.setObjectName("groupBox_6")
        self.groupBox_6.setGeometry(QRect(420, 10, 201, 251))
        self.verticalLayoutWidget_4 = QWidget(self.groupBox_6)
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(10, 19, 186, 221))
        self.verticalLayout_7 = QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_for_option_randomize_entrances = QLabel(self.verticalLayoutWidget_4)
        self.label_for_option_randomize_entrances.setObjectName(
            "label_for_option_randomize_entrances"
        )

        self.verticalLayout_9.addWidget(self.label_for_option_randomize_entrances)

        self.option_randomize_entrances = QComboBox(self.verticalLayoutWidget_4)
        self.option_randomize_entrances.setObjectName("option_randomize_entrances")

        self.verticalLayout_9.addWidget(self.option_randomize_entrances)

        self.verticalLayout_7.addLayout(self.verticalLayout_9)

        self.option_randomize_trials = QCheckBox(self.verticalLayoutWidget_4)
        self.option_randomize_trials.setObjectName("option_randomize_trials")

        self.verticalLayout_7.addWidget(self.option_randomize_trials)

        self.verticalLayout_trialshuffle = QVBoxLayout()
        self.verticalLayout_trialshuffle.setObjectName("verticalLayout_trialshuffle")
        self.label_4 = QLabel(self.verticalLayoutWidget_4)
        self.label_4.setObjectName("label_4")

        self.verticalLayout_trialshuffle.addWidget(self.label_4)

        self.option_shuffle_trial_objects = QComboBox(self.verticalLayoutWidget_4)
        self.option_shuffle_trial_objects.setObjectName("option_shuffle_trial_objects")

        self.verticalLayout_trialshuffle.addWidget(self.option_shuffle_trial_objects)

        self.verticalLayout_7.addLayout(self.verticalLayout_trialshuffle)

        self.verticalSpacer = QSpacerItem(
            20, 70, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding
        )

        self.verticalLayout_7.addItem(self.verticalSpacer)

        self.groupBox_9 = QGroupBox(self.tab_4)
        self.groupBox_9.setObjectName("groupBox_9")
        self.groupBox_9.setGeometry(QRect(10, 270, 201, 241))
        self.verticalLayoutWidget_5 = QWidget(self.groupBox_9)
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayoutWidget_5.setGeometry(QRect(10, 20, 181, 210))
        self.verticalLayout_15 = QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_28 = QVBoxLayout()
        self.verticalLayout_28.setObjectName("verticalLayout_28")
        self.label_for_option_starting_sword = QLabel(self.verticalLayoutWidget_5)
        self.label_for_option_starting_sword.setObjectName(
            "label_for_option_starting_sword"
        )

        self.verticalLayout_28.addWidget(self.label_for_option_starting_sword)

        self.option_starting_sword = QComboBox(self.verticalLayoutWidget_5)
        self.option_starting_sword.setObjectName("option_starting_sword")

        self.verticalLayout_28.addWidget(self.option_starting_sword)

        self.verticalLayout_15.addLayout(self.verticalLayout_28)

        self.option_start_pouch = QCheckBox(self.verticalLayoutWidget_5)
        self.option_start_pouch.setObjectName("option_start_pouch")

        self.verticalLayout_15.addWidget(self.option_start_pouch)

        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.label_for_option_rupoor = QLabel(self.verticalLayoutWidget_5)
        self.label_for_option_rupoor.setObjectName("label_for_option_rupoor")

        self.verticalLayout_16.addWidget(self.label_for_option_rupoor)

        self.option_rupoor_mode = QComboBox(self.verticalLayoutWidget_5)
        self.option_rupoor_mode.setObjectName("option_rupoor_mode")

        self.verticalLayout_16.addWidget(self.option_rupoor_mode)

        self.verticalLayout_15.addLayout(self.verticalLayout_16)

        self.option_gondo_upgrades = QCheckBox(self.verticalLayoutWidget_5)
        self.option_gondo_upgrades.setObjectName("option_gondo_upgrades")

        self.verticalLayout_15.addWidget(self.option_gondo_upgrades)

        self.option_hero_mode = QCheckBox(self.verticalLayoutWidget_5)
        self.option_hero_mode.setObjectName("option_hero_mode")

        self.verticalLayout_15.addWidget(self.option_hero_mode)

        self.option_fix_bit_crashes = QCheckBox(self.verticalLayoutWidget_5)
        self.option_fix_bit_crashes.setObjectName("option_fix_bit_crashes")

        self.verticalLayout_15.addWidget(self.option_fix_bit_crashes)

        self.verticalSpacer_17 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_15.addItem(self.verticalSpacer_17)

        self.groupBox_16 = QGroupBox(self.tab_4)
        self.groupBox_16.setObjectName("groupBox_16")
        self.groupBox_16.setGeometry(QRect(220, 270, 191, 241))
        self.verticalLayoutWidget_15 = QWidget(self.groupBox_16)
        self.verticalLayoutWidget_15.setObjectName("verticalLayoutWidget_15")
        self.verticalLayoutWidget_15.setGeometry(QRect(10, 20, 171, 211))
        self.verticalLayout_31 = QVBoxLayout(self.verticalLayoutWidget_15)
        self.verticalLayout_31.setObjectName("verticalLayout_31")
        self.verticalLayout_31.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_37 = QVBoxLayout()
        self.verticalLayout_37.setObjectName("verticalLayout_37")

        self.verticalLayout_31.addLayout(self.verticalLayout_37)

        self.option_triforce_required = QCheckBox(self.verticalLayoutWidget_15)
        self.option_triforce_required.setObjectName("option_triforce_required")

        self.verticalLayout_31.addWidget(self.option_triforce_required)

        self.verticalLayout_38 = QVBoxLayout()
        self.verticalLayout_38.setObjectName("verticalLayout_38")
        self.label_for_option_triforce_shuffle = QLabel(self.verticalLayoutWidget_15)
        self.label_for_option_triforce_shuffle.setObjectName(
            "label_for_option_triforce_shuffle"
        )

        self.verticalLayout_38.addWidget(self.label_for_option_triforce_shuffle)

        self.option_triforce_shuffle = QComboBox(self.verticalLayoutWidget_15)
        self.option_triforce_shuffle.setObjectName("option_triforce_shuffle")

        self.verticalLayout_38.addWidget(self.option_triforce_shuffle)

        self.verticalLayout_31.addLayout(self.verticalLayout_38)

        self.verticalSpacer_6 = QSpacerItem(
            20, 70, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding
        )

        self.verticalLayout_31.addItem(self.verticalSpacer_6)

        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName("tab_5")
        self.layoutWidget = QWidget(self.tab_5)
        self.layoutWidget.setObjectName("layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 1001, 499))
        self.verticalLayout_18 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.label_for_option_logic_mode = QLabel(self.layoutWidget)
        self.label_for_option_logic_mode.setObjectName("label_for_option_logic_mode")

        self.verticalLayout_18.addWidget(self.label_for_option_logic_mode)

        self.option_logic_mode = QComboBox(self.layoutWidget)
        self.option_logic_mode.setObjectName("option_logic_mode")

        self.verticalLayout_18.addWidget(self.option_logic_mode)

        self.verticalSpacer_7 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_18.addItem(self.verticalSpacer_7)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_19 = QVBoxLayout()
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName("label")

        self.verticalLayout_19.addWidget(self.label)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.enabled_locations = QListView(self.layoutWidget)
        self.enabled_locations.setObjectName("enabled_locations")

        self.horizontalLayout_17.addWidget(self.enabled_locations)

        self.verticalLayout_20 = QVBoxLayout()
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.enable_location = QPushButton(self.layoutWidget)
        self.enable_location.setObjectName("enable_location")

        self.verticalLayout_20.addWidget(self.enable_location)

        self.disable_location = QPushButton(self.layoutWidget)
        self.disable_location.setObjectName("disable_location")

        self.verticalLayout_20.addWidget(self.disable_location)

        self.horizontalLayout_17.addLayout(self.verticalLayout_20)

        self.disabled_locations = QListWidget(self.layoutWidget)
        self.disabled_locations.setObjectName("disabled_locations")

        self.horizontalLayout_17.addWidget(self.disabled_locations)

        self.verticalLayout_19.addLayout(self.horizontalLayout_17)

        self.horizontalLayout_2.addLayout(self.verticalLayout_19)

        self.verticalLayout_25 = QVBoxLayout()
        self.verticalLayout_25.setObjectName("verticalLayout_25")
        self.label_5 = QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")

        self.verticalLayout_25.addWidget(self.label_5)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.enabled_tricks = QListView(self.layoutWidget)
        self.enabled_tricks.setObjectName("enabled_tricks")

        self.horizontalLayout_18.addWidget(self.enabled_tricks)

        self.verticalLayout_21 = QVBoxLayout()
        self.verticalLayout_21.setObjectName("verticalLayout_21")
        self.enable_trick = QPushButton(self.layoutWidget)
        self.enable_trick.setObjectName("enable_trick")

        self.verticalLayout_21.addWidget(self.enable_trick)

        self.disable_trick = QPushButton(self.layoutWidget)
        self.disable_trick.setObjectName("disable_trick")

        self.verticalLayout_21.addWidget(self.disable_trick)

        self.horizontalLayout_18.addLayout(self.verticalLayout_21)

        self.disabled_tricks = QListView(self.layoutWidget)
        self.disabled_tricks.setObjectName("disabled_tricks")

        self.horizontalLayout_18.addWidget(self.disabled_tricks)

        self.verticalLayout_25.addLayout(self.horizontalLayout_18)

        self.horizontalLayout_2.addLayout(self.verticalLayout_25)

        self.verticalLayout_18.addLayout(self.horizontalLayout_2)

        self.tabWidget.addTab(self.tab_5, "")
        self.tab_7 = QWidget()
        self.tab_7.setObjectName("tab_7")
        self.groupBox_10 = QGroupBox(self.tab_7)
        self.groupBox_10.setObjectName("groupBox_10")
        self.groupBox_10.setGeometry(QRect(10, 10, 191, 231))
        self.verticalLayoutWidget_12 = QWidget(self.groupBox_10)
        self.verticalLayoutWidget_12.setObjectName("verticalLayoutWidget_12")
        self.verticalLayoutWidget_12.setGeometry(QRect(10, 20, 175, 207))
        self.verticalLayout_22 = QVBoxLayout(self.verticalLayoutWidget_12)
        self.verticalLayout_22.setObjectName("verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_24 = QVBoxLayout()
        self.verticalLayout_24.setObjectName("verticalLayout_24")
        self.label_for_option_hint_distribution = QLabel(self.verticalLayoutWidget_12)
        self.label_for_option_hint_distribution.setObjectName(
            "label_for_option_hint_distribution"
        )

        self.verticalLayout_24.addWidget(self.label_for_option_hint_distribution)

        self.option_hint_distribution = QComboBox(self.verticalLayoutWidget_12)
        self.option_hint_distribution.setObjectName("option_hint_distribution")

        self.verticalLayout_24.addWidget(self.option_hint_distribution)

        self.verticalLayout_22.addLayout(self.verticalLayout_24)

        self.option_cube_sots = QCheckBox(self.verticalLayoutWidget_12)
        self.option_cube_sots.setObjectName("option_cube_sots")

        self.verticalLayout_22.addWidget(self.option_cube_sots)

        self.option_precise_item = QCheckBox(self.verticalLayoutWidget_12)
        self.option_precise_item.setObjectName("option_precise_item")

        self.verticalLayout_22.addWidget(self.option_precise_item)

        self.verticalSpacer_11 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_22.addItem(self.verticalSpacer_11)

        self.groupBox_11 = QGroupBox(self.tab_7)
        self.groupBox_11.setObjectName("groupBox_11")
        self.groupBox_11.setGeometry(QRect(210, 10, 191, 231))
        self.verticalLayoutWidget_6 = QWidget(self.groupBox_11)
        self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
        self.verticalLayoutWidget_6.setGeometry(QRect(10, 20, 171, 201))
        self.verticalLayout_26 = QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayout_26.setObjectName("verticalLayout_26")
        self.verticalLayout_26.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_27 = QVBoxLayout()
        self.verticalLayout_27.setObjectName("verticalLayout_27")
        self.label_6 = QLabel(self.verticalLayoutWidget_6)
        self.label_6.setObjectName("label_6")

        self.verticalLayout_27.addWidget(self.label_6)

        self.option_song_hints = QComboBox(self.verticalLayoutWidget_6)
        self.option_song_hints.setObjectName("option_song_hints")

        self.verticalLayout_27.addWidget(self.option_song_hints)

        self.verticalLayout_26.addLayout(self.verticalLayout_27)

        self.option_impa_sot_hint = QCheckBox(self.verticalLayoutWidget_6)
        self.option_impa_sot_hint.setObjectName("option_impa_sot_hint")

        self.verticalLayout_26.addWidget(self.option_impa_sot_hint)

        self.verticalSpacer_10 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_26.addItem(self.verticalSpacer_10)

        self.tabWidget.addTab(self.tab_7, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName("tab_6")
        self.horizontalLayoutWidget_5 = QWidget(self.tab_6)
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")
        self.horizontalLayoutWidget_5.setGeometry(QRect(10, 10, 1011, 451))
        self.horizontalLayout_5 = QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.randomized_items = QListView(self.horizontalLayoutWidget_5)
        self.randomized_items.setObjectName("randomized_items")

        self.horizontalLayout_5.addWidget(self.randomized_items)

        self.verticalLayout_23 = QVBoxLayout()
        self.verticalLayout_23.setObjectName("verticalLayout_23")
        self.verticalSpacer_9 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_23.addItem(self.verticalSpacer_9)

        self.randomize_item = QPushButton(self.horizontalLayoutWidget_5)
        self.randomize_item.setObjectName("randomize_item")

        self.verticalLayout_23.addWidget(self.randomize_item)

        self.start_with_item = QPushButton(self.horizontalLayoutWidget_5)
        self.start_with_item.setObjectName("start_with_item")

        self.verticalLayout_23.addWidget(self.start_with_item)

        self.verticalSpacer_8 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_23.addItem(self.verticalSpacer_8)

        self.horizontalLayout_5.addLayout(self.verticalLayout_23)

        self.starting_items = QListView(self.horizontalLayoutWidget_5)
        self.starting_items.setObjectName("starting_items")

        self.horizontalLayout_5.addWidget(self.starting_items)

        self.tabWidget.addTab(self.tab_6, "")
        self.verticalLayoutWidget_10 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_10.setObjectName("verticalLayoutWidget_10")
        self.verticalLayoutWidget_10.setGeometry(QRect(10, 615, 1031, 110))
        self.verticalLayout_30 = QVBoxLayout(self.verticalLayoutWidget_10)
        self.verticalLayout_30.setObjectName("verticalLayout_30")
        self.verticalLayout_30.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.permalink_label = QLabel(self.verticalLayoutWidget_10)
        self.permalink_label.setObjectName("permalink_label")

        self.horizontalLayout_3.addWidget(self.permalink_label)

        self.permalink = QLineEdit(self.verticalLayoutWidget_10)
        self.permalink.setObjectName("permalink")

        self.horizontalLayout_3.addWidget(self.permalink)

        self.verticalLayout_30.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.label_3 = QLabel(self.verticalLayoutWidget_10)
        self.label_3.setObjectName("label_3")
        self.label_3.setToolTipDuration(-1)
        self.label_3.setLayoutDirection(Qt.LeftToRight)
        self.label_3.setAutoFillBackground(False)
        self.label_3.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_16.addWidget(self.label_3)

        self.seed = QLineEdit(self.verticalLayoutWidget_10)
        self.seed.setObjectName("seed")

        self.horizontalLayout_16.addWidget(self.seed)

        self.seed_button = QPushButton(self.verticalLayoutWidget_10)
        self.seed_button.setObjectName("seed_button")

        self.horizontalLayout_16.addWidget(self.seed_button)

        self.verticalLayout_30.addLayout(self.horizontalLayout_16)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.randomize_button = QPushButton(self.verticalLayoutWidget_10)
        self.randomize_button.setObjectName("randomize_button")

        self.horizontalLayout.addWidget(self.randomize_button)

        self.verticalLayout_30.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(2)
        self.option_sword_dungeon_reward.setCurrentIndex(-1)
        self.option_randomize_entrances.setCurrentIndex(-1)
        self.option_triforce_shuffle.setCurrentIndex(-1)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "Skyward Sword Randomizer", None)
        )
        self.option_description.setText("")
        # if QT_CONFIG(tooltip)
        self.tabWidget.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.label_2.setText(
            QCoreApplication.translate("MainWindow", "Output Folder", None)
        )
        self.ouput_folder_browse_button.setText(
            QCoreApplication.translate("MainWindow", "Browse", None)
        )
        self.option_plando.setText(
            QCoreApplication.translate("MainWindow", "Enable Plandomizer", None)
        )
        self.plando_file_browse.setText(
            QCoreApplication.translate("MainWindow", "Browse", None)
        )
        self.groupBox_12.setTitle(
            QCoreApplication.translate("MainWindow", "Additional File Generation", None)
        )
        self.option_no_spoiler_log.setText(
            QCoreApplication.translate("MainWindow", "No Spoiler Log", None)
        )
        self.option_json_spoiler.setText(
            QCoreApplication.translate("MainWindow", "Generate JSON Spoiler Log", None)
        )
        self.option_out_placement_file.setText(
            QCoreApplication.translate("MainWindow", "Generate Placement File", None)
        )
        self.groupBox_13.setTitle(
            QCoreApplication.translate("MainWindow", "Advanced Options", None)
        )
        self.option_dry_run.setText(
            QCoreApplication.translate("MainWindow", "Dry Run", None)
        )
        self.groupBox_14.setTitle(
            QCoreApplication.translate("MainWindow", "Cosmetics", None)
        )
        self.option_tunic_swap.setText(
            QCoreApplication.translate("MainWindow", "Tunic Swap", None)
        )
        self.groupBox_15.setTitle(
            QCoreApplication.translate("MainWindow", "Randomize Music", None)
        )
        self.label_for_option_music_rando.setText(
            QCoreApplication.translate("MainWindow", "Randomize Music", None)
        )
        self.option_cutoff_gameover_music.setText(
            QCoreApplication.translate("MainWindow", "Cutoff Game Over Music", None)
        )
        self.option_allow_custom_music.setText(
            QCoreApplication.translate("MainWindow", "Allow Custom Music", None)
        )
        self.groupBox_17.setTitle(
            QCoreApplication.translate("MainWindow", "Presets", None)
        )
        self.label_7.setText(
            QCoreApplication.translate(
                "MainWindow", "Presets overwrite ALL game settings", None
            )
        )
        self.load_preset.setText(QCoreApplication.translate("MainWindow", "Load", None))
        self.save_preset.setText(QCoreApplication.translate("MainWindow", "Save", None))
        self.delete_preset.setText(
            QCoreApplication.translate("MainWindow", "Delete", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab),
            QCoreApplication.translate("MainWindow", "Setup", None),
        )
        self.groupBox_4.setTitle(
            QCoreApplication.translate(
                "MainWindow",
                "What areas of the world should progress items appear?",
                None,
            )
        )
        self.progression_skyloft.setText(
            QCoreApplication.translate("MainWindow", "Skyloft", None)
        )
        self.progression_sky.setText(
            QCoreApplication.translate("MainWindow", "The Sky", None)
        )
        self.progression_thunderhead.setText(
            QCoreApplication.translate("MainWindow", "Thunderhead", None)
        )
        self.progression_faron.setText(
            QCoreApplication.translate("MainWindow", "Faron", None)
        )
        self.progression_eldin.setText(
            QCoreApplication.translate("MainWindow", "Eldin", None)
        )
        self.progression_lanayru.setText(
            QCoreApplication.translate("MainWindow", "Lanayru", None)
        )
        self.groupBox.setTitle(
            QCoreApplication.translate(
                "MainWindow", "Where should progress items appear?", None
            )
        )
        self.progression_freestanding.setText(
            QCoreApplication.translate("MainWindow", "Freestanding Items", None)
        )
        self.progression_miscellaneous.setText(
            QCoreApplication.translate("MainWindow", "Miscellaneous", None)
        )
        self.progression_spiral_charge.setText(
            QCoreApplication.translate("MainWindow", "Spiral Charge Chests", None)
        )
        self.progression_bombable.setText(
            QCoreApplication.translate("MainWindow", "Bombable Walls", None)
        )
        self.progression_silent_realm.setText(
            QCoreApplication.translate("MainWindow", "Silent Realms", None)
        )
        self.progression_long.setText(
            QCoreApplication.translate("MainWindow", "Long Quests", None)
        )
        self.progression_song.setText(
            QCoreApplication.translate("MainWindow", "Songs", None)
        )
        self.progression_minigame.setText(
            QCoreApplication.translate("MainWindow", "Minigames", None)
        )
        self.progression_scrapper.setText(
            QCoreApplication.translate("MainWindow", "Scrapper Quests", None)
        )
        self.progression_dungeon.setText(
            QCoreApplication.translate("MainWindow", "Dungeons", None)
        )
        self.label_for_option_max_batreaux_reward.setText(
            QCoreApplication.translate("MainWindow", "Batreaux", None)
        )
        self.progression_crystal_quest.setText(
            QCoreApplication.translate("MainWindow", "Crystal Quests", None)
        )
        self.progression_peatrice.setText(
            QCoreApplication.translate("MainWindow", "Peatrice", None)
        )
        self.progression_expensive.setText(
            QCoreApplication.translate("MainWindow", "Expensive Purchases", None)
        )
        self.progression_combat.setText(
            QCoreApplication.translate("MainWindow", "Combat Rewards", None)
        )
        self.progression_crystal.setText(
            QCoreApplication.translate("MainWindow", "Loose Crystals", None)
        )
        self.progression_cheap.setText(
            QCoreApplication.translate("MainWindow", "Cheap Purchases", None)
        )
        self.progression_free_gift.setText(
            QCoreApplication.translate("MainWindow", "Free Gifts", None)
        )
        self.progression_mini_dungeon.setText(
            QCoreApplication.translate("MainWindow", "Mini Dungeons", None)
        )
        self.progression_fetch.setText(
            QCoreApplication.translate("MainWindow", "Fetch Quests", None)
        )
        self.progression_digging.setText(
            QCoreApplication.translate("MainWindow", "Digging Spots", None)
        )
        self.progression_beedle.setText(
            QCoreApplication.translate("MainWindow", "Beedle's Shop", None)
        )
        self.progression_medium.setText(
            QCoreApplication.translate("MainWindow", "Medium Cost Purchases", None)
        )
        self.label_10.setText(
            QCoreApplication.translate("MainWindow", "Shop Mode", None)
        )
        self.progression_short.setText(
            QCoreApplication.translate("MainWindow", "Short Quests", None)
        )
        self.label_for_option_rupeesanity.setText(
            QCoreApplication.translate("MainWindow", "Rupeesanity", None)
        )
        self.progression_flooded_faron.setText(
            QCoreApplication.translate("MainWindow", "Flooded Faron", None)
        )
        self.groupBox_3.setTitle(
            QCoreApplication.translate("MainWindow", "Goddess Cube Options", None)
        )
        self.progression_eldin_goddess.setText(
            QCoreApplication.translate("MainWindow", "Eldin Volcano", None)
        )
        self.progression_goddess.setText(
            QCoreApplication.translate("MainWindow", "Enabled", None)
        )
        self.progression_faron_goddess.setText(
            QCoreApplication.translate("MainWindow", "Faron Woods", None)
        )
        self.progression_lanayru_goddess.setText(
            QCoreApplication.translate("MainWindow", "Lanayru Desert", None)
        )
        self.progression_summit_goddess.setText(
            QCoreApplication.translate("MainWindow", "Volcano Summit", None)
        )
        self.progression_floria_goddess.setText(
            QCoreApplication.translate("MainWindow", "Lake Floria", None)
        )
        self.progression_sand_sea_goddess.setText(
            QCoreApplication.translate("MainWindow", "Sand Sea", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_3),
            QCoreApplication.translate("MainWindow", "Progress Locations", None),
        )
        # if QT_CONFIG(tooltip)
        self.tab_4.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.groupBox_5.setTitle(
            QCoreApplication.translate(
                "MainWindow", "Gate of Time and Horde Door", None
            )
        )
        self.label_for_option_got_starting_state.setText(
            QCoreApplication.translate("MainWindow", "Starting State", None)
        )
        self.label_for_option_got_sword_requirement.setText(
            QCoreApplication.translate("MainWindow", "Sword Requirement", None)
        )
        self.label_for_option_got_dungeon_requirement.setText(
            QCoreApplication.translate("MainWindow", "Dungeon Requirement", None)
        )
        self.label_for_option_required_dungeon_count.setText(
            QCoreApplication.translate("MainWindow", "Required Dungeons", None)
        )
        self.groupBox_7.setTitle(
            QCoreApplication.translate("MainWindow", "Dungeons", None)
        )
        self.label_for_option_map_mode.setText(
            QCoreApplication.translate("MainWindow", "Map Mode", None)
        )
        self.label_for_option_small_key_mode.setText(
            QCoreApplication.translate("MainWindow", "Small Keys", None)
        )
        self.label_for_option_boss_key_mode.setText(
            QCoreApplication.translate("MainWindow", "Boss Keys", None)
        )
        self.option_empty_unrequired_dungeons.setText(
            QCoreApplication.translate("MainWindow", "Empty Unrequired Dungeons", None)
        )
        self.label_for_option_sword_reward.setText(
            QCoreApplication.translate("MainWindow", "Sword Dungeon Rewards", None)
        )
        self.option_sword_dungeon_reward.setCurrentText("")
        self.groupBox_8.setTitle(
            QCoreApplication.translate("MainWindow", "Endgame Bosses", None)
        )
        self.option_imp_2.setText(
            QCoreApplication.translate("MainWindow", "Skip Imprisoned 2", None)
        )
        self.option_horde.setText(
            QCoreApplication.translate("MainWindow", "Skip Horde", None)
        )
        self.option_g3.setText(
            QCoreApplication.translate("MainWindow", "Skip Ghirahim 3", None)
        )
        self.option_demise.setText(
            QCoreApplication.translate("MainWindow", "Skip Demise", None)
        )
        self.label_for_option_demise_count.setText(
            QCoreApplication.translate("MainWindow", "Demise Count", None)
        )
        self.groupBox_2.setTitle(
            QCoreApplication.translate("MainWindow", "Open Settings", None)
        )
        self.label_for_option_open_thunderhead.setText(
            QCoreApplication.translate("MainWindow", "Open Thunderhead", None)
        )
        self.label_for_option_open_lmf.setText(
            QCoreApplication.translate(
                "MainWindow", "Open Lanayru Mining Facility", None
            )
        )
        self.label_for_option_starting_tablet_count.setText(
            QCoreApplication.translate("MainWindow", "Starting Tablets", None)
        )
        self.option_open_et.setText(
            QCoreApplication.translate("MainWindow", "Open Earth Temple", None)
        )
        self.groupBox_6.setTitle(
            QCoreApplication.translate("MainWindow", "Overworld", None)
        )
        self.label_for_option_randomize_entrances.setText(
            QCoreApplication.translate("MainWindow", "Randomize Entrances", None)
        )
        self.option_randomize_entrances.setCurrentText("")
        self.option_randomize_trials.setText(
            QCoreApplication.translate(
                "MainWindow", "Randomize Silent Realm Gates", None
            )
        )
        self.label_4.setText(
            QCoreApplication.translate("MainWindow", "Shuffle Trial Objects", None)
        )
        self.groupBox_9.setTitle(
            QCoreApplication.translate("MainWindow", "Additional Options", None)
        )
        self.label_for_option_starting_sword.setText(
            QCoreApplication.translate("MainWindow", "Starting Sword", None)
        )
        self.option_start_pouch.setText(
            QCoreApplication.translate("MainWindow", "Start with Adventure Pouch", None)
        )
        self.label_for_option_rupoor.setText(
            QCoreApplication.translate("MainWindow", "Rupoor Mode", None)
        )
        self.option_gondo_upgrades.setText(
            QCoreApplication.translate("MainWindow", "Place Scrap Shop Upgrades", None)
        )
        self.option_hero_mode.setText(
            QCoreApplication.translate("MainWindow", "Hero Mode", None)
        )
        self.option_fix_bit_crashes.setText(
            QCoreApplication.translate("MainWindow", "Fix BiT crashes", None)
        )
        self.groupBox_16.setTitle(
            QCoreApplication.translate("MainWindow", "Triforce", None)
        )
        self.option_triforce_required.setText(
            QCoreApplication.translate("MainWindow", "Triforce Required", None)
        )
        self.label_for_option_triforce_shuffle.setText(
            QCoreApplication.translate("MainWindow", "Triforce Shuffle", None)
        )
        self.option_triforce_shuffle.setCurrentText("")
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_4),
            QCoreApplication.translate("MainWindow", "Additional Settings", None),
        )
        self.label_for_option_logic_mode.setText(
            QCoreApplication.translate("MainWindow", "Logic Mode", None)
        )
        self.label.setText(
            QCoreApplication.translate("MainWindow", "Exclude Locations", None)
        )
        self.enable_location.setText(
            QCoreApplication.translate("MainWindow", "<---", None)
        )
        self.disable_location.setText(
            QCoreApplication.translate("MainWindow", "--->", None)
        )
        self.label_5.setText(
            QCoreApplication.translate("MainWindow", "Enable Tricks", None)
        )
        self.enable_trick.setText(
            QCoreApplication.translate("MainWindow", "<---", None)
        )
        self.disable_trick.setText(
            QCoreApplication.translate("MainWindow", "--->", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_5),
            QCoreApplication.translate("MainWindow", "Logic Settings", None),
        )
        self.groupBox_10.setTitle(
            QCoreApplication.translate("MainWindow", "Gossip Stone Hints", None)
        )
        self.label_for_option_hint_distribution.setText(
            QCoreApplication.translate("MainWindow", "Hint Distribution", None)
        )
        self.option_cube_sots.setText(
            QCoreApplication.translate("MainWindow", "Separate Cube SotS Hints", None)
        )
        self.option_precise_item.setText(
            QCoreApplication.translate("MainWindow", "Precise Item Hints", None)
        )
        self.groupBox_11.setTitle(
            QCoreApplication.translate("MainWindow", "Other Hints", None)
        )
        self.label_6.setText(
            QCoreApplication.translate("MainWindow", "Song Hints", None)
        )
        self.option_impa_sot_hint.setText(
            QCoreApplication.translate("MainWindow", "Impa Stone of Trials Hint", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_7),
            QCoreApplication.translate("MainWindow", "Hints", None),
        )
        self.randomize_item.setText(
            QCoreApplication.translate("MainWindow", "<--", None)
        )
        self.start_with_item.setText(
            QCoreApplication.translate("MainWindow", "-->", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_6),
            QCoreApplication.translate("MainWindow", "Starting Inventory", None),
        )
        self.permalink_label.setText(
            QCoreApplication.translate(
                "MainWindow", "Permalink (copy paste to share your settings)", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.label_3.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(statustip)
        self.label_3.setStatusTip("")
        # endif // QT_CONFIG(statustip)
        self.label_3.setText(QCoreApplication.translate("MainWindow", "Seed", None))
        self.seed_button.setText(
            QCoreApplication.translate("MainWindow", "New Seed", None)
        )
        self.randomize_button.setText(
            QCoreApplication.translate("MainWindow", "Randomize", None)
        )

    # retranslateUi
