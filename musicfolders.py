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
import json

#print usage instructions. 
def usageErrorMsg():
    print("Usage: python musicfolders.py [musicsourcedir] [genre-info.json]")
    print("       Scans [musicsourcedir] for artist folders")
    print("       If artist folder's song's most common id3 genre tag matches genre-info.json,")
    print("       adds artist folder to genreFolder.json output.")


#verify musicdir and genre json file exist
def verifyInputs(genreConfig):
    if (len(sys.argv) < 2):
        return (False,"please specify root music directory")
        
    if (not(os.path.isdir(sys.argv[1]))):
        return (False,"music directory: [%s] is not valid" % sys.argv[1])
        
    if (not(os.path.isfile(sys.argv[2]))):
        return (False,"json file: [%s] is not valid" % sys.argv[2])

    #load json file
    try:
        with open(sys.argv[2], 'r') as jsonFile:
            genreConfig = json.load(jsonFile)
    except Exception, err:
        return (False,"error loading json file: %s" % err)

    return (True,"")        

#find most common genre tag from mp3s in artistDirPath
def getArtistGenre(artistDirPath):
    mp3list = os.listdir(artistDirPath)
    genreToCount = {} #map from genre to number of appearances
    for jj in mp3list:
        mp3filename, mp3fileext = os.path.splitext(jj);
        if (mp3fileext != ".mp3"):
            print ("non-mp3 file: " + mp3fileext);
        else: 
            try:
                audiofile = eyed3.load(os.path.join(artistDirPath,jj))
                if (isinstance(audiofile.tag.genre, eyed3.id3.Genre)):
                    genres = audiofile.tag.genre.name.replace('/',';').split(';')
                    for genre in genres:
                        genre = genre.lower().strip().encode("ascii")
                        if (genreToCount.get(genre) != None):
                            genreToCount[genre] += 1
                        else:
                            genreToCount[genre] = 1

            except Exception, err:
                print ("exception while loading file [%s]: %s\n", jj, err)

    if (genreToCount):
        genrelist = sorted(genreToCount, key=genreToCount.get, reverse=True)
        return (genrelist[0])
    else:
        return (None)



#iterate over artist folders in musicdir
#if artist's dominant genre matches genreLookup, add to genreFolders
#also cache dominant genre info
def loadGenreInfo(musicdir, genreLookup, genreCache):
    returnMe = {}
    try:
        musicdirs = os.listdir(musicdir)
    except Exception, err:
        print ("exception while listing music dir: %s\n", err)
        return;

    for ii in musicdirs:
        #print (ii)
        dirpath = os.path.join(musicdir,ii)
        if (os.path.isdir(dirpath)):
            if (genreCache.get(dirpath) != None): #cache-hit!
                thisGenre = genreCache[dirpath]
            else:
                thisGenre = getArtistGenre(dirpath)
                genreCache[dirpath] = thisGenre #add to cache

            if (genreLookup.get(thisGenre) != None): #genre match!
                returnMe[genreLookup[thisGenre]].append(dirpath) #add to results
        else:
            print ("nonDIR:" + ii)
    print("done iterating over songs")
    return (returnMe)

def loadGenreCache(cacheFileName):
    with open(cacheFileName,'r') as f:
       return (json.load(f))

#main - entry point
def main():
    genreConfig = {}

    #input validation
    isValid,errMsg = verifyInputs(genreConfig)
    if (not(isValid)):
        print ("Error: " + errMsg)
        usageErrorMsg()
        return 1

    genreLookup = {} #maps genre tag names to a genre folder

    #init genre data structs
    for genreName in genreConfig:
        for ii in genreConfig[genreName]:
            genreLookup[ii] = genreName

    #load genre info cache
    cacheFileName = os.path.join(sys.argv[1],"musicGenreCache.json")
    if (os.path.isfile(cacheFileName)):
        genreCache = loadGenreCache(cacheFileName)
    else:
        print("no genre cache file found")

    #turn off eyeD3 warnings
    log = logging.getLogger("eyed3.id3")
    log.setLevel(logging.ERROR)

    #iterate over music directories and load info
    genreFolders = loadGenreInfo(sys.argv[1], genreLookup, genreCache)
    
    #print results
    pprint (genreFolders, indent=2)

    #output results to json file
    with open('GenreFolders.json','w') as f:
        json.dump(genreFolders, f, indent=2)

    #output genre cache to json file
    with open(cacheFileName, 'w') as f:
        json.dump(genreCache, f, indent=2)        

    return 0


if (__name__ == '__main__'):
    main()
