# python CalculateAveConnection V1.0
# by wangjiaze on 2025-Feb-19

import sys

def parse_dict(string):
    result = {}
    if string != "{}":
        string = string.strip("{}")
        pairs = string.split(",")
        for pair in pairs:
            key, value = pair.split(":")
            result[key.strip()] = int(value.strip())
    return result


def CalculateAveConnection(inCsvPath, outCsvPath):
    with open(inCsvPath, 'r') as f:
        lines = f.readlines()
    
    outCsvFile = open(outCsvPath, 'w')
    outCsvFile.write("Name,ConnectionNumber,AveConnection\n")
    for line in lines[1:]:
        connection_radio = {}
        line = line.strip().split(',')
        name = line[0]
        atom_mul = parse_dict(line[3].replace(';', ','))
        atom_connection = parse_dict(line[4].replace(';', ','))   

        allMul = sum(atom_mul.values())
        if allMul == 0:
            print(f'{name},0,1')
            outCsvFile.write(f'{name},0,1\n')
        for atomName in atom_mul.keys():
            mul = atom_mul[atomName]
            connection = atom_connection[atomName]
            if connection not in connection_radio.keys():
                connection_radio[connection] = 0
            connection_radio[connection] += mul / allMul
        
        for connection, radio in connection_radio.items():
            radio = round(radio, 4)
            print(f'{name}_{connection},{connection},{radio}')
            outCsvFile.write(f'{name}_{connection},{connection},{radio}\n')
    outCsvFile.close()
    

if __name__ == "__main__":
    print("##############################")
    print(" CalculateAveConnection V1.0 #")
    print("                 2025-Feb-19 #")
    print("                by wangjiaze #")
    print("##############################")
    print()

    # inCsvPath = r'P:\Project\PoreTopology\01_IZA\02_Process\03_PoreTopology\02_Cif\Table-MS-NT-DeleteNotConnection.csv'
    # outCsvPath = r'P:\Project\PoreTopology\01_IZA\02_Process\03_PoreTopology\02_Cif\Table-MS-NT-AveConnection.csv'
    import sys

    if len(sys.argv) > 1:
        inCsvPath = sys.argv[1]
        outCsvPath = sys.argv[2]
        CalculateAveConnection(inCsvPath, outCsvPath)
    else:
        inCsvPath = input('Input Csv Path:\n')
        outCsvPath = input('Output Csv Path:\n')
        CalculateAveConnection(inCsvPath, outCsvPath)
        input('Press any key to continue.')
