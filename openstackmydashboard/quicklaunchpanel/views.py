# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from horizon import tabs
from horizon import forms
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from horizon.utils import memoized

from openstack_dashboard.dashboards.dungdashboard.quicklaunchpanel \
    import tabs as dungdashboard_tabs
from openstack_dashboard.dashboards.dungdashboard.quicklaunchpanel \
    import form as quicklaunchforms


from django.conf import settings
import launch_utils


class IndexView(tabs.TabbedTableView):
    tab_group_class = dungdashboard_tabs.QuicklaunchpanelTabs
    template_name = 'dungdashboard/quicklaunchpanel/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context


class LaunchInstanceView(forms.ModalFormView):
    form_class = quicklaunchforms.LaunchInstances
    template_name = 'dungdashboard/quicklaunchpanel/launch_instances.html'
    success_url = reverse_lazy("horizon:dungdashboard:quicklaunchpanel:index")
    modal_id = "launch_instance_modal"
    modal_header = _("Launch Instance")
    submit_label = _("Launch Instance")
    submit_url = "horizon:dungdashboard:quicklaunchpanel:launch_instances"

    @memoized.memoized_method
    def get_object(self):
        return []

    def get_initial(self):
        print('\n\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\init\n')
        return {'config_text': self._config_template}

    def get_context_data(self, **kwargs):
        context = super(LaunchInstanceView, self).get_context_data(**kwargs)
        context['submit_url'] = reverse(self.submit_url)
        return context

    def get_default_config(self):
        return 'asfasd'

    def get(self, request, *args, **kwargs):
        print('\n\\\\\\\\\\\\\\\\\\\\\\request_get_333 %s \n' % str(request))
        self._config_template = launch_utils.launch_utils_object \
            .get_config_template(request)
        return super(LaunchInstanceView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print('\n\\\\\\\\\\\\\\\\\\\\\\request %s \n' % str(request))
        return super(LaunchInstanceView, self).post(request, *args, **kwargs)
