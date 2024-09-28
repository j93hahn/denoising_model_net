from __future__ import annotations

from pathlib import Path
import os.path as osp
import open3d as o3d


class OFFObject:
    def __init__(self, vertices: list[list[float]], faces: list[list[int]]):
        self.vertices = vertices
        self.faces = faces

    def viz(self):
        mesh = o3d.geometry.TriangleMesh()
        mesh.vertices = o3d.utility.Vector3dVector(self.vertices)
        mesh.triangles = o3d.utility.Vector3iVector(self.faces)
        mesh.compute_vertex_normals()
        o3d.visualization.draw_geometries([mesh])

    @staticmethod
    def read_off_file(file: str) -> OFFObject:
        """
        Parses an .off file and return an OFFObject instance. There
        are some (known) inconsistencies in the .off file format that
        require additional logic such as the if/else statement. We make
        the assumption that the OFF file's faces always describe a triangle.

        https://segeval.cs.princeton.edu/public/off_format.html
        """
        assert file.endswith('.off'), 'File must be a .off file'

        with open(file, 'r') as f:
            lines = f.readlines()

        start_idx = 1
        if lines[0].strip() != 'OFF':   # numEdges = 0 always
            start_idx = 0
            num_vertices, num_faces, _ = map(int, lines[start_idx][3:].split())
        else:
            num_vertices, num_faces, _ = map(int, lines[start_idx].split())

        start_idx += 1

        vertices, faces = [], []
        for line in lines[start_idx:start_idx + num_vertices]:
            vertices.append(list(map(float, line.split())))

        for line in lines[start_idx + num_vertices:]:
            # index [1:] to skip the number of vertices in the face (always 3)
            faces.append(list(map(int, line.split()))[1:])

        assert num_faces == len(faces), \
            'Number of faces does not match the number of faces in the file'

        return OFFObject(vertices, faces)


if __name__ == '__main__':
    file = osp.abspath('data/tetra.off')
    obj = OFFObject.read_off_file(file)
    obj.viz()
