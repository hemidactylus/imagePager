#!/usr/bin/env python3

'''
    imagePager.py : a utility to generate a static image gallery
    with zipfile and thumbnail view,
    thought to fit in the salaWeb ecosystem.
'''

import sys
import os
import json

from fileUtils import (
    makeThumbnail,
    createZip,
    ensureDirectoryExists,
    listImageFiles,
    copyFile,
)
from templateUtils import (
    makeFotoPage,
    makeIndex,
)

tDir='thumbs'
fDir='images'
zipFileTitle='fotos.zip'
indexFileTitle='index.html'
pageTitleTemplate='foto_{n:04}.html'
galleryTitle='GalleryTitle'

def makePageTitle(pageTemplate, index, count):
    return pageTemplate.format(n=(((index-1)+count)%count)+1)

if __name__=='__main__':
    srcDir=sys.argv[1]
    dstDir=sys.argv[2]
    doZip=True
    #
    fotoDir=os.path.join(dstDir,tDir)
    thumbDir=os.path.join(dstDir,fDir)
    ensureDirectoryExists(dstDir)
    ensureDirectoryExists(fotoDir)
    ensureDirectoryExists(thumbDir)
    #
    fileList=listImageFiles(srcDir)
    #
    galleryDesc={
        'nfotos': len(fileList),
        'title': galleryTitle,
    }
    #
    if doZip:
        print('creating ZIP')
        zipFilename=os.path.join(dstDir,zipFileTitle)
        createZip([os.path.join(srcDir,fN) for fN in fileList],zipFilename)
        galleryDesc['zipfile']=zipFileTitle
    # the foto-items
    pageTitleMaker=lambda n: makePageTitle(pageTitleTemplate,n,galleryDesc['nfotos'])
    galleryDesc['fotopages']=[]
    for _fotoIndex,fotoName in enumerate(fileList):
        fotoIndex=_fotoIndex+1
        print('[%3i] %s' % (fotoIndex,fotoName))
        fotoPageTitle=pageTitleMaker(fotoIndex)
        # create copy and thumbnail
        tFotoTitle=os.path.join(tDir,'thumb_%s' % fotoName)
        fFotoTitle=os.path.join(fDir,fotoName)
        copyFile(os.path.join(srcDir,fotoName),os.path.join(dstDir,fDir))
        makeThumbnail(os.path.join(srcDir,fotoName),os.path.join(dstDir,tFotoTitle))
        # register it
        fotoItem={
            'index': fotoIndex,
            'indexlink': indexFileTitle,
            'filename': fotoPageTitle,
            'fotoname': fFotoTitle,
            'thumbnail': tFotoTitle,
            'title': fotoName,
            'gallerytitle': galleryTitle,
        }
        if _fotoIndex>0:
            fotoItem['prevlink']=pageTitleMaker(fotoIndex-1)
        if fotoIndex<galleryDesc['nfotos']:
            fotoItem['nextlink']=pageTitleMaker(fotoIndex+1)
        galleryDesc['fotopages'].append(fotoItem)

    makeIndex(galleryDesc,os.path.join(dstDir,indexFileTitle))
    for pageDesc in galleryDesc['fotopages']:
        makeFotoPage(pageDesc, os.path.join(dstDir,pageDesc['filename']))
    print('done!')
