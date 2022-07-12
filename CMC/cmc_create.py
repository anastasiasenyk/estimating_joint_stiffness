def create_xml_file(file_path):
    with open('coordinates_name.txt', 'r') as file:
        file = file.read().split('\n\n')

        cmc_task_xml = """<?xml version="1.0" encoding="UTF-8"?>
<OpenSimDocument Version="20302">
    <CMC_TaskSet name="arm_02_2021">
    <objects>
"""
    for joint in file:
        lines = joint.split('\n')
        for index, coordinate in enumerate(lines[1:]):
            if coordinate == '/':
                continue
            if index == 0:
                numbers = 'true false false'
            elif index == 1:
                numbers = 'false true false'
            else:
                numbers = 'false false †rue'

            task_bool = 'true'
            cmc_task_xml += f"""
		<CMC_Joint name="{coordinate}"> 
				<on> {task_bool} </on>
				<weight>       1.00000000    </weight>
			    <active> {numbers} </active>
				<kp>     100.00000000    </kp>
				<kv>      20.00000000      </kv>
				<ka>       1.00000000    </ka>
			    <coordinate> {coordinate} </coordinate>
				<limit>       0.00000000 </limit>
		</CMC_Joint>"""

    cmc_task_xml += """
    </objects>
		<groups/>
	</CMC_TaskSet>
</OpenSimDocument>
"""
    with open(file_path, 'w') as f:
        f.write(cmc_task_xml)


create_xml_file('full_arm_CMC_Tasks.xml')
