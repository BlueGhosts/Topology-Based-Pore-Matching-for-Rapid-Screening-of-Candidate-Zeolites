
# python SplitAdo V1.0
# by wangjiaze on 2022-May-14

import os

def SplitAdo(adoFilepath, outDirpath):
    name_fileLines = {}
    outFilepaths = []
    with open(adoFilepath) as file:
        lines = file.readlines()
    i = 0
    count = 1
    while i < len(lines):
        while '##' not in lines[i]:
            i+=1
        if '##' in lines[i]:
            fileLines = []
            name = lines[i+1].strip().split(':')[-1].replace('\\', '-').replace('/', '-')
            fileLines.append(lines[i])
            fileLines.append(lines[i+1])
            fileLines.append(lines[i+2])
            i+=3
            print("\r%s : %s           "%(count, name), end = ' ')
            count += 1
			# print(name)
            while i < len(lines) and '#' not in lines[i]:
                if 'Elapsed time' in lines[i]:
                    i += 1
                    continue
                fileLines.append(lines[i])
                i += 1
        name_fileLines[name] = fileLines

    for name, fileLines in name_fileLines.items():
        outFilepath = os.path.abspath("%s/%s.ado"%(outDirpath, name)).replace('\\', '/')
        with open(outFilepath, 'w') as file:
            for line in fileLines:
                file.write(line)
        outFilepaths.append(outFilepath)

    return outFilepaths

if __name__ == "__main__":
    print("####################")
    print("       SplitAdo V1.0")
    print("         2022-May-14")
    print("        by wangjiaze")
    print("####################")
    print()

    
    #filepath = 'exampleAdo.ado'
    #outDir = 'Output'
    import sys
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        outDir = sys.argv[2]
        SplitAdo(filepath, outDir)
    else:
        filepath = input('Input Ado File Path:\n')
        outDir = input('Output Folder Path:\n')
        SplitAdo(filepath, outDir)
        input('Press any key to continue.')


