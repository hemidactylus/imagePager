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

def normaliseRotation(imgName):
    '''
        uses 'mogrify' with the -auto-orient flag to shift
        all rotations from the exif data to the image file
    '''
    subprocess.check_output(
        [
            'mogrify',
            '-auto-orient',
            imgName,
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

def getFilesAndDirs(dirName,blackList=[]):
    '''
        returns a list of {
            'filename': 'aaa.txt',
            'isdir': True/False,
            'size': 123, # KB (None for dirs)
        } items, sorted with dirs first and then
        alphabetically (case insensitive)
    '''
    names=[]
    for fName in os.listdir(dirName):
        if fName not in blackList:
            tItem={
                'filename': fName
            }
            fullName=os.path.join(dirName,fName)
            if os.path.isfile(fullName):
                tItem['isdir']=False
                tItem['size']=int(os.path.getsize(fullName)/1024)
                names.append(tItem)
            elif os.path.isdir(fullName):
                tItem['isdir']=True
                tItem['size']=None
                names.append(tItem)
    return sorted(
        names,
        key=lambda itm: (0 if itm['isdir'] else 1, itm['filename'].lower()),
    )
