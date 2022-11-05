from typing import List, Optional

import numpy as np
from skrobot.coordinates import Coordinates
from skrobot.coordinates.math import rpy_angle, rpy_matrix
from skrobot.model import RobotModel
from skrobot.model.primitives import Sphere
from skrobot.viewers import TrimeshSceneViewer

from skplan.kinematics import ArticulatedCollisionKinematicsMap
from skplan.sdf import SDFLike


class SphereColor:
    NORMAL = (250, 250, 10, 200)
    COLLISION = (255, 0, 0, 200)


class CollisionSphereVisualizationManager:
    kinmap: ArticulatedCollisionKinematicsMap
    viewer: TrimeshSceneViewer
    sphere_list: List[Sphere]

    def __init__(self, kinmap: ArticulatedCollisionKinematicsMap, viewer: TrimeshSceneViewer):
        sphere_list = []
        for i in range(kinmap.n_feature):
            kinmap.sphere_name_list[i]
            r = kinmap.radius_list[i]
            center = kinmap.sphere_center_list[i]
            sphere = Sphere(radius=r, pos=center, color=SphereColor.NORMAL)
            sphere_list.append(sphere)

        for sphere in sphere_list:
            viewer.add(sphere)

        self.kinmap = kinmap
        self.viewer = viewer
        self.sphere_list = sphere_list

    def update(self, point_cspace: np.ndarray, sdf: Optional[SDFLike] = None) -> None:
        tmp, _ = self.kinmap.map(np.expand_dims(point_cspace, axis=0))
        points_tspace = tmp[0]
        assert len(points_tspace) == len(self.sphere_list)

        for point, sphere in zip(points_tspace, self.sphere_list):
            co = Coordinates(point)
            sphere.newcoords(co)

        if sdf is not None:
            # warn collision state by chaning the color
            for sphere in self.sphere_list:
                point = sphere.worldpos()
                radius = sphere.visual_mesh.metadata["radius"]
                val = sdf(np.expand_dims(point, axis=0)).item() - radius
                if val < 0.0:
                    n_facet = len(sphere._visual_mesh.visual.face_colors)
                    sphere._visual_mesh.visual.face_colors = np.array(
                        [SphereColor.COLLISION] * n_facet
                    )


def set_robot_config(
    robot_model: RobotModel, joint_names: List[str], angles: np.ndarray, with_base=False
):
    if with_base:
        assert len(joint_names) + 3 == len(angles)
    else:
        assert len(joint_names) == len(angles)

    if with_base:
        av_joint, av_base = angles[:-3], angles[-3:]
        x, y, theta = av_base
        co = Coordinates(pos=[x, y, 0.0], rot=rpy_matrix(theta, 0.0, 0.0))
        robot_model.newcoords(co)
    else:
        av_joint = angles

    for joint_name, angle in zip(joint_names, av_joint):
        robot_model.__dict__[joint_name].joint_angle(angle)


def get_robot_config(
    robot_model: RobotModel, joint_names: List[str], with_base=False
) -> np.ndarray:
    joint_list = [robot_model.__dict__[name] for name in joint_names]
    av_joint = np.array([j.joint_angle() for j in joint_list])
    if with_base:
        x, y, _ = robot_model.translation
        rpy = rpy_angle(robot_model.rotation)[0]
        theta = rpy[0]
        av_whole = np.hstack((av_joint, [x, y, theta]))
        return av_whole
    else:
        return av_joint
