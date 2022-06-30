import pandas as pd
import csv


def rewrite(from_file, format):
    """InverseKinematics.mot"""
    assert format in formats
    to_file = 'data/' + from_file.split('/')[1].split('.')[0] + '.' + format

    with open(to_file, 'w') as file:
        df = pd.read_csv(from_file)
        ncols = str(int(df.columns[-1].split(' ')[-1]) + 1)
        nrows = df.shape[0]

        # header
        file.write('Coordinates\nversion=1\n'
                   f'nRows={nrows}\nnColumns={ncols}\n'
                   'inDegrees=yes\n')
        if format == 'mot':
            file.write('\nUnits are S.I. units (second, meters, Newtons, ...)\n'
                       'Angles are in degrees.\n\n')
        file.write('endheader\n')

        columns = ['time']
        for col in df.columns[:-1]:
            columns.append(col)
        file.write('\t'.join(columns))
        file.write('\n')

        # body
        for index, row in df.iterrows():
            line = [f'{(1000 * index * 0.00000001):.8f}']
            for col in columns[1:]:
                number = f'{row[col]:.8f}'
                if number[0] != '-':
                    number = ' ' + number
                line.append(number)
            file.write('      ')
            file.write('	     '.join(line))
            file.write('\n')


formats = ['mot', 'sto']
rewrite('data_csv/euler.csv', formats[0])
rewrite('data_csv/emg.csv', formats[1])
