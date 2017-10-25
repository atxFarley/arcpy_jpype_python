#This script standardizes addresses
#using USPS Zip+4 services
#Script copies input feature class
#Creates output feature class with
#additional standardized address fields

#Import the required ArcPy and custom modules
import commonUSPSZip
import arcpy
from arcpy import env
from arcpy.da import *
import commonArcPy

#Override environment variables
#allow output to be overwritten
#for the sake of this assignment
arcpy.env.overwriteOutput = True

#Specify input parameters
#targetWorkspace = r"C:\PSUGIS\GEOG485\FinalProject\Smith_TX\Smith_TX"
targetWorkspace = arcpy.GetParameterAsText(0)
#inputFeatureClass = r"48423_fp_addr.shp"
inputFeatureClass = arcpy.GetParameterAsText(1)
#inputAddressField = "ADDR"
inputAddressField = arcpy.GetParameterAsText(2)
#inputCityField = "CITY"
inputCityField = arcpy.GetParameterAsText(3)
#inputStateField = "STATE"
inputStateField  = arcpy.GetParameterAsText(4)
#inputZipField = "ZIP"
inputZipField =  arcpy.GetParameterAsText(5)
#performUSPSZip4 = True
performUSPSZip4 = arcpy.GetParameterAsText(6)

#Specifify additional variables needed within the script
outputDataType = ""
allInputFields = {}
newFields = {}
allInputFieldsExist = False
performESRIStandardize = True
outputFeatureClassAppend = "esri"
outputFeatureClassBaseName  = ""
fullOutputFeatureClassName = ""

#Only allow USPS or ESRI address standardization, not both
if (performUSPSZip4):
    #Do a quick environment configuration verify here
    #User needs 32-bit JVM path and directory to zip4 java classes
    if (commonUSPSZip.validateJVMPath() and commonUSPSZip.validateZip4Classpath()):
        performESRIStandardize = False
        outputFeatureClassAppend = "usps"
    else:
        performUSPSZip4 = False
        performESRIStandardize = True
        outputFeatureClassAppend = "esri"
        #print "This computer is not configured to run the USPS Zip+4 standardization script"
        arcpy.AddError("This computer is not configured to run the USPS Zip+4 standardization script")

#print "Running Script to Standardize Addresses on {0} : Address Fields: {1} {2} {3} {4} - USPS Zip+4: {5}".format(inputFeatureClass, inputAddressField, inputCityField, inputStateField, inputZipField,performUSPSZip4)
arcpy.AddMessage("Running Script to Standardize Addresses on {0} : Address Fields: {1} {2} {3} {4} - USPS Zip+4: {5}".format(inputFeatureClass, inputAddressField, inputCityField, inputStateField, inputZipField,performUSPSZip4))

#Perform some basic validation to verify input file and field existence before proceeding
if(commonArcPy.workspaceExists(targetWorkspace)):
    #Once workspace existence is verified, set the environment workspace
    arcpy.env.workspace = targetWorkspace
    if(commonArcPy. featureClassExists(inputFeatureClass)):
        #Make sure there are actually records in the input feature class
        countResult =  int(arcpy.GetCount_management(inputFeatureClass).getOutput(0))
        if (countResult > 0):
            #print "Input Feature Class contains {0} records".format(str(countResult)))
            arcpy.AddMessage("Input Feature Class contains {0} records.".format(str(countResult)))
            #Verify input fields exist & specify new fields for output feature class
            try:
                inputFields = arcpy.ListFields(inputFeatureClass)
                for inputField in inputFields:
                    #print "Input feature class field name {0}".format(inputField.name)
                    arcpy.AddMessage("Input feature class field name {0}".format(inputField.name))
                    allInputFields[inputField.name] = inputField
                if (inputAddressField in allInputFields and inputCityField in allInputFields and inputStateField in allInputFields and inputZipField in allInputFields):
                    allInputFieldsExist = True
            except Exception as e:
                #print "Exception caught in field validation {0}".format(e.args[0])
                arcpy.AddError("Exception caught in field validation {0}".format(e.args[0]))
                allInputFieldsExist = False
        else:
            #print "The input feature class does not contain any records. Exiting script."
            arcpy.AddError("The input feature class does not contain any records. Exiting script.")

  

#Proceed after all validation passes, otherwise exit program
if (allInputFieldsExist):
    #print "Validation complete, proceeding with output feature class creation and address standardization"
    arcpy.AddMessage("Validation complete, proceeding with output feature class creation and address standardization")

    #Determine output feature class name, data type
    #Get the Describe object of the Input Feature Class
    #Properties from describe object needed for later use
    descInputFeature = arcpy.Describe(inputFeatureClass)
    outputDataType =  descInputFeature.dataType
    outputFeatureClassBaseName = descInputFeature.baseName
    #print "Output Feature Class Data Type {0}".format(outputDataType)
    arcpy.AddMessage("Output Feature Class Data Type {0}".format(outputDataType))
    #print "Output Feature Class Base Name {0}".format(outputFeatureClassBaseName)
    arcpy.AddMessage( "Output Feature Class Base Name {0}".format(outputFeatureClassBaseName))

           
    #Determine new address field names, types, lengths
    newFields[(outputFeatureClassAppend+"_"+inputAddressField).upper()] = allInputFields[inputAddressField]
    newFields[(outputFeatureClassAppend+"_"+inputCityField).upper()] = allInputFields[inputCityField]
    newFields[(outputFeatureClassAppend+"_"+inputStateField).upper()] = allInputFields[inputStateField]
    newFields[(outputFeatureClassAppend+"_"+inputZipField).upper()] = allInputFields[inputZipField]
    plusField = allInputFields[inputZipField]
    #plusField.length = 4
    newFields[(outputFeatureClassAppend+"_PLUS").upper()] = plusField

    #print "New Fields: {0}".format(newFields)
    arcpy.AddMessage("New Fields: {0}".format(newFields))

    fullOutputFeatureClassName = outputFeatureClassBaseName + "_" + outputFeatureClassAppend
    #print "Output Feature Class Full Name {0}".format(fullOutputFeatureClassName)
    arcpy.AddMessage("Output Feature Class Full Name {0}".format(fullOutputFeatureClassName))
        
    if (performUSPSZip4):
        #print "Performing USPS Zip+4 address standardization"
        arcpy.AddMessage("Performing USPS Zip+4 address standardization")

        #Copy the input feature class
        try:

            #Copy input feature class to new output feature class
            arcpy.CopyFeatures_management(inputFeatureClass, fullOutputFeatureClassName)

            #print "Input Feature Class {0} successfully copied to {1}".format(inputFeatureClass, fullOutputFeatureClassName)
            arcpy.AddMessage("Input Feature Class {0} successfully copied to {1}".format(inputFeatureClass, fullOutputFeatureClassName))


            #AddField needs to know full path with extension
            #So, set full feature class name based on data type
            if("ShapeFile" == outputDataType):
                fullOutputFeatureClassName  +=".shp"

            #Add new fields to output feature class
            for newFieldName in newFields:
                field = newFields[newFieldName]
                fieldLen = field.length
                if (newFieldName.find("PLUS") > 0):
                    fieldLen=4
                #print "Output feature class field name: {0}, field length: {1}, data type: {2}, nullable: {3}".format(newFieldName, str(fieldLen), str(field.type), str(field.isNullable)) 
                arcpy.AddMessage("Output feature class field name: {0}, field length: {1}, data type: {2}, nullable: {3}".format(newFieldName, str(fieldLen), str(field.type), str(field.isNullable)))        
                arcpy.AddField_management(fullOutputFeatureClassName, newFieldName,field.type ,field_length=fieldLen, field_is_nullable=field.isNullable)

        except Exception as e:
            #print "Exception caught in feature copy {0}".format(e.args[0])
            arcpy.AddError("Exception caught in feature copy {0}".format(e.args[0]))

        #Standardizde addresses
        addressSearchWhereClause = '"' + str(inputAddressField) + '" IS NOT NULL'
        cursorFields = [inputAddressField,inputCityField,inputStateField,inputZipField]
        #Need to make sure new fields get added to the cursor fields list
        #in a specific order, cannot guarantee that with just getting
        #the dictionary keys
        newFieldPositions = {}
        for key in newFields:
            if key.find(inputAddressField) > 0:
                newFieldPositions["4"] = key
            if key.find(inputCityField) > 0:
                newFieldPositions["5"] = key
            if key.find(inputStateField) > 0:
                newFieldPositions["6"] = key
            if key.find(inputZipField) > 0:
                newFieldPositions["7"] = key
            if key.find("PLUS") > 0:
                newFieldPositions["8"] = key
            
        for x in range(4, 9):    
            cursorFields.append(newFieldPositions[str(x)])
            #print "CursorFields: {0}".format(cursorFields)
            
        try:
            #Launch jvm here
            commonUSPSZip.launchJVM()
            #print "JVM launched successfully"
            arcpy.AddMessage("JVM launched successfully")    

            try:
                cursorCount = 0;
                with arcpy.da.UpdateCursor(fullOutputFeatureClassName, cursorFields,  where_clause=addressSearchWhereClause) as cursor:
                    for row in cursor:
                        cursorCount +=1
                        inputAddressObj = commonUSPSZip.USPSAddress(row[0], row[1], row[2], row[3])
                        #print "Input address object {0}, {1}, {2} {3}".format(inputAddressObj.inputAddress, inputAddressObj.inputCity, inputAddressObj.inputState, inputAddressObj.inputZip)
                        uspsAddressObj = commonUSPSZip.uspszip4(inputAddressObj)
                        #print "USPS address object: Input Address: {0}, {1}, {2} {3}, USPS Address: {4} , {5}, {6} {7}-{8}".format(uspsAddressObj.inputAddress, uspsAddressObj.inputCity, uspsAddressObj.inputState, uspsAddressObj.inputZip, uspsAddressObj.uspsAddress, uspsAddressObj.uspsCity, uspsAddressObj.uspsState, uspsAddressObj.uspsZip, uspsAddressObj.uspsPlus)
                        arcpy.AddMessage("{0} USPS address object: Input Address: {1}, {2}, {3} {4}, USPS Address: {5}, {6}, {7} {8}-{9}".format(str(cursorCount), uspsAddressObj.inputAddress, uspsAddressObj.inputCity, uspsAddressObj.inputState, uspsAddressObj.inputZip, uspsAddressObj.uspsAddress, uspsAddressObj.uspsCity, uspsAddressObj.uspsState, uspsAddressObj.uspsZip, uspsAddressObj.uspsPlus))
                        row[4] = uspsAddressObj.uspsAddress
                        row[5] = uspsAddressObj.uspsCity
                        row[6] = uspsAddressObj.uspsState
                        row[7] = uspsAddressObj.uspsZip
                        row[8] = uspsAddressObj.uspsPlus
                        #Update output feature class
                        cursor.updateRow(row)
            except arcpy.ExecuteError:
                print arcpy.GetMessages(2)
            except Exception as e:
                #print "Exception caught in UpdateCursor {0}".format(e.args[0])
                arcpy.AddError("Exception caught in UpdateCursor {0}".format(e.args[0]))
                                   
            #shutdown jvm here
            commonUSPSZip.shutdownJava()
            #print "JVM shut down successfully"
            arcpy.AddMessage("JVM shut down successfully")
            #print "{0} Rows updated.".format(str(cursorCount))
            arcpy.AddMessage("{0} Rows updated.".format(str(cursorCount)))   
        except Exception as e:
                #print "Exception caught in calling USPS Zip4 service {0}".format(e.args[0]))
                arcpy.AddError("Exception caught in calling USPS Zip4 service {0}".format(e.args[0]))


        #Run some statistics
        try:
            inputSummary= "inputSummaryStats.dbf"
            inputSummaryStatsFields = [[inputAddressField, "COUNT"]]
            inputSummaryCaseField = inputAddressField
            arcpy.Statistics_analysis(inputFeatureClass, inputSummary, inputSummaryStatsFields, inputSummaryCaseField)

            outputSummary= "outputSummaryStats.dbf"
            outputSummaryStatsFields = [[newFieldPositions["4"], "COUNT"]]
            outputSummaryCaseField = newFieldPositions["4"]
            arcpy.Statistics_analysis(fullOutputFeatureClassName, outputSummary, outputSummaryStatsFields, outputSummaryCaseField)
        except Exception as e:
            #print "Exception caught generating statistics {0}".format(e.args[0])
            arcpy.AddError("Exception caught generating statistics {0}".format(e.args[0]))


    else:
        #print "Using ArcGIS geoprocessing tool that standardizes the address information in a table or feature class"
        arcpy.AddMessage("Using ArcGIS geoprocessing tool that standardizes the address information in a table or feature class")

        locatorStyle = "US Address - Dual Ranges"
        standardizedFields = "HouseNum;PreDir;PreType;StreetName;SufType;SufDir"
        arcpy.StandardizeAddresses_geocoding(inputFeatureClass, inputAddressField, locatorStyle, standardizedFields, fullOutputFeatureClassName, "Static")

    #print "Script complete.  {0} created successfully".format(fullOutputFeatureClassName)
    arcpy.AddMessage("Script complete.  {0} created successfully".format(fullOutputFeatureClassName))

else:
    #print "Input feature class and input address fields did not pass validation.  Please correct input parameters and try again."
    arcpy.AddError("Input feature class and input address fields did not pass validation.  Please correct input parameters and try again.")


