from __future__ import annotations

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

    @staticmethod
    def read_off_file(file: str) -> OFFObject:
        """
        https://segeval.cs.princeton.edu/public/off_format.html
        """
        assert file.endswith('off'), 'File must be a .off file'

        with open(file, 'r') as f:
            lines = f.readlines()

        assert lines[0].strip() == 'OFF', 'First line must be "OFF"'

        num_vertices, num_faces, _ = map(int, lines[1].split())

        vertices = []
        for line in lines[2:2 + num_vertices]:
            vertices.append(list(map(float, line.split())))

        faces = []
        for line in lines[2 + num_vertices:]:
            faces.append(list(map(int, line.split()))[1:])

        return OFFObject(vertices, faces)


def dir_vine(data_dir: str):
    return Path(dir) / 'vine'


if __name__ == '__main__':
    file = 'data/example.off'
    obj = OFFObject.read_off_file(file)
    obj.viz()
