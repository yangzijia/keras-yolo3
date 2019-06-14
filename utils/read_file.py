import os

def ListFilesToTxt(dir,file,recursion):
    for root, subdirs, files in os.walk(dir):
        print(root)
        print(files)
        for name in files:
            new_txt = 'helmet/all_image/workers/aaa/%s' % name
            file.write(new_txt + "\n")
            
        if(not recursion):
            break
def Test():
    dir="helmet/all_image/workers/JPEGImages/"
    outfile="binaries.txt"

    file = open(outfile,"w")
    if not file:
        print ("cannot open the file %s for writing" % outfile)
    ListFilesToTxt(dir,file, 0)

    file.close()
Test()