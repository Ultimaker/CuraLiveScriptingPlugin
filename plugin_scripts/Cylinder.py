# Copyright (c) 2023 5@xes
# A Simple Code to create a Cylinder in Cura Using Trimesh

import numpy
import trimesh

from cura.CuraApplication import CuraApplication

from UM.Mesh.MeshData import MeshData, calculateNormalsFromIndexedVertices

from UM.Operations.AddSceneNodeOperation import AddSceneNodeOperation
from cura.Scene.CuraSceneNode import CuraSceneNode
from cura.Scene.SliceableObjectDecorator import SliceableObjectDecorator
from cura.Scene.BuildPlateDecorator import BuildPlateDecorator

def toMeshData(tri_node: trimesh.base.Trimesh) -> MeshData:
    tri_faces = tri_node.faces
    tri_vertices = tri_node.vertices

    indices = []
    vertices = []

    index_count = 0
    face_count = 0
    for tri_face in tri_faces:
        face = []
        for tri_index in tri_face:
            vertices.append(tri_vertices[tri_index])
            face.append(index_count)
            index_count += 1
        indices.append(face)
        face_count += 1

    vertices = numpy.asarray(vertices, dtype=numpy.float32)
    indices = numpy.asarray(indices, dtype=numpy.int32)
    normals = calculateNormalsFromIndexedVertices(vertices, indices, face_count)

    mesh_data = MeshData(vertices=vertices, indices=indices, normals=normals)
    return mesh_data

def addShape(mesh_data: MeshData) -> None:
    application = CuraApplication.getInstance()
    global_stack = application.getGlobalContainerStack()
    if not global_stack:
        return

    node = CuraSceneNode()

    node.setMeshData(mesh_data)
    node.setSelectable(True)
    node.setName("SimpleShape" + str(id(mesh_data)))

    scene = CuraApplication.getInstance().getController().getScene()
    op = AddSceneNodeOperation(node, scene.getRoot())
    op.push()

    default_extruder_position = application.getMachineManager().defaultExtruderPosition
    default_extruder_id = global_stack.extruders[default_extruder_position].getId()
    node.callDecoration("setActiveExtruder", default_extruder_id)

    active_build_plate = application.getMultiBuildPlateModel().activeBuildPlate
    node.addDecorator(BuildPlateDecorator(active_build_plate))

    node.addDecorator(SliceableObjectDecorator())

    application.getController().getScene().sceneChanged.emit(node)

"""
Cylinder creation Radius = 10 height = 20
"""
addShape(toMeshData(trimesh.primitives.Cylinder(radius = 10, height = 20)))

