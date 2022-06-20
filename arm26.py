import opensim as osim


class ARM26:
    def __init__(self, path):
        self.model = osim.Model(path)
        self.model.initSystem()

    def inverse_dynamics(self, path):
        inverse_d = osim.InverseDynamicsTool()
        inverse_d.setCoordinatesFileName(path)
        inverse_d.setModel(self.model)
        inverse_d.setResultsDir('./results')

        inverse_d.run()

    def computed_muscle_control(self, path):
        cmc = osim.CMCTool()
        cmc.setTaskSetFileName('./Arm26/ComputedMuscleControl/arm26_ComputedMuscleControl_Tasks.xml')
        cmc.setDesiredKinematicsFileName(path)
        cmc.setModel(self.model)
        cmc.setResultsDir('./results')

        cmc.run()


if __name__ == '__main__':
    model = ARM26('./Arm26/arm26.osim')

    path_inverse_kinematics_mot = './Arm26/OutputReference/InverseKinematics/arm26_InverseKinematics.mot'
    model.inverse_dynamics(path_inverse_kinematics_mot)
    model.computed_muscle_control(path_inverse_kinematics_mot)