#Module that contains common arcpy validation and geoprocessing functions
import arcpy

#License/Product Check Only necessary when running outside of an ArcMap script tool    
def checkArcGISProduct():
    boolProductLicensAvail = False
    try:
        #Check for license availability before attempting anything else
        #Project tool available on ArcGIS Desktop Basic
        strProductCheckReturn1 = arcpy.CheckProduct("arcview")
        strProductCheckReturn2 = arcpy.CheckProduct("arceditor")
        strProductCheckReturn3 = arcpy.CheckProduct("arcinfo")      
        if ( (strProductCheckReturn1 == "Available") or (strProductCheckReturn2 == "Available") or (strProductCheckReturn3 == "Available")):
            boolProductLicensAvail = True
            #print "License Available"
            arcpy.AddMessage("License Available")
    except Exception as e:
        #print "Exception caught checking license availability"
        arcpy.AddError("Exception caught checking license availability")

    return boolProductLicensAvail


#SpatialExtension license available
def checkSpatialExtension():
    boolProductLicensAvail = False
    try:
        #Check for license availability and check out upon availablity
        strSpatialExtensionCheck = arcpy.CheckExtension("spatial")
        #print "SpatialExtensionCheck: " + strSpatialExtensionCheck
        if (strSpatialExtensionCheck == "Available"):
            boolLicenseAvail = True     
            #print "Available"
            arcpy.AddMessage("Available")
        elif (strSpatialExtensionCheck == "Unavailable"):
            #print "Spatial Extension License is not available"
            arcpy.AddError("Spatial Extension License is not available")
        elif (strSpatialExtensionCheck == "NotLicensed"):
            #print "Spatial Extension License not licensed"
            arcpy.AddError("Spatial Extension License not licensed")
        elif (strSpatialExtensionCheck == "Failed"):
            #print "Spatial Extension Check Failed"
            arcpy.AddError("Spatial Extension Check Failed")
        else:
            #print "Spatial Extension Check Returned something unexpected.  This should NEVER happen"
            arcpy.AddError("Spatial Extension Check Returned something unexpected.  This should NEVER happen")
    except:
        #print "Exception caught checking out license"
        arcpy.AddError("Exception caught checking out license")

    return boolProductLicensAvail

#Check that workspace/folder exists
def workspaceExists(targetFolder):
    import os
    boolTargetFolderExists = False
    try:
        boolTargetFolderExists  = os.path.exists(targetFolder)
        #print "Target Folder {0} Exists = {1} ".format(targetFolder, str(boolTargetFolderExists))
        arcpy.AddMessage("Target Folder {0} Exists = {1} ".format(targetFolder, str(boolTargetFolderExists)))
    except Exception as e:
        #print "Exception caught checking for target folder existence"
        arcpy.AddError("Exception caught checking for target folder existence")

    return boolTargetFolderExists


#Check that file exists
def fileExists(filename):
    import os
    boolFileExists = False
    try:
        boolFileExists  = os.path.isfile(filename)
        #print "File {0} Exists = {1} ".format(filename, str(boolFileExists))
        arcpy.AddMessage("File {0} Exists = {1} ".format(filename, str(boolFileExists)))
    except Exception as e:
        #print "Exception caught checking for file existence"
        arcpy.AddError("Exception caught checking for file existence")

    return boolFileExists


#Check that a feature class exists
def featureClassExists(featureClass):
    featureClassExists = False
    try:
        featureClassExists = arcpy.Exists(featureClass)
        #print "Input Feature Class {0} Exists = {1} ".format(featureClass, str(featureClassExists))
        arcpy.AddMessage("Input Feature Class {0} Exists = {1} ".format(featureClass, str(featureClassExists)))
    except Exception as e:
        #print "Exception caught checking for input feature class existence"
        arcpy.AddError("Exception caught checking for input feature class existence")

    return featureClassExists

#Check that a feature class table exists
def featureClassTableExists(featureClass, tableName):
    tableExists = False
    if (featureClassExists(featureClass)):
        arcpy.env.workspace = featureClass
        try:
            tableExists = arcpy.Exists(tableName)
            #print "Feature Class Table {0} Exists = {1} ".format(tableName, str(tableExists))
            arcpy.AddMessage("Feature Class Table {0} Exists = {1} ".format(tableName, str(tableExists)))
        except Exception as e:
            #print "Exception caught checking for input feature class table existence"
            arcpy.AddError("Exception caught checking for input feature class table existence")
    else:
        #print "Feature class {0} does NOT exist".format(str(featureClass))
        arcpy.AddError("Feature class {0} does NOT exist".format(str(featureClass)))
 
    return tableExists






