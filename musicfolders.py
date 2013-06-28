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
import time

#print usage instructions. 
def usageErrorMsg():
    print("Usage: python [%s] [musicsourcedir] [genre-info.json] " % sys.argv[0])
    print("       Scans [musicsourcedir] for artist folders")
    print("       If artist folder's song's most common id3 genre tag matches genre-info.json,")
    print("       adds artist folder to genreFolder.json output.")
    

#verify musicdir and genre json file exist
def verifyInputs():
    if (len(sys.argv) < 2):
        return (False,"please specify root music directory",{})
        
    if (not(os.path.isdir(sys.argv[1]))):
        return (False,"music directory: [%s] is not valid" % sys.argv[1],{})
        
    if (not(os.path.isfile(sys.argv[2]))):
        return (False,"json file: [%s] is not valid" % sys.argv[2],{})

    #load json file
    try:
        with open(sys.argv[2], 'r') as jsonFile:
            genreConfig = json.load(jsonFile)
            return (True,"",genreConfig)        

    except Exception, err:
        return (False,"error loading json file: %s" % err,{})



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
        return (genrelist[0].encode('utf-8'))
    else:
        return (None)



#iterate over artist folders in musicdir
#if artist's dominant genre matches genreLookup, add to genreFolders
#also cache dominant genre info
def loadGenreInfo(musicdir, genreConfig, genreCache):
    returnMe = {}
    try:
        musicdirs = os.listdir(musicdir)
    except Exception, err:
        print ("exception while listing music dir: %s\n", err)
        return;

    genreLookup = {} #maps genre tag names to a genre folder

    #init genre data structs
    for genreName in genreConfig:
        returnMe[genreName] = []
        for ii in genreConfig[genreName]:
        
            genreLookup[ii] = genreName
    pprint(genreLookup)
    for ii in musicdirs:
        #print (ii)
        dirpath = os.path.join(musicdir,ii)
        if (os.path.isdir(dirpath)):
            dirTime = os.path.getmtime(dirpath)
            thisGenre = None

            #check genre cache
            if (genreCache.get(dirpath) != None): #cache-hit!
                (cacheGenre, cacheTime) = genreCache[dirpath]
                if (dirTime < cacheTime): # not stale data!
                    thisGenre = cacheGenre
                    pprint(thisGenre)

            #look for genre id3 tag info
            if (thisGenre == None):
                thisGenre = getArtistGenre(dirpath)
                

            #if we have a genre tag for this artist
            if (thisGenre != None):
                genreCache[dirpath] = (thisGenre, time.time()) 
                
                if (genreLookup.get(thisGenre) != None): #genre match!
                    returnMe[genreLookup[thisGenre]].append(dirpath) #add to results
        else:
            print ("nonDIR:" + ii)
    print("done iterating over songs")
    pprint(returnMe)
    return (returnMe)

def loadGenreCache(cacheFileName):
    with open(cacheFileName,'r') as f:
       return (json.load(f))

#main - entry point
def main():
    #input validation
    isValid,errMsg,genreConfig = verifyInputs()
    if (not(isValid)):
        print ("Error: " + errMsg)
        usageErrorMsg()
        return 1

    #load genre info cache
    cacheFileName = os.path.join(sys.argv[1],"musicGenreCache.json")
    if (os.path.isfile(cacheFileName)):
        genreCache = loadGenreCache(cacheFileName)
    else:
        print("no genre cache file found")
        genreCache = {}

    #turn off eyeD3 warnings
    log = logging.getLogger("eyed3.id3")
    log.setLevel(logging.ERROR)

    #iterate over music directories and load info
    pprint(genreConfig)
    genreFolders = loadGenreInfo(sys.argv[1], genreConfig, genreCache)
    
    #print results
    pprint (genreFolders, indent=2)

    #output results to json file
    with open('GenreFolders.json','w') as f:
        json.dump(genreFolders, f, indent=2)

    #output genre cache to json file
    with open(cacheFileName, 'w') as f:
        json.dump(genreCache, f, indent=2)        

    return 0


def printGenreInfo(genreCache):
    genreBreakDown = {}
    for thisFolder in genreCache:
        (pathDir, artistFolder) = os.path.split(thisFolder)
        artistGenre = genreCache[thisFolder][0]
        if (genreBreakDown.get(artistGenre) != None):
            genreBreakDown[artistGenre] += 1
        else:
            genreBreakDown[artistGenre] = 1
        
    sortedGenres = sorted(genreBreakDown, key=genreBreakDown.get, reverse=True)
    for ii in sortedGenres:
        print(ii + " - " + repr(genreBreakDown[ii]))
        

def mainGenreInfo():

    #load genre info cache
    cacheFileName = os.path.join(sys.argv[1],"musicGenreCache.json")
    if (os.path.isfile(cacheFileName)):
        genreCache = loadGenreCache(cacheFileName)
    else:
        print("no genre cache file found")
        return 1;
    
    #print genre cache information
    pprint(genreCache)
    printGenreInfo(genreCache)
    return 0

if (__name__ == '__main__'):
    mainGenreInfo()
#    main()
