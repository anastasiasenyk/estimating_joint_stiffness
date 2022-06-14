import opensim as osim
import sys

path_arm26 = 'Arm26/arm26.osim'
path_ik_mot = 'Arm26/OutputReference/InverseKinematics/arm26_InverseKinematics.mot'
path_write_results = 'results/armmodel_1_0.osim'


class ARM26:
    def __init__(self, path):
        self.model = osim.Model(path)

        self.inverse_d = osim.InverseDynamicsTool()
        if not running_as_test:
            self.model.setUseVisualizer(True)

    def inverse_dynamics(self, path):
        print('____________________________________')
        self.inverse_d.setName('InverseDynMod')
        self.inverse_d.setModelFileName(path)
        self.inverse_d.setModel(self.model)
        self.inverse_d.setOutputGenForceFileName(path)
        self.inverse_d.setStartTime(0.0)
        self.inverse_d.setEndTime(5.0)

        print(self.inverse_d.setReferences('Arm26/OutputReference/ForwardDynamics/arm26_Setup_Forward.xml'))

        self.inverse_d.setCoordinatesFileName(path)

        # inv_dyn.setCoordinateValues()

        # storage = osim.Storage()
        # storage.set
        # storage.printToXML('results/ll0.xml')
        # self.model.printControlStorage('results/ll1.xml')
        # inv_dyn.setResultsDir('results')
        # self.model.printControlStorage('results/ll2.xml')
        # # print(inv_dyn.setCoordinateValues('results/ll1.xml'))
        #
        # inv_dyn.set_results_directory('results')

    def run(self):
        """Simulate"""
        self.inverse_d.run()
        state = self.model.initSystem()
        self.model.equilibrateMuscles(state)
        manager = osim.Manager(self.model)
        state.setTime(0)
        manager.initialize(state)
        manager.integrate(10.0)

    def save_to_file(self, path):
        """Print/save model file"""
        self.model.printToXML(path)


if __name__ == '__main__':
    running_as_test = 'unittest' in str().join(sys.argv)
    model = ARM26(path_arm26)
    model.inverse_dynamics(path_ik_mot)
    model.run()

    model.save_to_file(path_write_results)
