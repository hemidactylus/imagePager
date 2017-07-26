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
    normaliseRotation,
)
from templateUtils import (
    makeFotoPage,
    makeIndex,
)
from cmdLineParse import cmdLineParse

indexFileTitle='index.html'
pageTitleTemplate='foto_{n:04}.html'

staticAddressPrefix="/static/salaWeb/"

def makePageTitle(pageTemplate, index, count):
    return pageTemplate.format(n=(((index-1)+count)%count)+1)

if __name__=='__main__':
    helpMsg='''
        Usage:
            ./imagePager <srcDir> <dstDir>
                -t "Title of gallery"
                [-z [zipfilename]]
                [-thumbdir thumbdir]
                [-fotodir fotodir]
                [-standalone, no reliance on anything else]
    '''
    args,opts = cmdLineParse(sys.argv[1:])
    doHelp=False
    abort=False
    if 'h' in opts:
        doHelp=True
    else:
        if len(args)!=2:
            doHelp=True
            abort=True
        else:
            srcDir=args[0]
            dstDir=args[1]
            if 'z' in opts:
                doZip=True
                if len(opts['z'])>0:
                    zipFileTitle=opts['z'][0]
                else:
                    zipFileTitle='images.zip'
            else:
                doZip=False
            if 't' not in opts or len(opts['t'])!=1:
                doHelp=True
                abort=True
            else:
                galleryTitle=opts['t'][0]
            if 'standalone' in opts:
                standalone=True
            else:
                standalone=False
            tDir=opts.get('thumbdir',['thumbs'])[0]
            fDir=opts.get('fotodir',['images'])[0]
            fDir=opts.get('fotodir',['images'])[0]
    #
    if doHelp:
        if abort:
            print('ERROR in command line arguments.')
        print(helpMsg)
    else:
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
            normaliseRotation(os.path.join(dstDir,fDir,fotoName))
            makeThumbnail(os.path.join(dstDir,fDir,fotoName),os.path.join(dstDir,tFotoTitle))
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

        makeIndex(
            galleryDesc,
            os.path.join(dstDir,indexFileTitle),
            staticAddressPrefix=staticAddressPrefix,
            standalone=standalone,
        )
        for pageDesc in galleryDesc['fotopages']:
            makeFotoPage(
                pageDesc,
                os.path.join(dstDir,pageDesc['filename']),
                staticAddressPrefix=staticAddressPrefix,
                standalone=standalone,
            )
        print('done.')
