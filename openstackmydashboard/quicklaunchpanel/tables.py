from django.utils.translation import ugettext_lazy as _
from django.template import defaultfilters as filters
from horizon import tables

from horizon.templatetags import sizeformat


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class FilterNameAction(tables.FilterAction):

    def filter(self, table, data, filter_string):
        """Really naive case-insensitive search."""
        q = filter_string.lower()

        def comp(data):
            return q in getattr(data, 'name', q).lower()

        return filter(comp, flavors)


class InstancesTable(tables.DataTable):
    name = tables.Column('name', verbose_name=_('Name'))
    image_name = tables.Column('image_name', verbose_name=_('Image Name'))
    # ip = tables.Column(
    # size = tables.Column(get_size, sortable=False, verbose_name=_("Size"))
    status = tables.Column('status', verbose_name=_('Status'))

    class Meta(object):
        name = 'instances'
        verbose_name = _('Instances')
        table_actions = (MyFilterAction,)


def get_image_name(image):
    return getattr(image, "name", None) or image.id


def get_format(image):
    format = getattr(image, "disk_format", "")
    # The "container_format" attribute can actually be set to None,
    # which will raise an error if you call upper() on it.
    if not format:
        return format
    if format == "raw":
        if getattr(image, "container_format") == 'docker':
            return pgettext_lazy("Image format for display in table",
                                 u"Docker")
        # Most image formats are untranslated acronyms, but raw is a word
        # and should be translated
        return pgettext_lazy("Image format for display in table", u"Raw")
    return format.upper()


class ImageTable(tables.DataTable):
    name = tables.Column(get_image_name, truncate=40, verbose_name='Name')
    status = tables.Column("status",
                           verbose_name=_("Status"),)
    disk_format = tables.Column(get_format, verbose_name=_("Format"))
    size = tables.Column("size",
                         filters=(filters.filesizeformat,),
                         attrs=({"data-type": "size"}),
                         verbose_name=_("Size"))

    class Meta(object):
        name = 'images'
        verbose_name = _('Images')
        table_actions = (MyFilterAction,)


def get_size(flavor):
    return sizeformat.mb_float_format(flavor.ram)


def get_disk_size(flavor):
    return _("%sGB") % (flavor.disk or 0)


def get_ephemeral_size(flavor):
    return _("%sGB") % getattr(flavor, 'OS-FLV-EXT-DATA:ephemeral', 0)


def get_swap_size(flavor):
    return _("%sMB") % (flavor.swap or 0)


class FlavorsTable(tables.DataTable):
    name = tables.Column('name', verbose_name=_('Flavor Name'))
    vcpus = tables.Column('vcpus', verbose_name=_('VCPUs'))
    ram = tables.Column(get_size,
                        verbose_name=_('RAM'),
                        attrs={'data-type': 'size'})
    disk = tables.Column(get_disk_size,
                         verbose_name=_('Root Disk'),
                         attrs={'data-type': 'size'})
    ephemeral = tables.Column(get_ephemeral_size,
                              verbose_name=_('Ephemeral Disk'),
                              attrs={'data-type': 'size'})
    swap = tables.Column(get_swap_size,
                         verbose_name=_('Swap Disk'),
                         attrs={'data-type': 'size'})

    class Meta(object):
        name = 'flavors'
        verbose_name = _("Flavors")
        table_actions = (FilterNameAction,)
