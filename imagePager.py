#!/usr/bin/env python3

import sys
import os
import shutil
import subprocess

def htmlpreamble(title,color='#a5edc2'):
    return '''<html>
    <head>
        <title>%s</title>
    </head>
    <body bgcolor="%s">
''' % (title,color)
    
def htmlclosing():
    return '''</body>
    </html>
    '''

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
    
if __name__=='__main__':
    srcDir=sys.argv[1]
    dstDir=sys.argv[2]
    doZip=True
    tDir='thumbs'
    fDir='images'
    fileList=sorted([f for f in os.listdir(srcDir) if isImage(f)])
    
    if doZip:
        zipFilename=os.path.join(dstDir,'fotos.zip')
        createZip([os.path.join(srcDir,fN) for fN in fileList],zipFilename)

    destIndex=open(os.path.join(dstDir,'index.html'),'w')
    destIndex.write(htmlpreamble('Foto Index'))
    destIndex.write("%s<hr>%s<hr>\n" % (
        'Foto Index',
        'Click sulle foto per navigare. Nelle foto a schermo pieno, click sulla foto per massima risoluzione.'
    ))
    if doZip:
        print('creating ZIP')
        destIndex.write('<a href="%s">File archivio con tutte le foto</a><hr>\n' % (
            'fotos.zip'
        ))
    try:
        os.mkdir(os.path.join(dstDir,tDir))
        os.mkdir(os.path.join(dstDir,fDir))
    except:
        print('Trouble making thumb/foto directories')
        pass
    nFotos=len(fileList)

    for _fotoIndex,fotoName in enumerate(fileList):
        fotoIndex=_fotoIndex+1
        print('%3i %s' % (fotoIndex, fotoName))
        ffile=open(os.path.join(dstDir,'foto_%03i.html' % fotoIndex),'w')
        ffile.write(htmlpreamble('Foto N. %i (%s)' % (fotoIndex, fotoName)))
        menu='<b>%s</b><br><a href="%s">Precedente</a>&nbsp;<a href="%s">Indice</a>&nbsp;<a href="%s">Successivo</a><hr>' % (
                fotoName,
                ('foto_%03i.html' % (1+((_fotoIndex-1+nFotos)%nFotos))),
                'index.html',
                ('foto_%03i.html' % (1+((_fotoIndex+1)%nFotos))),
            )
        # create copy and thumbnail
        shutil.copy(os.path.join(srcDir,fotoName),os.path.join(dstDir,fDir))
        tFotoName='thumb_%s' % fotoName
        makeThumbnail(os.path.join(srcDir,fotoName),os.path.join(dstDir,tDir,tFotoName))
        #
        ffile.write('%s<br><a href="%s/%s"><img height="75%%" src="%s/%s"></a><br>\n' % (menu, fDir,fotoName, fDir,fotoName))
        ffile.close()
        destIndex.write('<a href="%s">Foto %03i (%s)<img src="%s/%s" height="180px"></a><br>\n' % (('foto_%03i.html' % fotoIndex),fotoIndex,fotoName,tDir,tFotoName))

    destIndex.write("<hr>\n")
    destIndex.write(htmlclosing())

    destIndex.close()
