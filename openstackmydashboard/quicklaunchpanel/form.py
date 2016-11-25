from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms


from openstack_dashboard import api

import launch_utils


class LaunchInstances(forms.SelfHandlingForm):
    # name = forms.CharField(max_length=255, label=_("Snapshot Name"))
    config_text = forms.CharField(widget=forms.Textarea, label="Config:")

    def handle(self, request, data):
        print('up content/*****************\n')
        print(str(request.POST) + '\n')
        return 'Hehe'

    def handle_get(self, request):
        print('\n\\\\\\\\\\\\\\\\\Get method Launch instances, user name %s' %
              request.user.username)
        # azs = launch_utils.get_availability_zones(request)
        # print('\n\\\\\\\\\\\\\\\\\\\\\\\\AZ %s' % str(azs))
