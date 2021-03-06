# -*- coding: utf-8 -*-
#
# amsn - a python client for the WLM Network
#
# Copyright (C) 2008 Dario Freddi <drf54321@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from amsn2.ui import base

from PyQt4 import Qt
from PyQt4 import QtCore
from PyQt4 import QtGui

from fadingwidget import FadingWidget
from amsn2.views import MenuView, MenuItemView

import common

class aMSNMainWindow(QtGui.QMainWindow, base.aMSNMainWindow):
    def __init__(self, amsn_core, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self._amsn_core = amsn_core
        self.centralWidget = QtGui.QWidget(self)
        self.stackedLayout = QtGui.QStackedLayout()
        #self.stackedLayout.setStackingMode(QStackedLayout.StackAll)
        self.centralWidget.setLayout(self.stackedLayout)
        self.setCentralWidget(self.centralWidget)
        self.opaqLayer = FadingWidget(QtCore.Qt.white, self)
        self.stackedLayout.addWidget(self.opaqLayer)
        QtCore.QObject.connect(self.opaqLayer, QtCore.SIGNAL("fadeInCompleted()"), self.__activateNewWidget)
        QtCore.QObject.connect(self.opaqLayer, QtCore.SIGNAL("fadeOutCompleted()"), self.__fadeIn)
        self.resize(230, 550)

    def closeEvent(self, event):
        self._amsn_core.quit()

    def fadeIn(self, widget):
        widget.setAutoFillBackground(True)
        self.stackedLayout.addWidget(widget)
        self.stackedLayout.setCurrentWidget(self.opaqLayer)
        # Is there another widget in here?
        if self.stackedLayout.count() > 2:
            self.opaqLayer.fadeOut() # Fade out current active widget
        else:
            self.__fadeIn()

    def __fadeIn(self):
        # Delete old widget(s)
        while self.stackedLayout.count() > 2:
            widget = self.stackedLayout.widget(1)
            self.stackedLayout.removeWidget(widget)
            widget.deleteLater()
        self.opaqLayer.fadeIn()

    def __activateNewWidget(self):
        self.stackedLayout.setCurrentIndex(self.stackedLayout.count()-1)

    def __on_show(self):
        self._amsn_core.main_window_shown()

    def show(self):
        self.setVisible(True)
        self._amsn_core.idler_add(self.__on_show)

    def hide(self):
        self.setVisible(False)

    def set_title(self, title):
        self.setWindowTitle(title)

    def set_view(self, view):
        print "set_view request"

    def set_menu(self, menu):
        mb = QtGui.QMenuBar()

        common.create_menu_items_from_view(mb, menu.items)

        self.setMenuBar(mb)
