'''
    templateUtils.py : tools to deal with
    the image gallery template html files
'''

from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader('imageGallery', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

def makeIndex(galleryDesc, destFileName, staticAddressPrefix):
    indexTemplate = env.get_template('index.html')
    open(destFileName,'w').write(
        indexTemplate.render(
            galleryDesc=galleryDesc,
            title=galleryDesc['title'],
            staticAddressPrefix=staticAddressPrefix
        )
    )

def makeFotoPage(pageDesc, destFileName, staticAddressPrefix):
    pageTemplate = env.get_template('fotopage.html')
    open(destFileName,'w').write(
        pageTemplate.render(
            pageDesc=pageDesc,
            title=pageDesc['title'],
            staticAddressPrefix=staticAddressPrefix
        )
    )
