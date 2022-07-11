"""
inverse dynamics
computed muscle controls
forward dynamics
"""
import opensim as osim


class ARM26:
    def __init__(self, path):
        self.model = osim.Model(path)
        self.state = self.model.initSystem()

    def inverse_dynamics(self, path):
        inverse_d = osim.InverseDynamicsTool()
        inverse_d.setCoordinatesFileName(path)
        inverse_d.setModel(self.model)
        inverse_d.setResultsDir('./results')

        inverse_d.run()

    def computed_muscle_control(self, path):
        cmc = osim.CMCTool()
        cmc.setTaskSetFileName('CMCdir/full_arm_CMC_Tasks.xml')
        cmc.setDesiredKinematicsFileName(path)
        cmc.setModel(self.model)
        cmc.setResultsDir('./results')

        cmc.run()

    def forward_dynamics(self, path):
        forward_d = osim.ForwardTool()
        forward_d.setControlsFileName(path)
        forward_d.setModel(self.model)
        forward_d.setResultsDir('./results')

        forward_d.run()

    def run(self):
        self.model.equilibrateMuscles(self.state)
        manager = osim.Manager(self.model)
        self.state.setTime(0)
        manager.initialize(self.state)
        manager.integrate(1.0)


if __name__ == '__main__':
    print('-')
    model = ARM26('Geometry/full_arm_model_osv5.osim')
    print('-')

    # model.inverse_dynamics('data/euler.mot')

    moments_file = 'results/inverse_dynamics.sto'
    motion_file = 'data/euler.mot'

    model.computed_muscle_control(motion_file)

    # model.forward_dynamics('data/emg.sto')
