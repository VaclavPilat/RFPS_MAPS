## \file
# Object trait for interacting with Blender
from Mesh.Object import Object
import bpy, bmesh



def create(self) -> "bpy mesh":
    """Creating a blender mesh from face vertices

    Returns:
        bpy mesh: Created mesh object
    """
    mesh = bpy.data.meshes.new(self.name)
    bm = bmesh.new()
    vertices = {}
    for face in self.faces:
        for vert in face:
            if vert not in vertices:
                vertices[vert] = bm.verts.new(tuple(vert))
        bm.faces.new([vertices[vert] for vert in face])
    bm.to_mesh(mesh)
    return mesh
Object.create = create



## \todo Add object rotations
def build(self) -> "bpy object":
    """Building a blender object from an Object instance

    Returns:
        bpy object: Built blender object
    """
    obj = bpy.data.objects.new(self.name, self.create() if len(self.faces) else None)
    obj.location = list(self.position)
    bpy.context.scene.collection.objects.link(obj)
    for child in self.objects:
        child.build().parent = obj
    return obj
Object.build = build