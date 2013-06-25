#Tool to organize music into major category folders:
# 1)music-rap: rap, hiphop, R&B
# 2)music-classical: classical music
# 3)music-dance: fast electronic, trance, house, etc
# 3)music: everything else

import os
import sys
import eyed3
import logging
import re
import pickle
from pprint import pprint

#load genre information for moving folders to correct subfolders
def loadGenre(genreFileName, genreDirName, genreInfo):
    loadSuccess = False
    genreFile = open(genreFileName)
    try:
        genres = genreFile.read().lower().splitlines()
        genreNames = {}
        #genreNames[genreDirName] = True
        for ii in genres:
            genreNames[ii] = True
        genreInfo[genreDirName] = genreNames
        print (genreFileName + ": loaded successfully")
        loadSuccess = True
    except Exception, err:
        print ("exception while reading genrefile: %s\n", err)
        loadSuccess = False
    finally:
        genreFile.close()
        return loadSuccess

#print usage instructions. invoked on incorrect input params    
def usageErrorMsg():
    print("Usage: python musicfolders.py [musicsourcedir] [genre-[name1].txt] [genre-[name2].txt] etc..")
    print("       Will create directories [name1], [name2], if they DNE")
    print("       Will move all artist folders from directory [musicsource] to ")
    print("       directory [name1] that have music whose genres basically match")
    print("       a string in the genre-[name].txt file.")


#verify musicdir and genre text files exist
def verifyInputs(genreDict):
    if (len(sys.argv) < 2):
        return (False,"please specify root music directory")
    elif (not(os.path.isdir(sys.argv[1]))):
        return (False,"music directory: [%s] is not valid" % sys.argv[1])
    for ii in range(2, len(sys.argv)):
        if (not(os.path.isfile(sys.argv[ii]))):
            return (False,"genre file: [%s] is not a valid file" % sys.argv[ii])
        else:
            genreFileName = sys.argv[ii]     
            print(genreFileName)
            matchObj = re.search("genre-(.+)\.txt", genreFileName)
            if (matchObj == None):
                return (False, "genre file: [%s] needs to be formatted as genre-[name].txt" % genreFileName)
            genreDirName = matchObj.group(1)        
            print (genreDirName + " " + genreFileName)
            if (not(loadGenre(genreFileName, genreDirName, genreDict))):
                return (False, "loading genre file: [%s] failed" % genreFileName)
    return (True,"")
        

def loadGenreInfo(musicdir, genreToDir, genreFolders):
    try:
        musicdirs = os.listdir(musicdir)
    except Exception, err:
        print ("exception while listing music dir: %s\n", err)
        return;

    for ii in musicdirs:
        #print (ii)
        dirpath = os.path.join(musicdir,ii)
        if (os.path.isdir(dirpath)):
            mp3list = os.listdir(dirpath)
            dirGenreDict = {} #mapping from genre to count
            for jj in mp3list:
                mp3filename, mp3fileext = os.path.splitext(jj);
                if (mp3fileext != ".mp3"):
                    print ("non-mp3 file: " + mp3fileext);
                else: 
                    try:
                        audiofile = eyed3.load(os.path.join(dirpath,jj))
                        if (isinstance(audiofile.tag.genre, eyed3.id3.Genre)):
                            #print (audiofile.tag.genre.name + ": " +
                            #repr(audiofile.tag.genre.id))
                            genres = audiofile.tag.genre.name.replace('/',';').split(';')
                            for genre in genres:
                                genre = genre.lower().strip().encode("ascii")
                                if (dirGenreDict.get(genre) != None):
                                    dirGenreDict[genre] += 1
                                else:
                                    dirGenreDict[genre] = 1
                    except Exception, err:
                        print ("exception while loading [%s]: %s\n", jj, err)
                    pass

            genrelist = sorted(dirGenreDict, key=dirGenreDict.get, reverse=True)
            #pprint(dirGenreDict)
            #pprint(genrelist)
            if (len(genrelist) != 0 and genreToDir.get(genrelist[0]) != None):
                print "%s: %d" % (genrelist[0], dirGenreDict[genrelist[0]])
                genreFolders[genreToDir[genrelist[0]]][ii] = genrelist[0] + " 1st"
            #elif (len(genrelist) >= 2 and genreToDir.get(genrelist[1]) != None):
            #    print "%s: %d" % (genrelist[1], dirGenreDict[genrelist[1]])
            #    genreFolders[genreToDir[genrelist[1]]][ii] = genrelist[1] + " - " + genrelist[0]
        else:
            print ("nonDIR:" + ii)
    print("done iterating over songs")
    

def moveToDir(genreFolder, genreFolders):
    pass

def moveToGenreDirs(genreFolders):
    print ("moving:")
    for genreFolder in genreFolders:
        for dirName in genreFolders[genreFolder]:
            print ("  "+dirName)
        print ("To Dir: "+ genreFolder)

        confirmMove = '!'
        while (confirmMove != 'y' and confirmMove != 'n'):
            confirmMove = raw_input("Go Ahead? (y or n): ")

        if (confirmMove == 'y'):
            moveToDir(genreFolder, genreFolders[genreFolder])
        
    print ("Done.")

#main - entry point
def main():
    genreDict = {}
    isValid,errMsg = verifyInputs(genreDict)
    if (not(isValid)):
        print ("Error: " + errMsg)
        usageErrorMsg()
        return 1
    else:
        genreToDir = {}
        genreFolders = {}
        for genreName in genreDict:
            genreFolders[genreName] = {}
            for ii in genreDict[genreName]:
                genreToDir[ii] = genreName

        #turn off eyeD3 warnings
        log = logging.getLogger("eyed3.id3")
        log.setLevel(logging.ERROR)
        pprint(genreToDir)
    
        loadGenreInfo(sys.argv[1], genreToDir, genreFolders)

        pprint (genreDict, indent=2)
        pprint (genreFolders, indent=2)

        with open('genreDict.pickle', 'wb') as pickleFile:
            pickle.dump(genreDict, pickleFile)
        
        moveToGenreDirs(genreFolders)

        return 0

if (__name__ == '__main__'):
    main()
