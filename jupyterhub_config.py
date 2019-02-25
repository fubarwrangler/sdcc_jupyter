from sdcc_jupyter_spawners import SlurmForm

c.JupyterHub.spawner_class = 'sdcc_jupyter_spawners.ChooseSpawner'
c.ChooseSpawner.form_inst = SlurmForm(source='static/ic.html')
c.Spawner.debug = True
# c.Spawner.default_url = '/lab'

# c.PAMAuthenticator.open_sessions = False


#c.JupyterHub.spawner_class = 'wrapspawner.ProfilesSpawner'
#c.ProfilesSpawner.profiles = [
#       ( "Host process", 'local', 'jupyterhub.spawner.LocalProcessSpawner', {'ip':'0.0.0.0'} ),
#       ('Docker Python 2/3', 'systemuser', 'dockerspawner.SystemUserSpawner', dict(container_image="jupyterhub/systemuser")),
# ]
