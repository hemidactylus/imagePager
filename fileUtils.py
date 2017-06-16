'''
    fileUtils.py : libraries to handle thumbnail and zip generation,
    file identification, directory creation and the like
'''

import os
import shutil
import subprocess

def isImage(fname):
    return fname[-4:].lower()=='.jpg'

def makeThumbnail(src,dst):
    subprocess.check_output(
        [
            'convert',
            '-scale',
            '5%',
            src,
            dst,
        ]
    )
    
def createZip(srcFiles,dstZip):
    cmdList=['zip',dstZip]+srcFiles
    subprocess.check_output(cmdList)

def listImageFiles(srcDir):
    return sorted([f for f in os.listdir(srcDir) if isImage(f)])

def ensureDirectoryExists(dirName):
    '''
        if directory does not exist, it is created
    '''
    if not os.path.isdir(dirName):
        os.mkdir(dirName)

def copyFile(src,dst):
    shutil.copy(src,dst)
