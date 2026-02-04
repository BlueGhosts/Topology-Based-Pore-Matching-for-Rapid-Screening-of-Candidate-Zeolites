# python SplitCif V1.0
# by wangjiaze on 2022-May-17

import os

def SplitCif(cifFilepath, outDirpath):
    with open(cifFilepath) as file:
        contents = file.read()

    name_content = {}
    informatons = contents.split('\n\n')
    for informaton in informatons:
        if informaton:
            lines = informaton.split('\n')
            name = lines[0].split('TOPOS_')[-1].replace('/', '-')
            name_content[name] = informaton

    outFilepaths = []
    for name, fileLines in name_content.items():
        print(name)
        outFilepath = os.path.abspath("%s/%s.cif" % (outDirpath, name)).replace('\\', '/')
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

    # filepath = r'D:\Work\PoresTopology\Data\IZA\211221-IZA\Topos\PoresTopology\IZA#.cif'
    # outDir = r'D:\Work\PoresTopology\Data\IZA\211221-IZA\Topos\PoresTopology\#cif'
    import sys

    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        outDir = sys.argv[2]
        SplitCif(filepath, outDir)
    else:
        filepath = input('Input Cif File Path:\n')
        outDir = input('Output Folder Path:\n')
        SplitCif(filepath, outDir)
        input('Press any key to continue.')
