import jarray
import inspect
import os
import csv
import json
import urllib2
import shutil
import struct
import binascii
import codecs
import sys
import os.path
from datetime import datetime
from java.io import FileInputStream
from java.io import IOException
from java.lang import Exception
from org.apache.poi.xssf.usermodel import XSSFWorkbook
from org.apache.poi.hssf.usermodel import HSSFCell
from org.apache.poi.hssf.usermodel import HSSFRow
from org.apache.poi.hssf.usermodel import HSSFSheet
from org.apache.poi.hssf.usermodel import HSSFWorkbook
from subprocess import Popen, PIPE
from javax.swing import JCheckBox
from java.awt import GridLayout
from java.awt import GridBagLayout
from java.awt import GridBagConstraints
from javax.swing import JPanel
from javax.swing import JFileChooser
from javax.swing import JScrollPane
from javax.swing.filechooser import FileNameExtensionFilter
from java.sql  import DriverManager, SQLException
from org.sleuthkit.datamodel import SleuthkitCase
from org.sleuthkit.datamodel import AbstractFile
from org.sleuthkit.datamodel import ReadContentInputStream
from org.sleuthkit.datamodel import BlackboardArtifact
from org.sleuthkit.datamodel import BlackboardAttribute
from org.sleuthkit.autopsy.ingest import IngestModule
from org.sleuthkit.autopsy.ingest.IngestModule import IngestModuleException
from org.sleuthkit.autopsy.ingest import DataSourceIngestModule
from org.sleuthkit.autopsy.ingest import IngestModuleFactoryAdapter
from org.sleuthkit.autopsy.ingest import GenericIngestModuleJobSettings
from org.sleuthkit.autopsy.ingest import IngestModuleIngestJobSettingsPanel
from org.sleuthkit.autopsy.ingest import IngestMessage
from org.sleuthkit.autopsy.ingest import IngestServices
from org.sleuthkit.autopsy.ingest import ModuleDataEvent
from org.sleuthkit.autopsy.coreutils import Logger
from org.sleuthkit.autopsy.coreutils import PlatformUtil
from org.sleuthkit.autopsy.casemodule import Case
from org.sleuthkit.autopsy.casemodule.services import Services
from org.sleuthkit.autopsy.casemodule.services import FileManager
from org.sleuthkit.autopsy.datamodel import ContentUtils
from com.williballenthin.rejistry import RegistryHiveFile
from com.williballenthin.rejistry import RegistryKey
from com.williballenthin.rejistry import RegistryParseException
from com.williballenthin.rejistry import RegistryValue
from java.lang import Class
from java.lang import System
from java.util.logging import Level
from java.io import File
from org.sleuthkit.datamodel import TskData


class AGPIngestModuleFactory(IngestModuleFactoryAdapter):

    def __init__(self):
        self.settings = None

    moduleName = "Artifact Genome Project"
    
    def getModuleDisplayName(self):
        return self.moduleName
    
    def getModuleDescription(self):
        return "Artifact Genome Project"
    
    def getModuleVersionNumber(self):
        return "1.0"
    
    def getDefaultIngestJobSettings(self):
        return GenericIngestModuleJobSettings()

    def hasIngestJobSettingsPanel(self):
        return True

    # TODO: Update class names to ones that you create below
    def getIngestJobSettingsPanel(self, settings):
        if not isinstance(settings, GenericIngestModuleJobSettings):
            raise IllegalArgumentException("Expected settings argument to be instanceof GenericIngestModuleJobSettings")
        self.settings = settings
        return AGPWithUISettingsPanel(self.settings)

    def isDataSourceIngestModuleFactory(self):
        return True

    def createDataSourceIngestModule(self, ingestOptions):
        return AGPIngestModule(self.settings)

# Data Source-level ingest module.  One gets created per data source.
class AGPIngestModule(DataSourceIngestModule):

    _logger = Logger.getLogger(AGPIngestModuleFactory.moduleName)

    def log(self, level, msg):
        self._logger.logp(level, self.__class__.__name__, inspect.stack()[1][3], msg)

    def __init__(self, settings):
        self.context = None
        self.local_settings = settings
        self.List_Of_Windows_Internals = []
        self.List_Of_tables = []

    def startUp(self, context):
        self.context = context

        if self.local_settings.getSetting('CSV_Flag') == 'true':
            if PlatformUtil.isWindowsOS():
                self.log(Level.INFO, "XLS ==> " + str(self.local_settings.getSetting('CSV_Flag')))
                self.path_to_Webcache_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SearchResults.xls")#test.csv
                if not os.path.exists(self.path_to_Webcache_file):
                   raise IngestModuleException("XLS  does not exist for Windows")
            elif PlatformUtil.getOSName() == 'Linux':
                self.log(Level.INFO, "XLS ==> " + str(self.local_settings.getSetting('CSV_Flag')))
                self.path_to_Webcache_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SearchResults.xls")#test.csv
                if not os.path.exists(self.path_to_Webcache_file):
                   raise IngestModuleException("XLS  does not exist for Linux")
        if self.local_settings.getSetting('DOWNLOAD') == 'true':
            if PlatformUtil.isWindowsOS():
                self.log(Level.INFO, "XLS ==> " + str(self.local_settings.getSetting('DOWNLOAD')))
                self.path_to_Webcache_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SearchResults.xls")#test.csv
                if not os.path.exists(self.path_to_Webcache_file):
                   raise IngestModuleException("XLS  does not exist for Windows")
            elif PlatformUtil.getOSName() == 'Linux':
                self.log(Level.INFO, "XLS ==> " + str(self.local_settings.getSetting('DOWNLOAD')))
                self.path_to_Webcache_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SearchResults.xls")#test.csv
                if not os.path.exists(self.path_to_Webcache_file):
                   raise IngestModuleException("XLS  does not exist for Linux")

        pass


    def process(self, dataSource, progressBar):

        self.log(Level.INFO, "Starting to process")
        progressBar.switchToIndeterminate()
        
       
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y%H%M%S")
        self.path_to_Webcache_file10 = os.path.join(os.path.dirname(os.path.abspath(__file__)), ( "report" + dt_string + ".html"))
        sys.stdout = open(self.path_to_Webcache_file10,'w')
        print "<html>"
        mes1000 = "<head><style>input { display: none; } input + label { display: inline-block } input ~ .tab { display: none } #tab1:checked ~ .tab.content1, #tab2:checked ~ .tab.content2 { display: block; } input + label {border: 1px solid #999;background: #EEE;padding: 4px 12px;border-radius: 4px 4px 0 0;position: relative;top: 1px;} input:checked + label { background: #FFF; border-bottom: 1px solid transparent;} input ~ .tab {border-top: 1px solid #999; padding: 12px;}  table {font-family: arial, sans-serif;border-collapse: collapse; width: 100%;}td, th {border: 1px solid #dddddd;text-align: left;padding: 8px;}tr:nth-child(even) {background-color: #dddddd;}</style></head>"
        print mes1000
        
        #mes1000 ="<div style=\"display: block;margin-left: auto;margin-right: auto;width: 40%;\"><a href=\"#dashboard\" data-transition=\"slide\" data-direction=\"reverse\"><img alt=\"\" title=\"\" src=\"https://agpnewhaven.com/static/img/agp_logo.png\"  /></a></div>"
        #print mes1000
        self.artifact_type = "Registry"
      
        
        print "<input type=\"radio\" name=\"tabs\" id=\"tab1\" checked /><label for=\"tab1\">Registry</label><input type=\"radio\" name=\"tabs\" id=\"tab2\" /><label for=\"tab2\">File</label>"
        print "<div class=\"tab content1\">"
        if self.local_settings.getSetting('DOWNLOAD') == 'true':
                self.process_Registry(dataSource, progressBar)
        print "</div>"
        self.artifact_type = "File"
       
        print "<div class=\"tab content2\">"
        #print "<tr><th>Artifact Type</th><th>Artifact name</th><th>FILE NAME</th><th>FILE PATH</th></tr>"
        if self.local_settings.getSetting('CSV_Flag') == 'true':
            progressBar.progress("Processing XLS")	
            self.process_File(dataSource, progressBar)
            message = IngestMessage.createMessage(IngestMessage.MessageType.DATA,
                "AGP", " AGP File artifacts Has Been Analyzed " )
            IngestServices.getInstance().postMessage(message)
        print "</div>"
        
  
        # After all databases, post a message to the ingest messages in box.
        message = IngestMessage.createMessage(IngestMessage.MessageType.DATA,
            "AGP", " AGP artifacts Has Been Analyzed " )
        IngestServices.getInstance().postMessage(message)
       
        print "</html>" 
        return IngestModule.ProcessResult.OK                

    def process_File(self, dataSource, progressBar): 
        progressBar.switchToIndeterminate()
        skCase = Case.getCurrentCase().getSleuthkitCase()
        blackboard = Case.getCurrentCase().getServices().getBlackboard()
        fileManager = Case.getCurrentCase().getServices().getFileManager()
        files = fileManager.findFiles(dataSource, "%", "/")
        if PlatformUtil.isWindowsOS():
            self.log(Level.INFO, "XLS ==> " + str(self.local_settings.getSetting('CSV_Flag')))
            self.path_to_Webcache_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SearchResults.xls")
            if not os.path.exists(self.path_to_Webcache_file):
                 raise IngestModuleException("XLS Executable does not exist for Windows")
        elif PlatformUtil.getOSName() == 'Linux':
            self.log(Level.INFO, "XLS ==> " + str(self.local_settings.getSetting('CSV_Flag')))
            self.path_to_Webcache_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SearchResults.xls")
            if not os.path.exists(self.path_to_Webcache_file):
                raise IngestModuleException("XLS Executable does not exist for Linux")
           
        #print "<br><br><br><br><h1>FILE ARTIFACTS</h1><br><br><br><br>"     
 
        #print "<table>"
        #print "<tr><th>Artifact Found</th><th>FILE NAME</th><th>FILE PATH</th></tr>"
        
        mes1000 ="<div style=\"display: block;margin-left: auto;margin-right: auto;width: 40%;\"><a href=\"#dashboard\" data-transition=\"slide\" data-direction=\"reverse\"><img alt=\"\" title=\"\" src=\"https://agpnewhaven.com/static/img/agp_logo.png\"  /></a></div>"
        print mes1000
        print "<table>"
        print "<tr><th>Artifact Type</th><th>Artifact name</th><th>FILE NAME</th><th>FILE PATH</th><th>Path on Disk</th></tr>"
        if True:
            if True:
                try:
                    
                    inp = FileInputStream(self.path_to_Webcache_file)
                   

                    myWorkBook = HSSFWorkbook (inp)
                    sheet = myWorkBook.getSheet("File Artifacts")
                    i1  = 1
                    
                    rowsCount = sheet.getLastRowNum()
                    while i1 <= rowsCount:
                        row = sheet.getRow(i1)
                        i1 = i1 + 1
                        cell = row.getCell(23)
                        cell1 = row.getCell(0)
                        val = cell.getStringCellValue()
                        val1 = cell1.getStringCellValue()
                        try:
                            val2 = ""
                            try:
                                cell2 = row.getCell(22)
                                val2 = cell2.getStringCellValue()
                            except:
                                 self.log(Level.INFO, "Error reading file name ")
                                 
                            filePath = json.loads(val)
                            
                            
                            if(filePath['path']  != "" ):
                                if(val2 == ""):
                                    val2 = "%"
                                    
                                
                                files = fileManager.findFiles(dataSource, val2,  "%" + filePath['path'])
                                self.log(Level.INFO, "val2  " + val2)
                                self.log(Level.INFO, " path    " + filePath['path'])
                                
                                self.log(Level.INFO, "files found " + str(len(files)))
                                self.log(Level.INFO, "-----------------------------")
                                numFiles = len(files)
                                try:
                                    if(numFiles == 0):
                                        astring = filePath['path'].replace("/", "\\")
                                        if(len(astring) > 2):
                                            files = fileManager.findFiles(dataSource, val2,  "%" + astring)
                                            numFiles = len(files)
                                except:
                                    a100 = 0
                                
                                try:
                                    if(numFiles == 0):
                                        astring = filePath['path'].replace("\\", "/")
                                        if(len(astring) > 2):
                                            files = fileManager.findFiles(dataSource, val2,  "%" + astring)
                                            numFiles = len(files)
                                except:
                                    a100 = 0                                
                                    
                                try:
                                    if(numFiles == 0):
                                        astring = filePath['path'].replace("/", "\\")
                                        astring = astring[astring[1:].find('\\')+1:]#os.path(astring.parts[1:])                                     
                                        if(len(astring) > 2):
                                            files = fileManager.findFiles(dataSource, val2,  "%" + astring)
                                            numFiles = len(files) 
                                    
                                except:
                                    a100 = 0
                                try:
                                    if(numFiles == 0):
                                        astring = filePath['path'].replace("/", "\\")
                                        astring = astring[astring[1:].find('\\')+1:]
                                        astring = astring[astring[1:].find('\\')+1:]                                       
                                        if(len(astring) > 2):
                                            files = fileManager.findFiles(dataSource, val2,  "%" + astring)
                                            numFiles = len(files) 
                                    
                                except:
                                    a100 = 0
                                   
                                   
                                    
                                
                                
                                try:
                                    if(numFiles == 0):
                                        astring = filePath['path'].replace("\\", "/")
                                        astring = astring[astring[1:].find('/')+1:]
                                        if(len(astring) > 2):
                                            files = fileManager.findFiles(dataSource, val2,  "%" + astring)
                                            numFiles = len(files) 
                                    
                                except:
                                    a100 = 0
                                try:
                                    if(numFiles == 0):
                                        astring = filePath['path'].replace("\\", "/")
                                        astring = astring[astring[1:].find('/')+1:]
                                        astring = astring[astring[1:].find('/')+1:]
                                        if(len(astring) > 2):
                                            files = fileManager.findFiles(dataSource, val2,  "%" + astring)
                                            numFiles = len(files)
                                except:
                                    a100 = 0                                
                               
                                            
                                     
                                if(numFiles < 21):
                                    if(numFiles > 0):
                                        #self.printRow(val1,val2,filePath['path'])
                                        print "<tr style=\"background-color:#ADD8E6\">"
                                        print "<td>"
                                        print val1 + " - " + filePath['path']
                                        print "<td>"
                                        print "<td></td><td></td>"
                                        print "<tr>"
                                        
                                        
                                    message2 = IngestMessage.createMessage(IngestMessage.MessageType.DATA, "Artifact Found" ,val1,val1)
                                    IngestServices.getInstance().postMessage(message2)
                                    for file in files:
                                        #message2 = IngestMessage.createMessage(IngestMessage.MessageType.DATA, filePath['path'], file.getParentPath(),file.getParentPath())
                                        #IngestServices.getInstance().postMessage(message2)
                                        art = file.newArtifact(BlackboardArtifact.ARTIFACT_TYPE.TSK_INTERESTING_FILE_HIT)
                                        att = BlackboardAttribute(BlackboardAttribute.ATTRIBUTE_TYPE.TSK_SET_NAME.getTypeID(), 
                                        AGPIngestModuleFactory.moduleName, 'AGP ' + val1)
                                        art.addAttribute(att)
                                        
                                        
                                        try:
                                            blackboard.indexArtifact(art)
                                        except Blackboard.BlackboardException as e:
                                            self.log(Level.SEVERE, "Error indexing artifact " + art.getDisplayName())

                                        mx1 = " "
                                        if self.local_settings.getSetting('EXPORT') == 'true':
                                            Temp_Dir = Case.getCurrentCase().getTempDirectory()
                                            temp_dir = os.path.join(Temp_Dir, "files extracted")
                                            
                                            temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files extracted")
                                            try:
                                                os.mkdir(temp_dir)
                                            except:
                                                self.log(Level.INFO, "files extracted Directory already exists " + temp_dir)
                                            extractedFile = os.path.join(temp_dir, str(file.getId()) + "-" + file.getName())
                                            mo = File(extractedFile)
                                            ContentUtils.writeToFile(file, mo)
                                            mx1 = "<a href=\"" + mo.getPath() + "\">" + mo.getPath() + "</a>"
                                       
                                            
                                        mx = str(file.getId()) + "-" + file.getName()
                                        
                                        print "<tr>"
                                        print "<td>"
                                        print self.artifact_type
                                        print "</td>"
                                        print "<td>"
                                        print val1
                                        print "</td>"
                                        print "<td>"
                                        print mx
                                        print "</td>"
                                        print "<td>"
                                        print mx1
                                        print "</td>"
                                        print "<td>"
                                        print file.getParentPath()
                                        print "</td>"
                                        print "</tr>"
                                        
                                        IngestServices.getInstance().fireModuleDataEvent(
                                        ModuleDataEvent(AGPIngestModuleFactory.moduleName, 
                                        BlackboardArtifact.ARTIFACT_TYPE.TSK_INTERESTING_FILE_HIT, None))
                            
                        except:
                            a = 1
                            #message2 = IngestMessage.createMessage(IngestMessage.MessageType.DATA, "not found" ,"not found","not found")
                            #IngestServices.getInstance().postMessage(message2)
                
                except IOException as ex:
                        message2 = IngestMessage.createMessage(IngestMessage.MessageType.DATA, "IOEXCEPTION", "IOEXCEPTION","IOEXCEPTION")
                        IngestServices.getInstance().postMessage(message2)        
        print "</table>"  
    def process_Registry(self, dataSource, progressBar): 
        progressBar.switchToIndeterminate()
        
        skCase = Case.getCurrentCase().getSleuthkitCase();
        fileManager = Case.getCurrentCase().getServices().getFileManager()

        # Create Recyclebin directory in temp directory, if it exists then continue on processing		
        Temp_Dir = Case.getCurrentCase().getTempDirectory()
        temp_dir = os.path.join(Temp_Dir, "registries")
        self.log(Level.INFO, "create Directory " + temp_dir)
        try:
		    os.mkdir(temp_dir)
        except:
		    self.log(Level.INFO, "registries Directory already exists " + temp_dir)



        systemAbsFile = []
        ntUserFiles = fileManager.findFiles(dataSource, "ntuser.dat")
        usrClassFiles = fileManager.findFiles(dataSource, "usrclass.dat")
        files1 = fileManager.findFiles(dataSource, "SAM","Windows/System32/Config")           
        files2 = fileManager.findFiles(dataSource, "HKEY_CURRENT_USER","Windows/System32/Config")              
        files3 = fileManager.findFiles(dataSource, "HKEY_LOCAL_MACHINE","Windows/System32/Config")    
        files4 = fileManager.findFiles(dataSource, "HKEY_USERS","Windows/System32/Config")  
        files5 = fileManager.findFiles(dataSource, "HKEY_CLASSES_ROOT","Windows/System32/Config")          
        files6 = fileManager.findFiles(dataSource, "KEY_LOCAL_MACHINE","Windows/System32/Config")      
        files7 = fileManager.findFiles(dataSource, "HKLM","Windows/System32/Config")
        files8 = fileManager.findFiles(dataSource, "SECURITY","Windows/System32/Config")
        files = ntUserFiles + usrClassFiles  + files1 + files2 + files3 + files4 + files5 + files6 + files7 + files8
        
        numFiles = len(files)
        self.log(Level.INFO, "Number of  Files found ==> " + str(numFiles))
        
    
        if PlatformUtil.isWindowsOS():
            self.log(Level.INFO, "XLS ==> " + str(self.local_settings.getSetting('DOWNLOAD')))
            self.path_to_Webcache_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SearchResults.xls")
            if not os.path.exists(self.path_to_Webcache_file):
                 raise IngestModuleException("XLS Executable does not exist for Windows")
        elif PlatformUtil.getOSName() == 'Linux':
            self.log(Level.INFO, "XLS ==> " + str(self.local_settings.getSetting('DOWNLOAD')))
            self.path_to_Webcache_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SearchResults.xls")
            if not os.path.exists(self.path_to_Webcache_file):
                raise IngestModuleException("XLS Executable does not exist for Linux")
        i = 0     

     
        #print "<br><br><br><br><h1>REGISTRY ARTIFACTS</h1><br><br><br><br>"
        
        mes1000 ="<div style=\"display: block;margin-left: auto;margin-right: auto;width: 40%;\"><a href=\"#dashboard\" data-transition=\"slide\" data-direction=\"reverse\"><img alt=\"\" title=\"\" src=\"https://agpnewhaven.com/static/img/agp_logo.png\"  /></a></div>"
        print mes1000
        print "<table>"
        print "<tr><th>Artifact Type</th><th>Key</th><th>VALUE NAME</th><th>VALUE</th></tr>"
        
        for file in files:
            if True:
                try:
                
                    i = i + 1
                    lclDbPath = os.path.join(temp_dir,  str(i) + '' + file.getName())
                    ContentUtils.writeToFile(file, File(lclDbPath))
                    inp = FileInputStream(self.path_to_Webcache_file)
                    myWorkBook = HSSFWorkbook (inp)
                    sheet = myWorkBook.getSheet("Windows Registry Artifacts")
                    i1  = 1                   
                    rowsCount = sheet.getLastRowNum()
                  
                    while i1 <= rowsCount:
                        registryKeyToFind2 = ""
                        row = sheet.getRow(i1)
                        i1 = i1 + 1
                        cell = row.getCell(17)
                        cell1 = row.getCell(0)
                        val = cell.getStringCellValue()
                        val1 = cell1.getStringCellValue()
                        if self.context.isJobCancelled():
                            return IngestModule.ProcessResult.OK
                        if True:   
                            try:
                                samRegFile = RegistryHiveFile(File(lclDbPath))
                                currentKey = self.findRegistryKey(samRegFile, val)
                                self.printRow(val, "","")
                               
                                for value in currentKey.getValueList():
                                    for st1 in value.getValue().getAsStringList():
                                        self.printRow(val, value.getName(),st1)
                                     
                                    try:
                                        mn = str(value.getValue().getAsNumber())
                                        self.printRow(val, value.getName(),mn)
                                    except:
                                        self.log(Level.INFO, "no number ")                                      
       
                              
                                
                                try:
                                    bamKey = currentKey.getSubkeyList()
                                    for sk in bamKey:
                                        if len(sk.getValueList()) > 0:
                                            registryKey = sk.getName()
                                            skValues = sk.getValueList()
                                            for skValue in skValues:
                                                if skValue.getName() == 'SequenceNumber' or skValue.getName() == 'Version':
                                                    pass
                                                else:
                                                    indRecord = []
                                                    value = skValue.getValue()
                                                    binData = self.getRawData(value.getAsRawData())
                                                    msTime = struct.unpack('<qqq', binData)[0]
                                                    linuxTime = int(str(msTime)[0:11]) - 11644473600
                                                    uId = registryKey[registryKey.rfind("-")+1:]
                                                    self.printRow(val, "uid",uId)
                                                    self.printRow(val, "skValue Name",str(skValue.getName()))
                                                    self.printRow(val, "linuxTime",str(linuxTime))
                                                    self.printRow(val, "indRecord",indRecord)
                                except:
                                    self.log(Level.INFO, "no bam key")
                                     
                                try:
                                    self.log(Level.INFO, "sam key " + val)
                                    samKey = currentKey.getSubkeyList()   
                                    self.log(Level.INFO, "sam key2")
                                    for sk in samKey:
                                        self.log(Level.INFO, "sam key3")
                                        registryKey = sk.getName()
                                        skValues = sk.getValueList()
                                        self.log(Level.INFO, "sam key4 " + str(len(skValues)))
                                        if len(skValues) > 0:
                                            for skVal in skValues:
                                                if skVal.getName() == 'V':
                                                    value = skVal.getValue()
                                                    hexArray = self.getRawData(value.getAsRawData())
                                                    pos1 = int(str(struct.unpack_from('<l', hexArray[4:])[0]))
                                                    pos3 = int(str(struct.unpack_from('<l', hexArray[12:])[0])) + 204 
                                                    pos4 = int(str(struct.unpack_from('<l', hexArray[16:])[0]))
                                                    pos6 = int(str(struct.unpack_from('<l', hexArray[24:])[0])) + 204
                                                    pos7 = int(str(struct.unpack_from('<l', hexArray[28:])[0]))
                                                    pos9 = int(str(struct.unpack_from('<l', hexArray[36:])[0])) + 204
                                                    pos10 = int(str(struct.unpack_from('<l', hexArray[40:])[0]))
                                                    fmtStringName = "<" + str(pos4) + "s"		  
                                                    fmtStringFullname = ">" + str(pos7) + "s"
                                                    fmtStringComment = ">" + str(pos10) + "s"
                                                    userName = struct.unpack_from(fmtStringName, hexArray[pos3:])[0]
                                                    fullName = struct.unpack_from(fmtStringFullname, hexArray[pos6:])[0]
                                                    comment = struct.unpack_from(fmtStringComment, hexArray[pos9:])[0]
                                                    userName = self.utf16decode(userName)
                                                    userId[str(int(registryKey, 16))] = userName
                                                    self.printRow(val, "userName",userName)
                                                    self.printRow(val, "fullName",fullName)
                                                    self.printRow(val, "comment",comment)
                                                    self.printRow(val, "userName",userName)
                                                    self.printRow(val, "userId",userId)
                                except:
                                    self.log(Level.INFO, "no sam key")
                            except:
                                try:
                                    regKeyList1 = val.split('\\')
                                    registryKeyToFind2 = os.path.join(*(regKeyList1[1:]))
                                    
                                    samRegFile = RegistryHiveFile(File(lclDbPath))
                                    currentKey = self.findRegistryKey(samRegFile, registryKeyToFind2)

                                    
                                    
                                    self.printRow(registryKeyToFind2, "","")
                                    for value in currentKey.getValueList(): 
                                        pd = ""
                                        for st1 in value.getValue().getAsStringList():
                                            self.printRow(registryKeyToFind2, value.getName(),st1)
                                        
                                        #pd = value.getValue().getAsRawData().toString() 
                                        #self.log(Level.INFO, "mess1  " + value.getAsString())
                                        try:
                                            mn = str(value.getValue().getAsNumber())
                                            self.printRow(val, value.getName(),mn)
                                        except:
                                            self.log(Level.INFO, "no number ")
                                        
                                    try:
                                        bamKey = currentKey.getSubkeyList()
                                        for sk in bamKey:
                                            if len(sk.getValueList()) > 0:
                                                registryKey = sk.getName()
                                                skValues = sk.getValueList()
                                                for skValue in skValues:
                                                    if skValue.getName() == 'SequenceNumber' or skValue.getName() == 'Version':
                                                        pass
                                                    else:
                                                        indRecord = []
                                                        value = skValue.getValue()
                                                        binData = self.getRawData(value.getAsRawData())
                                                        msTime = struct.unpack('<qqq', binData)[0]
                                                        linuxTime = int(str(msTime)[0:11]) - 11644473600
                                                        uId = registryKey[registryKey.rfind("-")+1:]
                                                        self.printRow(registryKeyToFind2, "uid",uId)
                                                        self.printRow(registryKeyToFind2, "skValue Name",str(skValue.getName()))
                                                        self.printRow(registryKeyToFind2, "linuxTime",str(linuxTime))
                                                        self.printRow(registryKeyToFind2, "indRecord",indRecord)
                                    except:
                                        self.log(Level.INFO, "no bm key")
                                     
                                    try:
                                        samKey = currentKey.getSubkeyList()   
                                        for sk in samKey:
                                            registryKey = sk.getName()
                                            skValues = sk.getValueList()
                                            if len(skValues) > 0:
                                                for skVal in skValues:
                                                    if skVal.getName() == 'V':
                                                        value = skVal.getValue()
                                                        hexArray = self.getRawData(value.getAsRawData())
                                                        pos1 = int(str(struct.unpack_from('<l', hexArray[4:])[0]))
                                                        pos3 = int(str(struct.unpack_from('<l', hexArray[12:])[0])) + 204 
                                                        pos4 = int(str(struct.unpack_from('<l', hexArray[16:])[0]))
                                                        pos6 = int(str(struct.unpack_from('<l', hexArray[24:])[0])) + 204
                                                        pos7 = int(str(struct.unpack_from('<l', hexArray[28:])[0]))
                                                        pos9 = int(str(struct.unpack_from('<l', hexArray[36:])[0])) + 204
                                                        pos10 = int(str(struct.unpack_from('<l', hexArray[40:])[0]))
                                                        fmtStringName = "<" + str(pos4) + "s"		  
                                                        fmtStringFullname = ">" + str(pos7) + "s"
                                                        fmtStringComment = ">" + str(pos10) + "s"
                                                        userName = struct.unpack_from(fmtStringName, hexArray[pos3:])[0]
                                                        fullName = struct.unpack_from(fmtStringFullname, hexArray[pos6:])[0]
                                                        comment = struct.unpack_from(fmtStringComment, hexArray[pos9:])[0]
                                                        userName = self.utf16decode(userName)
                                                        userId[str(int(registryKey, 16))] = userName
                                                        self.printRow(registryKeyToFind2, "userName",userName)
                                                        self.printRow(registryKeyToFind2, "fullName",fullName)
                                                        self.printRow(registryKeyToFind2, "comment",comment)
                                                        self.printRow(registryKeyToFind2, "userName",userName)
                                                        self.printRow(registryKeyToFind2, "userId",userId)
                                    except:   
                                        self.log(Level.INFO, "no sam key")
                                except:
                                    a = 1
                
                
                except IOException as ex:
                        message2 = IngestMessage.createMessage(IngestMessage.MessageType.DATA, "IOEXCEPTION", "IOEXCEPTION","IOEXCEPTION")
                        IngestServices.getInstance().postMessage(message2)
        try:
            shutil.rmtree(temp_dir)		
        except:
		    self.log(Level.INFO, "removal of directory tree failed " + temp_dir)
        print "</table>"      
    def findRegistryKey(self, registryHiveFile, registryKey):
    
        rootKey = registryHiveFile.getRoot()
        regKeyList = registryKey.split('\\')
        currentKey = rootKey
        samKey = currentKey.getSubkeyList()   
            
        i = 0 
        for key in regKeyList:
            currentKey = currentKey.getSubkey(key) 
        return currentKey  

    def printRow(self, value, value1, value2):
        #sys.stdout = open(self.path_to_Webcache_file10,'w')  
        print "<tr>"
        print "<td>"
        print self.artifact_type
        print "</td>"
        print "<td>"
        print value
        print "</td>"
        print "<td>"
        print  value1
        print "</td>"
        print "<td>"
        print value2
        print "</td>"
        print "</tr>"
        
    def printRow2(self, value, value1, value2,value3):
        #sys.stdout = open(self.path_to_Webcache_file10,'w')  
        print "<tr>"
        print "<td>"
        print self.artifact_type
        print "</td>"
        print "<td>"
        print value
        print "</td>"
        print "<td>"
        print  value1
        print "</td>"
        print "<td>"
        print value2
        print "</td>"
        print "<td>"
        print value3
        print "</td>"
        print "</tr>"
    def getRawData(self, rawData):
    
        hexArray = ""
        arrayLength = rawData.remaining()
        for x in range(0, arrayLength):
            binByte = rawData.get()
            # Have to check if this is a negative number or not.  Byte will be returned -127 to 127 instead of 0 to 255
            if binByte < 0:
                binByte = 256 + binByte
            hexArray = hexArray + chr(binByte)
        return hexArray        

    def utf16decode(self, bytes):
        bytes = binascii.hexlify(bytes)
        bytes = [bytes[i:i+2] for i in range(0, len(bytes), 2)]
        bytes = (''.join(filter(lambda a: a !='00', bytes)))
        bytes = codecs.decode(bytes, 'hex')
        return(bytes)   
        
        
class AGPWithUISettingsPanel(IngestModuleIngestJobSettingsPanel):
    
    def __init__(self, settings):
        self.local_settings = settings
        self.initComponents()
        self.customizeComponents()
    
    def checkBoxEvent(self, event):
        if self.Recentlyused_CB2.isSelected():
            self.local_settings.setSetting('EXPORT', 'true')
        else:
            self.local_settings.setSetting('EXPORT', 'false')
            
        if self.Recentlyused_CB.isSelected():
            self.local_settings.setSetting('CSV_Flag', 'true')
        else:
            self.local_settings.setSetting('CSV_Flag', 'false')
            
        if self.Recentlyused_CB1.isSelected():
            self.local_settings.setSetting('DOWNLOAD', 'true')
        else:
            self.local_settings.setSetting('DOWNLOAD', 'false')  
   
    

    def initComponents(self):
        self.panel0 = JPanel()
        self.gbPanel0 = GridBagLayout() 
        self.gbcPanel0 = GridBagConstraints() 
        self.panel0.setLayout( self.gbPanel0 ) 
        self.Recentlyused_CB = JCheckBox( "File artifacts(put SearchResults.xls file inside same plugin directory level)", actionPerformed=self.checkBoxEvent) 
        self.gbcPanel0.gridx = 2 
        self.gbcPanel0.gridy = 5
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.Recentlyused_CB, self.gbcPanel0 ) 
        self.panel0.add( self.Recentlyused_CB ) 
        self.Recentlyused_CB1 = JCheckBox( "Registry Artifacts", actionPerformed=self.checkBoxEvent) 
        self.gbcPanel0.gridx = 2 
        self.gbcPanel0.gridy = 7 
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.Recentlyused_CB1, self.gbcPanel0 ) 
        self.panel0.add( self.Recentlyused_CB1 ) 
        
        
        self.Recentlyused_CB2 = JCheckBox( "Export Files", actionPerformed=self.checkBoxEvent) 
        self.gbcPanel0.gridx = 2 
        self.gbcPanel0.gridy = 9 
        self.gbcPanel0.gridwidth = 1 
        self.gbcPanel0.gridheight = 1 
        self.gbcPanel0.fill = GridBagConstraints.BOTH 
        self.gbcPanel0.weightx = 1 
        self.gbcPanel0.weighty = 0 
        self.gbcPanel0.anchor = GridBagConstraints.NORTH 
        self.gbPanel0.setConstraints( self.Recentlyused_CB2, self.gbcPanel0 ) 
        self.panel0.add( self.Recentlyused_CB2 )
        self.add(self.panel0)

    def customizeComponents(self):
        self.Recentlyused_CB.setSelected(self.local_settings.getSetting('CSV_Flag') == 'true')
        self.Recentlyused_CB1.setSelected(self.local_settings.getSetting('DOWNLOAD') == 'true')
        self.Recentlyused_CB2.setSelected(self.local_settings.getSetting('EXPORT') == 'true')
    # Return the settings used
    def getSettings(self):
        return self.local_settings

