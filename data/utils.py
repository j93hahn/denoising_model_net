from pathlib import Path
import open3d as o3d


class OFFObject:
    def __init__(self, vertices, faces):
        self.vertices = vertices
        self.faces = faces

    def viz(self):
        mesh = o3d.geometry.TriangleMesh()
        mesh.vertices = o3d.utility.Vector3dVector(self.vertices)
        mesh.triangles = o3d.utility.Vector3iVector(self.faces)
        o3d.visualization.draw_geometries([mesh])


def dir_vine(data_dir: str):
    return Path(dir) / 'vine'


"""
https://segeval.cs.princeton.edu/public/off_format.html
"""
def read_off_file(file: str):
    assert file.endswith('off'), 'File must be a .off file'

    with open(file, 'r') as f:
        lines = f.readlines()
