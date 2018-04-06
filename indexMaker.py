#!/usr/bin/env python3

'''
    indexMaker.py : a quick and dirty
    index page generation utility.
    Run this in the home dir
    where you want the index to be
    created
'''

import sys
import os
import json

from fileUtils import (
    getFilesAndDirs,
)
from templateUtils import (
    makeFileIndex,
)
from cmdLineParse import cmdLineParse

indexFileTitle='index.html'

staticAddressPrefix="/static/salaWeb/"

def makePageTitle(pageTemplate, index, count):
    return pageTemplate.format(n=(((index-1)+count)%count)+1)

if __name__=='__main__':
    helpMsg='''
        Usage:
            ./indexMaker <dstDir>
                [-standalone, no reliance on anything else]
                [-title TitleOfPage]
                [-text SubTitleText]
    '''
    args,opts = cmdLineParse(sys.argv[1:])
    doHelp=False
    abort=False
    if 'h' in opts:
        doHelp=True
    else:
        if len(args)!=1:
            doHelp=True
            abort=True
        else:
            dstDir=args[0]
            if 'standalone' in opts:
                standalone=True
            else:
                standalone=False
            if 'title' in opts:
                forcedTitle=opts['title'][0]
            else:
                forcedTitle=None
            if 'text' in opts:
                subTitleText=' '.join(opts['text'])
            else:
                subTitleText=None
    #
    if doHelp:
        if abort:
            print('ERROR in command line arguments.')
        print(helpMsg)
    else:
        print('Creating index')
        # get dirs and files
        fileItems=getFilesAndDirs(dstDir,blackList=[indexFileTitle])
        #
        if forcedTitle is None:
            theDir=os.path.split(dstDir)[1]
            if theDir=='.':
                theDir=subTitleText
        else:
            theDir=forcedTitle
        #
        fileDesc={
            'fileItems': fileItems,
            'title': theDir,
            'text': subTitleText,
        }
        makeFileIndex(
            fileDesc,
            os.path.join(dstDir,indexFileTitle),
            staticAddressPrefix=staticAddressPrefix,
            standalone=standalone,
        )
        print('done.')
