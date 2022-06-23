# -*- coding: utf-8 -*-

import os
import sys
import xml.etree.ElementTree as ET
import arcpy
from arcpy import metadata as md


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [CreateMetadata]


class CreateMetadata(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Create Metadata"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        param0 = arcpy.Parameter(
            displayName ='Input XML Template',
            name ='in_features',
            datatype ="GPType",
            parameterType ='Required',
            direction ='Input')

        param1 = arcpy.Parameter(
            displayName='Statistics Field(s)',
            name='stat_fields',
            datatype='GPValueTable',
            parameterType='Optional',
            direction='Input')

        param1.parameterDependencies = [param0.name]
        param1.columns = [['Field', 'Field'], ['GPString', 'Statistic Type']]
        param1.filters[1].type = 'ValueList'
        param1.values = [['NAME', 'SUM']]
        param1.filters[1].list = ['SUM', 'MIN', 'MAX', 'STDEV', 'MEAN']

        params = [param0, param1]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):

        with open(parameters[0].valueAsText, 'rt', encoding='utf8') as f:
            parser = ET.XMLParser()
            tree = ET.parse(f, parser=parser)
            root = tree.getroot()
            arcpy.AddMessage(root.tag)

            prefix_map = {'gmd': 'http://www.isotc211.org/2005/gmd', 'gmx': 'http://www.isotc211.org/2005/gmx',
                          'gco': 'http://www.isotc211.org/2005/gco', 'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                          'gml': 'http://www.opengis.net/gml/3.2', 'xlink': 'http://www.w3.org/1999/xlink'}

            purposeEls = root.findall(".//gmd:electronicMailAddress/gco:CharacterString", prefix_map)
            for element in purposeEls:
                if element.text is not None:
                    arcpy.AddMessage(element.text)
        return

