from willspawner import ParamForm

c.JupyterHub.spawner_class = 'willspawner.FormLocalSpawner'
c.FormLocalSpawner.form_inst = ParamForm(source='static/ic.html')
c.Spawner.debug = True
# c.Spawner.default_url = '/lab'

# c.PAMAuthenticator.open_sessions = False


#c.JupyterHub.spawner_class = 'wrapspawner.ProfilesSpawner'
#c.ProfilesSpawner.profiles = [
#       ( "Host process", 'local', 'jupyterhub.spawner.LocalProcessSpawner', {'ip':'0.0.0.0'} ),
#       ('Docker Python 2/3', 'systemuser', 'dockerspawner.SystemUserSpawner', dict(container_image="jupyterhub/systemuser")),
# ]
