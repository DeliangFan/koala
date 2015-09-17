# Server Specific Configurations
server = {
    'port': '8080',
    'host': '0.0.0.0'
}

# Pecan Application Configurations
app = {
    'root': 'example.api.controllers.root.RootController',
    'modules': ['example.api'],
    'static_root': '%(confdir)s/public',
    'template_path': '%(confdir)s/example/api/templates',
    'debug': False,
}

wsme = {
    'debug': True
}

# Custom Configurations must be in Python dictionary format::
#
# foo = {'bar':'baz'}
#
# All configurations are accessible at::
# pecan.conf
