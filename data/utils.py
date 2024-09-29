from __future__ import annotations

import numpy as np
import open3d as o3d


class OFFObject:
    def __init__(self, file_path: str, vertices: np.ndarray, faces: np.ndarray, include_faces: bool=False):
        self.file_path = file_path
        self.vertices = vertices
        if include_faces:
            # for 90% of our use cases, we only need the point cloud vertices
            self.faces = faces

    def viz_point_cloud(self):
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(self.vertices)
        o3d.visualization.draw_geometries([pcd])

    def viz_mesh(self):
        if not hasattr(self, 'faces'):
            # there are tools such as Poisson reconstruction which can
            # generate the faces, but I observe bad performance here and
            # choose to not include it
            return

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
        vertices = np.array(vertices, dtype=np.float32)

        for line in lines[start_idx + num_vertices:]:
            # index [1:] to skip the number of vertices in the face (always 3)
            faces.append(list(map(int, line.split()))[1:])
        faces = np.array(faces, dtype=np.int32)

        assert num_faces == len(faces), \
            'Number of faces does not match the number of faces in the file'

        return OFFObject(file, vertices, faces, include_faces=True)

    def write_off_file(self):
        """
        Save the point cloud only as a .ply file. This is useful for
        visualization purposes.
        """
        with open(f'{self.file_path.removesuffix(".off")}.ply', 'w') as f:
            f.write(f'num vertices {len(self.vertices)}\n')
            for vertex in self.vertices:
                f.write(f'{vertex[0]} {vertex[1]} {vertex[2]}\n')

    def noise(self, std: float) -> OFFObject:
        """
        Adds noise directly to the vertices of the object. The noise is sampled
        from a normal distribution with mu = 0 and std = std.
        """
        corrupted_vertices = self.vertices + np.random.normal(0, std, self.vertices.shape)
        return OFFObject(self.file_path, corrupted_vertices, self.faces, include_faces=True)

    def occlude(self, ratio: float) -> OFFObject:
        """
        Selects a random point in the object, and removes the closest points
        to that point. The algorithm is simple: for each vertex, calculate its
        distance to ground zero; we take the arg indices of the sorted distances
        in an increasing order and remove the first ratio * len(self) vertices.
        """
        ground_zero = self.vertices[np.random.choice(len(self.vertices))]
        distances = np.linalg.norm(self.vertices - ground_zero, axis=1)
        occluded_indices = np.argsort(distances)[:int(ratio * len(self))]
        occluded_vertices = np.delete(self.vertices, occluded_indices, axis=0)
        return OFFObject(self.file_path, occluded_vertices, self.faces)

    def __len__(self):
        return len(self.vertices)

    def __repr__(self):
        return f'OFFObject with {len(self)} vertices'


if __name__ == '__main__':
    file = 'ModelNet40/airplane/test/airplane_0627.off'
    obj = OFFObject.read_off_file(file)
    obj.viz_mesh()
    obj.viz_point_cloud()

    noised_obj = obj.noise(10.0)
    noised_obj.viz_mesh()
    noised_obj.viz_point_cloud()

    occluded_obj = obj.occlude(0.5)
    occluded_obj.viz_point_cloud()
