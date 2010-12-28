#zope stuff
from zope.interface import Interface
from zope.container.constraints import contains
from zope import schema

#grok stuff
import grok

#dolmen stuff
from dolmen.app.site import Dolmen
from dolmen.app.content import icon
from dolmen.file import ImageField
from dolmen.blob import BlobProperty
from dolmen import content
from dolmen.app.security.content import CanAddContent, CanViewContent
from dolmen.app.layout import models

#menhir imports
from menhir.contenttype.image import IImage, Image

#cinezune stuff
from cinezune.locaciones import LocacionesMessageFactory as _

class Locaciones(Dolmen):
    content.nofactory()
    title= _(u"Cinezune")

class LocacionesIndex(models.Index):
    grok.context(Locaciones)
    content.require(CanViewContent)

class IPicture(IImage):
    """A Picture of a location
    """
    description = schema.Text(
        title=_(u"Private description"),
        description=_(u"This is a private description of a location. This information will not be public.")
        )


class Picture(Image):
    """A simple image storing its data in a blob.
    """
    content.name(u'A photo of the location')
    content.schema(IPicture)


class ILocation (Interface):
    contains(IPicture)
    title = schema.TextLine( title=_(u"Location title"),
                             description = _(u"Give a title of the site")
                             )
    private_description = schema.Text(
        title=_(u"Private description"),
        description=_(u"This is a private description of a location. This information will not be public.")
        )

    address = schema.Text(
            title=_(u"Location address"),
            description=_(u"Please write the address of this location. This information will not be public."),
        )

    map_url = schema.URI (
            title=_(u"Google Map URL"),
            description=_(u"This is the URL of a google map with information about this location. This information will not be public."),
            required=False,
        )

    sketch = ImageField(
            title=_(u"Sketch Map"),
            description=_(u"Please upload an image for the sketch map. This information will not be public."),
            required=False,
        )

class Location (content.Container):
    grok.implements(ILocation)
    content.schema(ILocation)
    content.name(u'A Location with photos')
    content.require(CanAddContent)
    sketch = BlobProperty(ILocation['sketch'])

class LocationIndex(models.Index):
    grok.context(Location)
    content.require(CanViewContent)
