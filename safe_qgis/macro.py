"""
InaSAFE Disaster risk assessment tool developed by AusAid -
  **Helper module for gui script functions.**

Contact : ole.moller.nielsen@gmail.com

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
__author__ = 'bungcip@gmail.com'
__version__ = '0.5.1'
__revision__ = '$Format:%H$'
__date__ = '10/01/2011'
__copyright__ = 'Copyright 2012, Australia Indonesia Facility for '
__copyright__ += 'Disaster Reduction'

import os
from safe.common.utilities import ugettext as tr
from safe_qgis.dock import Dock
from qgis.utils import iface


def findInaSAFEDock():
    """ Get InaSAFE Dock widget instance.
    Returns: Dock - instance of InaSAFE Dock in QGIS main window.
    """
    return iface.mainWindow().findChild(Dock, 'InaSAFEDock')


def setupScenario(theHazard, theExposure, theFunction,
                  theAggregation=None):
    """Simulate user activities when setting combo box state in InaSAFE Dock widget.

    Args:
        theHazard str - (Required) name of the hazard combo entry to set.
        theExposure str - (Required) name of exposure combo entry to set.
        theFunction str - (Required) name of the function combo entry to set.
        theAggregation str - (Optional) which layer should be used for
        aggregation.

    Returns: None.

    Raises: Exception - occurs when this function failed to set the state of combo box.
    """

    def setComboBox(theWidget, theText, theFailMessage):
        myIndex = theWidget.findText(theText)
        if myIndex == -1:
            raise Exception(theFailMessage)
        theWidget.setCurrentIndex(myIndex)

    myDock = findInaSAFEDock()
    myDock.show()

    if theHazard is not None:
        myMessage = tr('Hazard Layer Not Found: %s' % theHazard)
        setComboBox(myDock.cboHazard, theHazard, myMessage)

    if theExposure is not None:
        myMessage = tr('Exposure Layer Not Found: %s' % theExposure)
        setComboBox(myDock.cboExposure, theExposure, myMessage)

    if theFunction is not None:
        myMessage = tr('Impact Function Not Found: %s' % theFunction)
        setComboBox(myDock.cboFunction, theFunction, myMessage)

    if theAggregation is not None:
        if myDock.cboAggregation.isEnabled() is False:
            raise Exception('The aggregation combobox should be enabled')

        myMessage = tr('Aggregation layer Not Found: %s' % theAggregation)
        setComboBox(myDock.cboAggregation, theAggregation, myMessage)


def runScenario():
    """Simulate pressing run button in InaSAFE dock widget.

    """

    #FIXME: (Gigih) need to check if scenario failed or not.
    theDock = findInaSAFEDock()
    theDock.pbnRunStop.click()



def addLayers(theDirectory, thePaths):

    def extractPath(thePath):
        myFilename = os.path.split(thePath)[-1]  # In case path was absolute
        myBaseName, myExt = os.path.splitext(myFilename)
        myPath = os.path.join(theDirectory, thePath)
        return myPath, myBaseName

    myPaths = []
    if isinstance(thePaths, str):
        myPaths.append(extractPath(thePaths))
    elif isinstance(thePaths, list):
        myPaths = [extractPath(x) for x in thePaths]
    else:
        myMessage = "thePaths must be string or list not %s" % type(thePaths)
        raise Exception(myMessage)

    for myPath, myBaseName in myPaths:
        myExt = os.path.splitext(myPath)[-1]

        if myExt in ['.asc', '.tif']:
            iface.addRasterLayer(myPath, myBaseName)
        elif myExt in ['.shp'] :
            iface.addVectorLayer(myPath, myBaseName, 'ogr')
        else:
            raise Exception('File %s had illegal extension' % myPath)


def assertEquals(theValue, theExpected, theMessage=None):
    #FIXME: (gigih) change assert to something else
    assert theValue == theExpected, theMessage

def assertTrue(theValue, theMessage=None):
    #FIXME: (gigih) change assert to something else
    assert theValue is True, theMessage
