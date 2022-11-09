from abc import ABC
from manipulation.exercises.grader import Grader


class ProblemSetBase(ABC):

    def __init__(self,
                 notebook_ipynb_list,
                 test_cases_list,
                 drake_tag):
        self.notebook_ipynb_list = notebook_ipynb_list
        self.test_cases_list = test_cases_list
        self.drake_tag = drake_tag
        self.results_json = '/autograder/results/results.json'

    def grade_problem_set(self):
        Grader.grade_from_notebooks(
            self.test_cases_list, self.notebook_ipynb_list, self.results_json)

class ProblemSet0(ProblemSetBase):

    def __init__(self):
        notebook_ipynb_list = [
            '/autograder/submission/manipulation_station_io.ipynb',
            '/autograder/submission/direct_joint_control.ipynb'
            ] 
        from manipulation.exercises.robot.test_manipulation_io \
            import TestManipulationIO
        from manipulation.exercises.robot.test_direct_joint_control \
            import TestDirectJointControl

        test_cases_list = [TestManipulationIO, TestDirectJointControl]
        drake_tag = 'drake-20220822'

        super().__init__(
            notebook_ipynb_list=notebook_ipynb_list,
            test_cases_list=test_cases_list,
            drake_tag=drake_tag)

class ProblemSet1(ProblemSetBase):

    def __init__(self):
        notebook_ipynb_list = [
            '/autograder/submission/reflected_inertia.ipynb',
            '/autograder/submission/planar_manipulator.ipynb',
            '/autograder/submission/rigid_transforms.ipynb']
        from manipulation.exercises.robot.test_reflected_inertia \
            import TestSimplePendulumWithGearbox
        from manipulation.exercises.pick.test_planar_manipulator \
            import TestPlanarManipulator
        from manipulation.exercises.pick.test_rigid_transforms \
            import TestRigidTransforms
        test_cases_list = [TestSimplePendulumWithGearbox,
                           TestPlanarManipulator,
                           TestRigidTransforms]

        drake_tag = 'drake-20220822'
        super().__init__(
            notebook_ipynb_list=notebook_ipynb_list,
            test_cases_list=test_cases_list,
            drake_tag=drake_tag)

class ProblemSet2(ProblemSetBase):

    def __init__(self):

        notebook_ipynb_list = [
            '/autograder/submission/robot_painter.ipynb',
            '/autograder/submission/intro_to_qp.ipynb',                        
            '/autograder/submission/differential_ik_optimization.ipynb']
        from manipulation.exercises.pick.test_robot_painter \
            import TestRobotPainter
        from manipulation.exercises.pick.test_simple_qp \
            import TestSimpleQP
        from manipulation.exercises.pick.test_differential_ik \
            import TestDifferentialIK
        test_cases_list = [TestRobotPainter,
                           TestSimpleQP,
                           TestDifferentialIK]

        drake_tag = 'drake-20220922'
        super().__init__(
            notebook_ipynb_list=notebook_ipynb_list,
            test_cases_list=test_cases_list,
            drake_tag=drake_tag)

class ProblemSet3(ProblemSetBase):

    def __init__(self):
        notebook_ipynb_list = [
            '/autograder/submission/bunny_icp.ipynb',
            '/autograder/submission/ransac.ipynb']
        from manipulation.exercises.pose.test_icp \
            import TestICP
        from manipulation.exercises.pose.test_ransac \
            import TestRANSAC
        test_cases_list = [TestICP,
                           TestRANSAC]
        drake_tag = 'drake-20220822'

        super().__init__(
            notebook_ipynb_list=notebook_ipynb_list,
            test_cases_list=test_cases_list,
            drake_tag=drake_tag)

class ProblemSet5(ProblemSetBase):

    def __init__(self):
        notebook_ipynb_list = [
            '/autograder/submission/normal_estimation_depth.ipynb',
            '/autograder/submission/analytic_antipodal_grasps.ipynb',
            '/autograder/submission/grasp_candidate.ipynb']
        from manipulation.exercises.clutter.test_normal \
            import TestNormal
        from manipulation.exercises.clutter.test_analytic_grasp \
            import TestAnalyticGrasp
        from manipulation.exercises.clutter.test_grasp_candidate \
            import TestGraspCandidate
        test_cases_list = [TestNormal,
                           TestAnalyticGrasp,
                           TestGraspCandidate]
        drake_tag = 'drake-20220822'

        super().__init__(
            notebook_ipynb_list=notebook_ipynb_list,
            test_cases_list=test_cases_list,
            drake_tag=drake_tag)

class ProblemSet6(ProblemSetBase):

    def __init__(self):
        notebook_ipynb_list = [
            '/autograder/submission/label_generation.ipynb',
            '/autograder/submission/segmentation_and_grasp.ipynb']
        from manipulation.exercises.segmentation.test_mask \
            import TestMask
        from manipulation.exercises.segmentation.test_segmentation_and_grasp \
            import TestSegmentationAndGrasp
        test_cases_list = [TestMask,
                           TestSegmentationAndGrasp]
        drake_tag = 'drake-20220822'

        super().__init__(
            notebook_ipynb_list=notebook_ipynb_list,
            test_cases_list=test_cases_list,
            drake_tag=drake_tag)

class ProblemSet6a(ProblemSetBase):

    def __init__(self):
        notebook_ipynb_list = [
            '/autograder/submission/label_generation.ipynb']
        from manipulation.exercises.segmentation.test_mask \
            import TestMask
        test_cases_list = [TestMask]
        drake_tag = 'drake-20220822'

        super().__init__(
            notebook_ipynb_list=notebook_ipynb_list,
            test_cases_list=test_cases_list,
            drake_tag=drake_tag)

class ProblemSet7(ProblemSetBase):

    def __init__(self):
        notebook_ipynb_list = [ 
            '/autograder/submission/hybrid_force_position.ipynb']
        from manipulation.exercises.force.test_hybrid \
            import TestHybrid
        test_cases_list = [TestHybrid]
        drake_tag = 'drake-20220822'

        super().__init__(
            notebook_ipynb_list=notebook_ipynb_list,
            test_cases_list=test_cases_list,
            drake_tag=drake_tag)

class ProblemSet8(ProblemSetBase):

    def __init__(self):
        notebook_ipynb_list = [
            '/autograder/submission/door_opening.ipynb',
            '/autograder/submission/rrt_planning.ipynb',
            '/autograder/submission/taskspace_iris.ipynb']
        from manipulation.exercises.trajectories.test_door_opening \
            import TestDoorOpening
        from manipulation.exercises.trajectories.test_rrt_planning \
            import TestRRT
        from manipulation.exercises.trajectories.test_taskspace_iris \
            import TestTaskspaceIRIS
        test_cases_list = [TestDoorOpening,
                           TestRRT,
                           TestTaskspaceIRIS]
        drake_tag = 'drake-20220822'

        super().__init__(
            notebook_ipynb_list=notebook_ipynb_list,
            test_cases_list=test_cases_list,
            drake_tag=drake_tag)        

class ProblemSet9(ProblemSetBase):

    def __init__(self):
        notebook_ipynb_list = [
            '/autograder/submission/stochastic_optimization.ipynb',
            '/autograder/submission/policy_gradient.ipynb']
        from manipulation.exercises.rl.test_stochastic_optimization \
            import TestStochasticOptimization
        from manipulation.exercises.rl.test_vpg \
            import TestVPG
        test_cases_list = [TestStochasticOptimization,
                           TestVPG]
        drake_tag = 'drake-20220822'

        super().__init__(
            notebook_ipynb_list=notebook_ipynb_list,
            test_cases_list=test_cases_list,
            drake_tag=drake_tag)        

def current_problem_set():
    return ProblemSet8()

if __name__ == "__main__":
    pset = current_problem_set()
    pset.grade_problem_set()
