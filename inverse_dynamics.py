import opensim as osim
import numpy as np
import sys

path_arm26 = 'Arm26/arm26.osim'
path_inverse_kinematics_mot1 = 'Arm26/OutputReference/InverseKinematics/arm26_InverseKinematics.mot'
path_inverse_kinematics_mot2 = 'results/arm26_InverseKinematics.mot'
path_write_results = 'results/armmodel_1_0.osim'
path_inverse_dyn_setup = 'Arm26/OutputReference/ForwardDynamics/arm26_Setup_Forward.xml'


class ARM26:
    def __init__(self, path):
        self.model = osim.Model(path)
        self.inverse_d = osim.InverseDynamicsTool()
        if not running_as_test:
            self.model.setUseVisualizer(True)

    def inverse_dynamics(self, path):
        """
        inverse dynamics
        use: path_to_file.mot
        """
        print('____________________________________')

        # initialisation for osim.InverseDynamicsTool()
        self.inverse_d.setName('InverseDynMod')
        self.inverse_d.setModelFileName(path_arm26)
        self.inverse_d.setModel(self.model)
        self.inverse_d.setOutputGenForceFileName(path)
        self.inverse_d.setStartTime(0.0)
        self.inverse_d.setEndTime(1.0)
        self.inverse_d.setResultsDir('results')
        self.inverse_d.setReferences(path_inverse_dyn_setup)
        self.inverse_d.setCoordinatesFileName(path)

        # write data from file to osim.Storage()
        sto = osim.Storage()
        motion_array = self.read_file(11, path)
        for item in motion_array:
            row = osim.ArrayDouble()
            row.appendVector(osim.Vector([float(item[1]), float(item[2])]))
            sto.append(float(item[0]), row)

        sto.printToXML('results/new_storage.xml')  # save storage

        # place the storage into osim.InverseDynamicsTool()
        self.inverse_d.setCoordinateValues(sto)

    def read_file(self, num_invalid_lines, file_name):
        """return data from file"""
        with open(file_name, 'r') as f:
            file = f.read().split('\n')
        data = []
        for line in file[num_invalid_lines:]:
            if line != '':
                data.append([item.strip('\t').strip() for item in line.split(' ') if item!=''])

        return data

    def run(self):
        """Simulate"""
        self.inverse_d.run()  # run inverse dynamics (well, nothing happen)
        state = self.model.initSystem()
        self.model.equilibrateMuscles(state)
        manager = osim.Manager(self.model)
        state.setTime(0)
        manager.initialize(state)
        manager.integrate(1.0)

    def save_to_file(self, path):
        """Print/save model file"""
        self.model.printToXML(path)


if __name__ == '__main__':
    running_as_test = 'unittest' in str().join(sys.argv)
    model = ARM26(path_arm26)
    model.inverse_dynamics(path_inverse_kinematics_mot2)
    model.run()

    model.save_to_file(path_write_results)
