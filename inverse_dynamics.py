import opensim as osim
import numpy as np
import sys

path_arm26 = 'Arm26/arm26.osim'
path_inverse_kinematics_mot = 'Arm26/OutputReference/InverseKinematics/arm26_InverseKinematics.mot'
path_write_results = 'results/armmodel_1_0.osim'
path_dir_write_results = 'results'
path_inverse_dyn_setup = 'Arm26/OutputReference/ForwardDynamics/arm26_Setup_Forward.xml'


class ARM26:
    def __init__(self, path):
        self.model = osim.Model(path)
        self.inverse_d = None
        if not running_as_test:
            self.model.setUseVisualizer(True)

    def inverse_dynamics(self, path):
        """
        inverse dynamics
        use: path_to_file.mot
        """
        print('____________________________________')

        "initialisation for osim.InverseDynamicsTool()"
        self.inverse_d = osim.InverseDynamicsTool(path_arm26, True)
        self.inverse_d.setName('InverseDynMod')
        # self.inverse_d.setModelFileName(path_arm26)
        self.inverse_d.setModel(self.model)
        self.inverse_d.setStartTime(0.0)
        self.inverse_d.setEndTime(1.0)
        self.inverse_d.setResultsDir('../results/')
        self.inverse_d.setOutputGenForceFileName('inverse_dynamics.sto')
        # self.inverse_d.setReferences(path_inverse_dyn_setup)
        # self.inverse_d.setCoordinatesFileName(path)

        "write data from file to osim.Storage()"
        sto = osim.Storage()
        motion_array = self.read_file(11, path)
        for item in motion_array:
            row = osim.ArrayDouble()
            row.appendVector(osim.Vector([float(item[1]), float(item[2])]))
            sto.append(float(item[0]), row)

            # new_array = osim.Storage()
            # new_array.append(float(item[0]), row)
            # self.inverse_d.setCoordinateValues(new_array)

        sto.printToXML('results/new_storage.xml')  # save storage
        self.inverse_d.setCoordinateValues(sto)   # place the storage into osim.InverseDynamicsTool()
        # self.inverse_d.setCoordinatesFileName('results/new_storage.xml')
        self.inverse_d.setCoordinatesFileName(path)
        self.inverse_d.run()  # run inverse dynamics (file.sto will be created and visualisation (should) starts)

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
    model.inverse_dynamics(path_inverse_kinematics_mot)
    # model.run()
    # model.save_to_file(path_write_results)
