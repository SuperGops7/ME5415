import math

youngModulusActuators = 500
youngModulusStiffLayerActuators = 1500

ROBOT_POS = [-10, 0, 0]
ROBOT_ORT = [0, 0, -90]

def createScene(rootNode):
    rootNode.addObject('RequiredPlugin',
                       pluginName='SoftRobots SofaPython3')
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.AnimationLoop')  # Needed to use components [FreeMotionAnimationLoop]
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Collision.Detection.Algorithm')  # Needed to use components [BVHNarrowPhase,BruteForceBroadPhase,CollisionPipeline]
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Collision.Detection.Intersection')  # Needed to use components [LocalMinDistance]
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Collision.Geometry')  # Needed to use components [LineCollisionModel,PointCollisionModel,TriangleCollisionModel]
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Collision.Response.Contact')  # Needed to use components [CollisionResponse]
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Constraint.Lagrangian.Correction')  # Needed to use components [GenericConstraintCorrection,UncoupledConstraintCorrection]
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Constraint.Lagrangian.Solver')  # Needed to use components [GenericConstraintSolver]
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Engine.Select')  # Needed to use components [BoxROI]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.IO.Mesh')  # Needed to use components [MeshOBJLoader,MeshSTLLoader,MeshVTKLoader]
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.LinearSolver.Direct')  # Needed to use components [SparseLDLSolver]
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.LinearSolver.Iterative')  # Needed to use components [CGLinearSolver]
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Mapping.Linear')  # Needed to use components [BarycentricMapping]
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Mapping.NonLinear')  # Needed to use components [RigidMapping]
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Mass')  # Needed to use components [UniformMass]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.ODESolver.Backward')  # Needed to use components [EulerImplicitSolver]
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Setting')  # Needed to use components [BackgroundSetting]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.SolidMechanics.FEM.Elastic')  # Needed to use components [TetrahedronFEMForceField]
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.SolidMechanics.Spring')  # Needed to use components [RestShapeSpringsForceField]
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.StateContainer')  # Needed to use components [MechanicalObject]
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Topology.Container.Constant')  # Needed to use components [MeshTopology]
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Topology.Container.Dynamic')  # Needed to use components [TetrahedronSetTopologyContainer]
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Visual')  # Needed to use components [VisualStyle]  
    rootNode.addObject('RequiredPlugin', name='Sofa.GL.Component.Rendering3D')  # Needed to use components [OglModel,OglSceneFrame]

    rootNode.addObject('VisualStyle',
                       displayFlags='showVisualModels hideBehaviorModels hideCollisionModels hideBoundingCollisionModels hideForceFields showInteractionForceFields hideWireframe')
    rootNode.gravity.value = [-9810, 0, 0]
    rootNode.addObject('FreeMotionAnimationLoop')
    rootNode.addObject('GenericConstraintSolver', tolerance=1e-12, maxIterations=10000)
    # rootNode.addObject('EulerImplicitSolver', name='odesolver', rayleighStiffness=0.1, rayleighMass=0.1)
    rootNode.addObject('DefaultPipeline')
    rootNode.addObject('BruteForceBroadPhase')
    rootNode.addObject('BVHNarrowPhase')
    rootNode.addObject('DefaultContactManager', response='FrictionContactConstraint', responseParams='mu=0.6')
    rootNode.addObject('LocalMinDistance', name='Proximity', alarmDistance=5, contactDistance=1, angleCone=0.0)

    rootNode.addObject('BackgroundSetting', color=[0, 0.168627, 0.211765, 1.])
    rootNode.addObject('OglSceneFrame', style='Arrows', alignment='TopRight')


    ##########################################
    ##### Actuator
    ##########################################
    
    actuator = rootNode.addChild('Actuator 1')
    actuator.addObject('EulerImplicitSolver', name='odesolver', rayleighStiffness=0.1, rayleighMass=0.1)
    actuator.addObject('SparseLDLSolver', name='preconditioner', template="CompressedRowSparseMatrixMat3x3d")

    actuator.addObject('MeshVTKLoader', name='loader', filename='data/mesh/ActuatorCollision.vtk',
                        translation=ROBOT_POS, rotation=ROBOT_ORT)
    # actuator.addObject('MeshTopology', src='@loader', name='container')
    actuator.addObject('TetrahedronSetTopologyContainer', position='@loader.position', 
                    tetrahedra='@loader.tetrahedra', name='container')

    actuator.addObject('MechanicalObject', name='tetras', template='Vec3', 
                    showIndices=False, showIndicesScale=4e-5)
    actuator.addObject('UniformMass', totalMass=0.04)
    actuator.addObject('TriangleFEMForceField', template='Vec3', name='FEM', method='large', poissonRatio=0.3,
                        youngModulus=youngModulusActuators)
    # actuator.addObject('TetrahedronFEMForceField', template='Vec3', name='FEM', method='large', poissonRatio=0.3,
    #                     youngModulus=youngModulusActuators)

    # actuator.addObject('BoxROI', name='boxROI', box=[-10, 0, -20, 0, 30, 20], drawBoxes=True, doUpdate=True)
    # actuator.addObject('BoxROI', name='boxROISubTopo', box=[-100, 22.5, -8, -19, 28, 8], drawBoxes=True, strict=False, computeTetrahedra=False)
    # actuator.addObject('BoxROI', name='boxROISubTopo', box='0 0 0 150 -100 1', drawBoxes=True)
    # actuator.addObject('BoxROI', name='membraneROISubTopo', box='0 0 -0.1 150 -100 0.1', computeTetrahedra="false",
    #                    drawBoxes=True)
    # actuator.addObject('RestShapeSpringsForceField', points=0, stiffness=1e12,
    #                     angularStiffness=1e12)
    actuator.addObject('LinearSolverConstraintCorrection')

    ##########################################
    # Sub topology						   #
    ##########################################
    modelSubTopo = actuator.addChild('modelSubTopo')
    modelSubTopo.addObject('TriangleSetTopologyContainer', position='@loader.position',
                            triangles='@boxROISubTopo.trianglesInROI', name='containerSub')
    modelSubTopo.addObject('TriangleFEMForceField', template='Vec3d', name='FEM', method='large',
                            poissonRatio=0.4, youngModulus=youngModulusStiffLayerActuators - youngModulusActuators)
    # modelSubTopo.addObject('TetrahedronSetTopologyContainer', position='@loader.position',
    #                         tetrahedra='@boxROISubTopo.tetrahedraInROI', name='containerSub')
    # modelSubTopo.addObject('TetrahedronFEMForceField', template='Vec3', name='FEM', method='large',
    #                         poissonRatio=0.3, youngModulus=youngModulusStiffLayerActuators - youngModulusActuators)

    ##########################################
    # Constraint							 #
    ##########################################
    cavity1 = actuator.addChild('cavity1')
    cavity1.addObject('MeshSTLLoader', name='loader', filename='data/mesh/Actuator1Cavity.stl',
                        translation=ROBOT_POS, rotation=ROBOT_ORT)
    cavity1.addObject('MeshTopology', src='@loader', name='topo')
    cavity1.addObject('MechanicalObject', name='cavity1')
    cavity1.addObject('SurfacePressureConstraint', name='SurfacePressureConstraint', template='Vec3', value=0,
                        triangles='@topo.triangles', valueType='pressure')
    cavity1.addObject('BarycentricMapping', name='mapping', mapForces=False, mapMasses=False)

    cavity2 = actuator.addChild('cavity2')
    cavity2.addObject('MeshSTLLoader', name='loader', filename='data/mesh/Actuator2Cavity.stl',
                        translation=ROBOT_POS, rotation=ROBOT_ORT)
    cavity2.addObject('MeshTopology', src='@loader', name='topo')
    cavity2.addObject('MechanicalObject', name='cavity2')
    cavity2.addObject('SurfacePressureConstraint', name='SurfacePressureConstraint', template='Vec3', value=0,
                        triangles='@topo.triangles', valueType='pressure')
    cavity2.addObject('BarycentricMapping', name='mapping', mapForces=False, mapMasses=False)

    cavity3 = actuator.addChild('cavity3')
    cavity3.addObject('MeshSTLLoader', name='loader', filename='data/mesh/Actuator3Cavity.stl',
                        translation=ROBOT_POS, rotation=ROBOT_ORT)
    cavity3.addObject('MeshTopology', src='@loader', name='topo')
    cavity3.addObject('MechanicalObject', name='cavity3')
    cavity3.addObject('SurfacePressureConstraint', name='SurfacePressureConstraint', template='Vec3', value=0,
                        triangles='@topo.triangles', valueType='pressure')
    cavity3.addObject('BarycentricMapping', name='mapping', mapForces=False, mapMasses=False)
    cavity4 = actuator.addChild('cavity4')
    cavity4.addObject('MeshSTLLoader', name='loader', filename='data/mesh/Actuator4Cavity.stl',
                        translation=ROBOT_POS, rotation=ROBOT_ORT)
    cavity4.addObject('MeshTopology', src='@loader', name='topo')
    cavity4.addObject('MechanicalObject', name='cavity4')
    cavity4.addObject('SurfacePressureConstraint', name='SurfacePressureConstraint', template='Vec3', value=0,
                        triangles='@topo.triangles', valueType='pressure')
    cavity4.addObject('BarycentricMapping', name='mapping', mapForces=False, mapMasses=False)

    ##########################################
    # Collision							  #
    ##########################################

    collisionActuator = actuator.addChild('collisionActuator')
    collisionActuator.addObject('MeshSTLLoader', name='loader', filename='data/mesh/ActuatorCollision.stl',
                                translation=ROBOT_POS, rotation=ROBOT_ORT)
    collisionActuator.addObject('TriangleSetTopologyContainer', position='@loader.position', 
                                triangles='@loader.triangles', name='container_actuator')
    # collisionActuator.addObject('MeshTopology', src='@loader', name='topo')
    collisionActuator.addObject('MechanicalObject', name='collisMech', template='Vec3d')
    collisionActuator.addObject('TriangleCollisionModel', selfCollision=False)
    collisionActuator.addObject('LineCollisionModel', selfCollision=False)
    collisionActuator.addObject('PointCollisionModel', selfCollision=False)
    collisionActuator.addObject('BarycentricMapping')

    ##########################################
    ##### Visualization
    ##########################################
    modelVisu = actuator.addChild('Visu')
    modelVisu.addObject('MeshSTLLoader', name='loader', filename='data/mesh/ActuatorCollision.stl', translation=ROBOT_POS, rotation=ROBOT_ORT)
    modelVisu.addObject('OglModel', src='@loader', color=[0.7, 0.7, 0.7, 0.6], template='Vec3')
    modelVisu.addObject('BarycentricMapping')

    ##########################################
    #### Floor
    ##########################################

    planeNode = rootNode.addChild('Plane')
    planeNode.addObject('MeshOBJLoader', name='loader', filename='data/mesh/floorFlat.obj', triangulate=True,
                        rotation=[0, 0, 270], scale=10, translation=[-15, 0, 0])
    planeNode.addObject('MeshTopology', src='@loader')
    planeNode.addObject('MechanicalObject', src='@loader')
    planeNode.addObject('TriangleCollisionModel', simulated=False, moving=False)
    planeNode.addObject('LineCollisionModel', simulated=False, moving=False)
    planeNode.addObject('PointCollisionModel', simulated=False, moving=False)
    planeNode.addObject('OglModel', name='Visual', src='@loader', color=[1, 0, 0, 1])

    ## Cube to check collisions/gravity
    cube = rootNode.addChild('cube')
    cube.addObject('EulerImplicitSolver', name='odesolver')
    cube.addObject('SparseLDLSolver', name='linearSolver', template="CompressedRowSparseMatrixMat3x3d")
    cube.addObject('MechanicalObject', template='Rigid3', position=[20, 70, 70, 0, 0, 0, 1])
    cube.addObject('UniformMass', totalMass=0.001)
    cube.addObject('UncoupledConstraintCorrection')

    # collision
    cubeCollis = cube.addChild('cubeCollis')
    cubeCollis.addObject('MeshOBJLoader', name='loader', filename='data/mesh/smCube27.obj', triangulate=True,
                         scale=6)
    cubeCollis.addObject('MeshTopology', src='@loader')
    cubeCollis.addObject('MechanicalObject')
    cubeCollis.addObject('TriangleCollisionModel')
    cubeCollis.addObject('LineCollisionModel')
    cubeCollis.addObject('PointCollisionModel')
    cubeCollis.addObject('RigidMapping')

    # visualization
    cubeVisu = cube.addChild('cubeVisu')
    cubeVisu.addObject('MeshOBJLoader', name='loader', filename='data/mesh/smCube27.obj')
    cubeVisu.addObject('OglModel', name='Visual', src='@loader', color=[0.0, 0.1, 0.5], scale=6.2)
    cubeVisu.addObject('RigidMapping')
    
    rootNode.addObject(RobotController(node=rootNode))

    return rootNode

'''
===
'''

import Sofa.Core
from Sofa.constants import *
import math

class RobotController(Sofa.Core.Controller):

    def __init__(self, *a, **kw):

        Sofa.Core.Controller.__init__(self, *a, **kw)
        self.node = kw["node"]
        self.constraints = []
        self.dofs = []
        self.dofs.append(self.node.getChild('Actuator 1').getMechanicalState())
        self.constraints.append(self.node.getChild('Actuator 1').cavity2.SurfacePressureConstraint)
        self.constraints.append(self.node.getChild('Actuator 1').cavity1.SurfacePressureConstraint)
        self.constraints.append(self.node.getChild('Actuator 1').cavity3.SurfacePressureConstraint)
        self.constraints.append(self.node.getChild('Actuator 1').cavity4.SurfacePressureConstraint)

        self.state = "increase_1_3"

        return

    def onAnimateBeginEvent(self, event):
        # print("onAnimateBeginEvent")

        increment = 0.1
        pressureHighThreshold = 3.05
        pressureLowThreshold = 0.0
        MIN_PRESSURE = 0
        MAX_PRESSURE = pressureHighThreshold*1.1

        # Define the finite states
        STATE_PHASE_0 = "increase_1_3"
        STATE_PHASE_1 = "decrease_1_3"
        STATE_PHASE_2 = "increase_2_4"
        STATE_PHASE_3 = "decrease_2_4"

        if self.state == STATE_PHASE_0:
            # Phase 0: pressurize channels 1 & 3
            for i in [0, 2]:
                pressureValue = self.constraints[i].value.value[0] + increment
                if pressureValue > MAX_PRESSURE: # max pressure edge case
                    pressureValue = MAX_PRESSURE
                self.constraints[i].value = [pressureValue]
            if self.constraints[0].value.value[0] >= pressureHighThreshold and self.constraints[2].value.value[0] >= pressureHighThreshold:
                self.state = STATE_PHASE_1
        elif self.state == STATE_PHASE_1:
            # Phase 1: Depressurize channels 1 & 3
            self.constraints[0].value = self.constraints[2].value = [0.0]
            self.state = STATE_PHASE_2
        
        elif self.state == STATE_PHASE_2:
            # Phase 2: pressurize channels 2 & 4
            for i in [1, 3]:
                pressureValue = self.constraints[i].value.value[0] + increment
                if pressureValue > MAX_PRESSURE: # max pressure edge case
                    pressureValue = MAX_PRESSURE
                self.constraints[i].value = [pressureValue]
            if self.constraints[1].value.value[0] >= pressureHighThreshold and self.constraints[3].value.value[0] >= pressureHighThreshold:
                self.state = STATE_PHASE_3

        elif self.state == STATE_PHASE_3:
            # Phase 3: depressurize channels 2 & 4
            self.constraints[1].value = self.constraints[3].value = [0.0]
            self.state = STATE_PHASE_0

        # print(self.constraints[0].value.value[0])
        # print(self.state)
