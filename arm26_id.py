import opensim as osim
path_inverse_kinematics_mot = './Arm26/OutputReference/InverseKinematics/arm26_InverseKinematics.mot'


def inverse_dynamics():
    model = osim.Model('./Arm26/arm26.osim')
    model.initSystem()

    inverse_d = osim.InverseDynamicsTool(path_inverse_kinematics_mot, True)
    inverse_d.setModel(model)
    inverse_d.setResultsDir('../results')

    inverse_d.run()


if __name__ == '__main__':
    inverse_dynamics()



path_inverse_dynamics_setup = './Arm26/OutputReference/ForwardDynamics/arm26_Setup_Forward.xml'