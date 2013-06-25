
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
