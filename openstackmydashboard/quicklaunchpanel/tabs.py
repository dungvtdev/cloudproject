from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from horizon import exceptions
from horizon import tabs
from horizon.tables import LinkAction

from openstack_dashboard import api
from openstack_dashboard.dashboards.dungdashboard.quicklaunchpanel \
    import tables

from horizon.utils import memoized

from openstack_dashboard.dashboards.dungdashboard.quicklaunchpanel \
    import launch_utils


class OverviewTab(tabs.TableTab):

    name = _('OverviewTab')
    slug = 'overview_tab'
    table_classes = (tables.InstancesTable,
                     tables.ImageTable, tables.FlavorsTable)
    template_name = (
        'dungdashboard/quicklaunchpanel/overview_detail_tables.html')
    preload = False

    def has_more_data(self, table):
        if table is tables.InstancesTable:
            return getattr(self, "_has_more_instances", False)
        if table is tables.ImageTable:
            return getattr(self, "_has_more_images", False)
        if table is tables.FlavorsTable:
            return getattr(self, "_has_more_flavors", False)

    def get_instances_data(self):
        marker = self.request.GET.get(
            tables.InstancesTable._meta.pagination_param, None)
        instances, self._has_more_instances = launch_utils.get_instances_data(self.request, marker)
        return instances

    def get_flavors_data(self):
        flavors = launch_utils.get_flavors_data(self.request)
        self._has_more_flavors = flavors or False
        return flavors

    def get_images_data(self):
        marker = self.request.GET.get(
            tables.InstancesTable._meta.pagination_param, None)
        images, self._has_more_images = launch_utils.get_images_data(
            self.request, marker)
        return images


class LaunchInstance(LinkAction):
    name = "launch_instance_action"
    verbose_name = _("Launch Instance")
    url = "horizon:dungdashboard:quicklaunchpanel:launch_instances"
    classes = ("ajax-modal", "btn-primary",)
    # icon = "pencil"


class QuickLaunchTab(tabs.Tab):
    name = _('Quick Launch Tab')
    slug = 'quicklaunch_tab'
    preload = False
    template_name = 'dungdashboard/quicklaunchpanel/quicklaunch_tab.html'

    def get_context_data(self, request, **kwargs):
        """This method should return a dictionary of context data used to
        render the tab. Required.
        """
        context = super(QuickLaunchTab, self).get_context_data(
            request, **kwargs)
        context['submit_url'] = reverse(
            'horizon:dungdashboard:quicklaunchpanel:launch_instances')
        context['action'] = self.get_launch_action()
        return context

    @memoized.memoized_method
    def get_launch_action(self):
        return LaunchInstance()


class QuicklaunchpanelTabs(tabs.TabGroup):
    slug = "quicklaunchpanel_tabs"
    tabs = (OverviewTab, QuickLaunchTab,)
    sticky = True
