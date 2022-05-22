from PyQt5 import QtWidgets, QtCore, QtGui


class CustomWidget(QtWidgets.QWidget):
    def __init__(self, user, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        self.user = user
        # self.setGeometry(QtCore.QRect(0, 0, 211, 90))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        # self.UserImage = QtWidgets.QLabel(self)
        # self.UserImage.setText("This is an Image")
        # self.UserImage.setObjectName("UserImage")
        # self.horizontalLayout.addWidget(self.UserImage)
        # self.verticalLayout = QtWidgets.QVBoxLayout()
        # self.verticalLayout.setObjectName("verticalLayout")
        # self.UserName = QtWidgets.QLabel(self)
        # self.UserName.setText("My name is jeff")
        # self.UserName.setObjectName("UserName")
        # self.verticalLayout.addWidget(self.UserName)
        # self.UserStatus = QtWidgets.QLabel(self)
        # self.UserStatus.setText("I am available")
        # self.UserStatus.setObjectName("UserStatus")
        # self.verticalLayout.addWidget(self.UserStatus)
        self.setGeometry(QtCore.QRect(0, 0, 281, 51))
        self.setObjectName("chat_bot_widget")
        self.chat_bot = QtWidgets.QLabel(self)
        self.chat_bot.setGeometry(QtCore.QRect(50, 5, 231, 41))
        self.chat_bot.setStyleSheet("background: rgb(255, 255, 255);\n"
                                    "border-radius: 10px;\n"
                                    "padding-left: 10px")
        self.chat_bot.setObjectName("chat_bot")
        self.label_7 = QtWidgets.QLabel(self)
        self.label_7.setGeometry(QtCore.QRect(10, 10, 31, 31))
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap("icon/bot.png"))
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")

        self.horizontalLayout.addLayout(self)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        # self.setGeometry(QtCore.QRect(0, 0, 281, 51))
        # self.setObjectName("chat_bot_widget")
        # self.chat_bot = QtWidgets.QLabel(self)
        # self.chat_bot.setGeometry(QtCore.QRect(50, 5, 231, 41))
        # self.chat_bot.setStyleSheet("background: rgb(255, 255, 255);\n"
        #                             "border-radius: 10px;\n"
        #                             "padding-left: 10px")
        # self.chat_bot.setObjectName("chat_bot")
        # self.label_7 = QtWidgets.QLabel(self)
        # self.label_7.setGeometry(QtCore.QRect(10, 10, 31, 31))
        # self.label_7.setText("")
        # self.label_7.setPixmap(QtGui.QPixmap("icon/bot.png"))
        # self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        # self.label_7.setObjectName("label_7")


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    listWidget = QtWidgets.QListWidget()
    item = QtWidgets.QListWidgetItem(listWidget)
    item_widget = CustomWidget("user")
    listWidget.addItem(item)
    listWidget.setItemWidget(item, item_widget)
    item.setSizeHint(item_widget.sizeHint())
    listWidget.show()
    sys.exit(app.exec_())
