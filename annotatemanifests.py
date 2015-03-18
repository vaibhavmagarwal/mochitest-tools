import os, json, shutil

#function to annotate the mochitest.ini files
def annotateManifests(files, skip):
    notfound = {}
     
    for key in files:
        baseDir = r'C:/mozilla-inbound/mozilla-inbound/'+key
        if os.path.isdir(baseDir):
            print "skipping directory: %s" % key
            notfound[key] = files[key]
            continue

        if not os.path.isfile(baseDir):
            print "NOT A FILE: %s" % key
            notfound[key] = files[key]
            continue
        
        #print baseDir
        found = False
        index = baseDir.rfind("/")
        fname = baseDir[index+1:]
        baseDir = baseDir[:index+1]
        skipif = ""
        if not os.path.exists(os.path.join(baseDir,'mochitest.ini')):
            print (key,files[key])
            notfound[key] = files[key]
            continue

        with open(os.path.join(baseDir,'mochitest.ini'),'r+') as mf:
            lines = mf.readlines()
            outfile = open('tmp.ini','wb')
            flag = 0
            for line in lines:
                line = line.strip('\n')
                if line.strip() == "[%s]" % fname:
                    skipif = "skip-if = %s" % skip
                    found = True
                if flag==0:
                    outfile.write(line+'\n')
                else:
                    flag = 0
                if skipif:
                    lineno = lines.index(line+'\n')
                    if lineno<len(lines)-1 and "skip-if" in lines[lineno+1]:
                        if not (("b2g" in skipif and "b2g" in lines[lineno+1]) or ("gonk" in skipif and "gonk" in lines[lineno+1])):  #the conditions however does not work if the skip-if is after a comment in mochitest.ini
                            newline = lines[lineno+1].strip().replace("skip-if =",skipif+" ||")
                            if files[key]:
                                newline += " #%s"%files[key]
                            outfile.write(newline+'\n')
                            flag = 1
                        else:
                            if files[key]:
                                skipif += " #%s"%files[key]
                            outfile.write('TODO: '+skipif+'\n')
                    else:
                        if files[key]:
                                skipif += " #%s"%files[key]
                        outfile.write(skipif+'\n')
                    skipif = ""
        if found == False:
            notfound[key] = files[key]
        outfile.close()
        os.remove(os.path.join(baseDir,'mochitest.ini'))
        os.rename('tmp.ini', os.path.join(baseDir,'mochitest.ini'))

    return notfound
     

