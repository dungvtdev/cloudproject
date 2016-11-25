from django.conf import settings
from os import path

print('\n\n//////////////////setting\n %s' % settings.ROOT_PATH)


class MyConfig(object):
    conf_template_file = \
        'dashboards/dungdashboard/quicklaunchpanel/config/config_template.txt'

    def get_conf_template_abspath(self):
        p = path.join(settings.ROOT_PATH, self.conf_template_file)
        print('\n\\\\\\\\\path %s\n' % p)
        return p

config = MyConfig()
config.get_conf_template_abspath()