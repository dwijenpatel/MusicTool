import os
import sys
import json

def moveToDir(genreFolder, genreFolders):
    for artistDir in genreFolders:
        (artistPath, artistDirName) = os.path.split(artistDir)
        newPath = os.path.join(genreFolder,artistDirName)
        os.rename(artistDir, newPath)

def moveToGenreDirs(genreFolders,rootDir):
    for genreFolder in genreFolders:

        print ("moving following to genre folder [%s]" % genreFolder)
        for artistDir in genreFolders[genreFolder]:
            print ("  "+artistDir)

        confirmMove = '!'
        while (confirmMove != 'y' and confirmMove != 'n'):
            confirmMove = raw_input("Go Ahead? (y or n): ")

        if (confirmMove == 'y'):
            try:
                genreDir = os.path.join(rootDir,genreFolder)
                if (not(os.path.isdir(genreDir))):
                    os.mkdir(genreDir)

                moveToDir(genreDir, genreFolders[genreFolder])

            except Exception, err:
                print("movetoDir failed. Reason: %s" % err)

    print ("Done.")


def verifyInputs():
    if (len(sys.argv) < 2):
        return (False,"please specify json file with genre move info",None)
    elif (len(sys.argv) < 3):
        return (False,"please specify root dir location for genre folders",None)
    elif (not(os.path.isfile(sys.argv[1]))):
        return (False,"json file: [%s] is not valid" % sys.argv[1],None)
    elif (not(os.path.isdir(sys.argv[2]))):
        return (False,"root dir location [%s] is not valid" % sys.argv[2],None)

    #load json file
    try:
        with open(sys.argv[1], 'r') as jsonFile:
            genreFolders = json.load(jsonFile)
            return (True,"",genreFolders)

    except Exception, err:
        return (False,"error loading json file: %s" % err,{})        


#main - entry point
def main():
    #input validation
    isValid,errMsg,genreFolders = verifyInputs()
    if (not(isValid)):
        print("Error: "+ errMsg)
        return 1

    moveToGenreDirs(genreFolders,sys.argv[2])


if (__name__ == '__main__'):
    main()


