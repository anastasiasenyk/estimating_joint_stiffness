from scipy.spatial.transform import Rotation as R
import numpy as np
import pandas as pd


def euler_rotate(path):
    data = np.genfromtxt(path, delimiter=',', skip_header=True)

    shoulder_data = data[:,0:3]
    elbow_data = np.reshape(data[:,4], (-1, 1))
    elbow_data = np.append(elbow_data, np.zeros([len(elbow_data), 2]), 1)
    wrist_data = data[:,4:-1]

    r1 = R.from_euler("z", 90, degrees=False)
    T1 = np.array(r1.as_matrix())
    r2 = R.from_euler("x", 90, degrees=False)
    T2 = np.array(r2.as_matrix())

    T_total = T1 * T2

    tr_shoulder_data = np.matmul(shoulder_data, T_total)
    tr_elbow_data = np.reshape(np.matmul(elbow_data, T_total)[:,0], (-1, 1))
    tr_wrist_data = np.matmul(wrist_data, T_total)

    tr_data = np.append(tr_shoulder_data, tr_elbow_data, 1)
    tr_data = np.append(tr_data, tr_wrist_data, 1)
    tr_data = pd.DataFrame(tr_data)

    # column names
    tr_data.columns = ['ra_sh_e_f', 'ra_sh_ad_ab', 'ra_sh_ext_int',
               'ra_el_e_f', 'ra_wr_e_f', 'ra_wr_s_p', 'ra_wr_ad_ab']

    # create a new file name
    if len(path.split('/')) != 1:
        path = path.split('/')
        new_file = '/'.join(path[:-1] + ['tr_'+ path[-1]])
    else:
        new_file = 'tr_' + path

    # save the dataframe as a csv file
    tr_data.to_csv(new_file, index=False)


def file_format_change(name_file, format):
    """csv into .sto or .mot"""
    assert format in ['mot', 'sto']
    to_file = 'data/' + name_file.split('/')[-1].split('.')[0] + '.' + format

    with open(to_file, 'w') as file:
        df = pd.read_csv(name_file)

        # header
        file.write('Coordinates\nversion=1\n'
                   f'nRows={df.shape[0]}\nnColumns={len(df.columns) + 1}\n'
                   'inDegrees=no\n')
        if format == 'mot':
            file.write('\nUnits are S.I. units (second, meters, Newtons, ...)\n'
                       'Angles are in radians.\n\n')
        file.write('endheader\n')

        # column names
        columns = ['time']
        for col in df.columns:
            columns.append(col)

        # write a line with column names
        if format == 'mot':
            file.write('\t'.join(['time', 'ra_sh_e_f', 'ra_sh_ad_ab', 'ra_sh_ext_int',
                                  'ra_el_e_f', 'ra_wr_e_f', 'ra_wr_s_p', 'ra_wr_ad_ab']))
        else:
            file.write('\t'.join(columns))
        file.write('\n')

        # body
        for index, row in df.iterrows():
            # time
            if format == 'mot':
                line = [f'{(index*(1/490)):.8f}']
            else:
                line = [f'{(index*(1/1000)):.8f}']

            # data columns
            for col in columns[1:]:
                number = f'{row[col]:.8f}'
                if number[0] != '-':
                    number = ' ' + number
                line.append(number)
            file.write('      ')
            file.write('	     '.join(line))
            file.write('\n')


formats = ['mot', 'sto']
# euler_rotate('./data_csv/euler.csv')
# file_format_change('./data_csv/tr_euler.csv', formats[0])
file_format_change('./data_csv/euler.csv', formats[0])
