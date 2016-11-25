from horizon import exceptions
from horizon.utils import memoized

from django.utils.translation import ugettext as _
from django import template

from openstack_dashboard import api
import openstack_dashboard.dashboards.dungdashboard.quicklaunchpanel as mypanel


class LaunchUtils(object):

    def get_launch_state(self, request):
        """
        Return infomation: availability_zone, image, flavor, network, subnet
        Phuc vu goi y trong file config, tra ve template cho nguoi dung
        """
        availability_zones = get_availability_zones(request)
        images, _ = get_images_data(request)
        networks = get_networks_data(request)
        # flavors = get_flavors_data(request)
        state = {}
        state['availability_zones'] = availability_zones
        state['images'] = images
        state['networks'] = networks
        return state

    def get_resource_state():
        """
        Return info: ram, storage(root, ephemeral)
        """
        pass

    def get_network_ip_resources():
        """
        Return info: float-ip, ip da su dung
        """
        pass

    def create_instances(self, config):
        """
        Create instance in file-config
        """
        pass

    def get_config_template(self, request):
        state = self.get_launch_state(request)
        template_name = 'dungdashboard/quicklaunchpanel/config/config_template.html'
        internal_networks = list(MyNetwork(n.name_or_id, n.subnets)
                             for n in state['networks'] if not n['router:external'])
        print('\n\\\\\\\\\\\\\\\\\\\internal network: %s' %
              str(internal_networks))
        external_networks = list(MyNetwork(n.name_or_id, n.subnets)
                             for n in state['networks'] if n['router:external'])
        context = {"availability_zones": state['availability_zones'],
                   "images": list(im.name for im in state['images']),
                   "internal_networks": internal_networks,
                   "external_networks": external_networks}
        return template.loader.render_to_string(template_name, context)


class MyNetwork(object):

    def __init__(self, name, subnets):
        self.name = name
        self.subnets = subnets

launch_utils_object = LaunchUtils()


def get_availability_zones(request):
    zone_list = []

    try:
        zones = api.nova.availability_zone_list(request)
        zone_list = [zone.zoneName
                     for zone in zones if zone.zoneState['available']]
        zone_list.sort()
    except Exception:
        exceptions.handle(request, _('Unable to retrieve availability '
                                     'zones.'))
    if len(zone_list) > 1:
        zone_list.insert(0, "Any")

    return zone_list


def get_images_data(request, marker=None):
    try:
        images, _has_more_images, _prev = api.glance.image_list_detailed(
            request, marker=marker, paginate=True, sort_dir='asc',
            sort_key='name')

        return images, _has_more_images
    except Exception:
        _has_more_images = False
        error_message = _('Unable to get images')
        exceptions.handle(request, error_message)
        return [], _has_more_images


def get_flavors_data(request):
    try:
        flavors = api.nova.flavor_list(request)
        return flavors
    except Exception:
        error_message = _('Unable to get flavors')
        exceptions.handle(request, error_message)
        return []


def get_instances_data(request, marker=None):
    try:
        instances, _has_more_instances = api.nova.server_list(
            request,
            search_opts={'marker': marker, 'paginate': True})

        return instances, _has_more_instances
    except Exception:
        _has_more_instances = False
        error_message = _('Unable to get instances')
        exceptions.handle(request, error_message)

        return [], _has_more_instances


def get_networks_data(request):
    try:
        tenant_id = request.user.tenant_id
        networks = api.neutron.network_list_for_tenant(
            request, tenant_id, include_external=True)
        print('\n\\\\\\\\\\\\\\typeof networks %s' % str(networks))
    except Exception:
        networks = []
        msg = _('Network list can not be retrieved.')
        exceptions.handle(request, msg)
    return networks
