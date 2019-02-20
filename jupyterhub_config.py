c.JupyterHub.spawner_class = 'willspawner.DemoFormSpawner'
c.Spawner.debug = True
c.Spawner.default_url = '/lab'
#c.JupyterHub.spawner_class = 'wrapspawner.ProfilesSpawner'
#c.ProfilesSpawner.profiles = [
#       ( "Host process", 'local', 'jupyterhub.spawner.LocalProcessSpawner', {'ip':'0.0.0.0'} ),
#       ('Docker Python 2/3', 'systemuser', 'dockerspawner.SystemUserSpawner', dict(container_image="jupyterhub/systemuser")),
# ]
