"""
/***************************************************************************
 Navtable
                                 A QGIS plugin
 Navtable
                              -------------------
        begin                : 2019-02-20
        copyright            : (C) 2013 by Francisco P. Sampayo
        email                : fpsampayo@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt
from qgis.core import QgsApplication
from NavTable.gui.NTSelectByFormDialog import NTSelectByFormDialog

pluginPath = os.path.split(os.path.dirname(__file__))[0]
WIDGET, BASE = uic.loadUiType(
    os.path.join(pluginPath, 'ui', 'expressionBuilderDialog.ui'))


class NTExpressionBuilder(BASE, WIDGET):

    def __init__(self, layer, expression, iface):
        super().__init__(None)
        self.setupUi(self)

        self.layer = layer
        self.iface = iface

        self.setWindowTitle(self.tr('Filter NavTable Features by Expression'))
        self.expressionBuilder = self.mExpressionBuilderWidget
        self.expressionBuilder.setLayer(layer)
        self.expressionBuilder.loadFieldNames()
        self.expressionBuilder.loadRecent()

        self.btnFilterForm.setText(self.tr('Add Expression by Form'))
        self.btnFilterForm.setIcon(QgsApplication.getThemeIcon('mIconFormSelect.svg'))
        self.btnFilterForm.clicked.connect(self.formExpression)

        self.initialExpression = expression
        self.expressionBuilder.setExpressionText(expression)

    def formExpression(self):

        dialog = NTSelectByFormDialog(self.layer, self.iface)

        if dialog.exec_():
            self.expressionBuilder.setExpressionText(dialog.expression)


    def accept(self):

        if self.initialExpression == self.expressionBuilder.expressionText():
            self.reject()
            return

        if self.expressionBuilder.isExpressionValid() or \
                self.expressionBuilder.expressionText() == '':
            self.expressionBuilder.saveToRecent()
            super().accept()
