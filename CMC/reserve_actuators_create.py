def create_xml_file(data, path):
    with open(data, 'r') as file:
        file = file.read().split('\n\n')

        cmc_task_xml = """<?xml version="1.0" encoding="UTF-8"?>
<OpenSimDocument Version="20302">
	<ForceSet name="arm_02_2021">
		<defaults/>
		<objects>
"""
    for joint in file:
        lines = joint.split('\n')
        for index, coordinate in enumerate(lines[2:]):
            if coordinate == '/':
                continue
            cmc_task_xml += f"""
		    <CoordinateActuator name="{coordinate}_reserve">
				<isDisabled> false </isDisabled>
				<min_control> -infinity </min_control>
				<max_control> infinity </max_control>
				<coordinate> {coordinate} </coordinate>
				<optimal_force>    1.00000000 </optimal_force>
			</CoordinateActuator>
"""

    cmc_task_xml += """
    </objects>
		<groups/>
	</ForceSet>
</OpenSimDocument>
"""
    with open(path, 'w') as f:
        f.write(cmc_task_xml)


# create_xml_file('full_arm_Reserve_Actuators.xml')
create_xml_file('subluxation_coordinate_name.txt', '../Subluxation/subluxation_arm_Reserve_Actuators.xml')

