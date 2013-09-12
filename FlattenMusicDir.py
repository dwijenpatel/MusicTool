import os
import pprint

def flattenMusic(curDir, moveToDir):
    fileList = os.listdir(curDir)
    for ii in fileList:
        #print(" "+ii)
        fullpath = os.path.join(curDir,ii)
        if (os.path.isfile(fullpath)):
            filename, fileext = os.path.splitext(ii);
            if (fileext == ".mp3"):
                try:
                    os.rename(os.path.join(curDir,ii),
                              os.path.join(moveToDir,ii))
                except Exception, err:
                    print ("move %(a)s failed. reason: %(b)s " % 
                           {"a":ii, "b":err})
        elif (os.path.isdir(fullpath)):
            print(" flattening: " + fullpath)
            flattenMusic(fullpath, moveToDir)


print(os.getcwd())

for ii in os.listdir(os.getcwd()):
    if (os.path.isdir(ii)):
        print("flattening: " + ii)
        flattenMusic(ii, os.getcwd())
