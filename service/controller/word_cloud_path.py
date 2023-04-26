from flask import Blueprint

world_cloud_path= Blueprint('world_cloud_path', __name__)

# path
@world_cloud_path.route('/')
def index():
    return 'world_cloud_path'

