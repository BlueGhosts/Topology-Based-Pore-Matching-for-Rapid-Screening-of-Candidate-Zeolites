# python SplitCgd V1.0
# by wangjiaze on 2022-May-14

import re
import os

def SplitCgd(cgdFilepath, outDirpath):
    with open(cgdFilepath) as file:
        contents = file.read()

    name_tiling = {}
    tilings = contents.split('\n\n')
    for tiling in tilings:
        if tiling:
            lines = tiling.split('\n')
            name = re.search('NAME "(.*?);', lines[1]).group(1).replace('\\', '-').replace('/', '-')
            name_tiling[name] = tiling

    outFilepaths = []
    for name, fileLines in name_tiling.items():
        print(name)
        outFilepath = os.path.abspath("%s/%s.cgd" % (outDirpath, name)).replace('\\', '/')
        with open(outFilepath, 'w') as file:
            for line in fileLines:
                file.write(line)
        outFilepaths.append(outFilepath)
    return outFilepaths

if __name__ == "__main__":
    print("####################")
    print("       SplitCgd V1.0")
    print("         2022-May-14")
    print("        by wangjiaze")
    print("####################")
    print()

    # filepath = 'example.cgd'
    # outDir = 'Output'
    import sys

    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        outDir = sys.argv[2]
        SplitCgd(filepath, outDir)
    else:
        filepath = input('Input Cgd File Path:\n')
        outDir = input('Output Folder Path:\n')
        SplitCgd(filepath, outDir)
        input('Press any key to continue.')
