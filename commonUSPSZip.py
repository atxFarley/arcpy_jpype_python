from jpype import *

jvmPath=r"C:\Java\32bit\jdk1.8.1_21\jre\bin\server\jvm.dll"
zip4Classpath="C:\\Python27\\ArcGIS10.4\\amyScripts\\classes"
zip4ClasspathArg="-Djava.class.path="+zip4Classpath

def validateJVMPath():
    import os
    jvmPathExists = False
    try:
        jvmPathExists  = os.path.exists(jvmPath)
        print "JVM Path{0} Exists = {1} ".format(jvmPath, str(jvmPathExists))
    except Exception as e:
        print "Exception caught checking for jvm path existence"

    return jvmPathExists

def validateZip4Classpath():
    import os
    zip4ClasspathExists = False
    try:
        zip4ClasspathExists = os.path.exists(zip4Classpath)
        print "Zip4 Class Path{0} Exists = {1} ".format(zip4Classpath, str(zip4ClasspathExists))
    except Exception as e:
        print "Exception caught checking for zip4 class path existence"

    return zip4ClasspathExists

def launchJVM():
    try: 
        #startJVM(r"C:\Java\32bit\jdk1.8.1_21\jre\bin\server\jvm.dll", "-Xms256m", "-Xmx512m", "-ea", "-Djava.class.path=C:\\Python27\\ArcGIS10.4\\amyScripts\\classes")
        startJVM(jvmPath, "-Xdiag", "-Xshare:off	", "-Xms256m", "-Xmx512m", "-ea", zip4ClasspathArg)
        #java.lang.System.out.println("hello world");
        print "JVM launched"
    except Exception as e:
        print "Exception caught launching JVM {0}".format(e.args[0])

def shutdownJava():
    try: 
        shutdownJVM()
    except Exception as e:
        print "Exception caught"

def uspszip4(uspsAddressObj):
    try: 
        z = java.rmi.Naming.lookup("rmi://bzip4.flooddata.com:12346/zip4");
        print z, z.__class__
        iAddress = uspsAddressObj.inputAddress
        iCity = uspsAddressObj.inputCity;
        iState = uspsAddressObj.inputState
        iZip= uspsAddressObj.inputZip
        z4Model = ""
        z4Model = z.addressInquiry(iAddress, iCity, iState, iZip);
        if (not z4Model.multAdrResult):
            uspsAddressObj.setUSPSFields(z4Model.dadl1,z4Model.dctya, z4Model.dstaa,z4Model.zipc,z4Model.addon )

        #Testing/Debugging lines
        #uspsAddressObj.setUSPSFields(iAddress, iCity, iState, iZip, "0000")
        #java.lang.System.out.println("\tInput Address: " + z4Model.iadl1 + " (street), " + z4Model.ictyi + " (city), " + z4Model.istai + " (state), " + z4Model.izipc + " (zipcode)");
        #java.lang.System.out.println("\tOutput Address: " + z4Model.dadl1 + " (street), " + z4Model.dctya + " (city), " + z4Model.dstaa + " (state), " + z4Model.zipc + " (zipcode), " + z4Model.addon + " (addon), " + z4Model.ppnum + " (ppnum), " + z4Model.str_name + " (streetname), " + z4Model.psnum + " (psnum), " + z4Model.punit+ " (punit), " + z4Model.rec_type + " (rec_type), " + z4Model.county + " (countcode)");        
        #java.lang.System.out.println("\tParsed Address: " + z4Model.pre_dir + " (pre_dir), " + z4Model.str_name + " (streetname), " + z4Model.suffix + " (suffix), " + z4Model.post_dir + " (post_dir)");
        #java.lang.System.out.println("\tParsed Address2: " + z4Model.ppnum + " (ppnum) " + z4Model.ppre1 + " (ppre1), " + z4Model.ppre2 + " (ppre2), " + z4Model.ppnam + " (ppnam), " + z4Model.psuf2 + " (psuf2), " + z4Model.ppst1 + " (ppst1), " + z4Model.ppst2 + " (ppst2)");
    except Exception as e:
        print "Exception caught calling out to the USPS Zip+4 Java Server {0}".format(e.args[0])

    return uspsAddressObj



class USPSAddress:

    def __init__(self, iAddress, iCity, iState, iZip):
        self.inputAddress = iAddress
        self.inputCity = iCity
        self.inputState = iState
        self.inputZip = iZip
        self.uspsAddress = ""
        self.uspsCity = ""
        self.uspsState = ""
        self.uspsZip=""
        self.uspsPlus = ""

    def setUSPSFields(self, sAddress, sCity, sState, sZip, sPlus):
        self.uspsAddress = sAddress
        self.uspsCity = sCity
        self.uspsState = sState
        self.uspsZip=sZip
        self.uspsPlus = sPlus