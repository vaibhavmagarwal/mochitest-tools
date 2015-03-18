import json, shutil
from annotatemanifests import annotateManifests
js1 = {'filename': r'C:\mozilla-inbound\mozilla-inbound\testing\mochitest\b2g.json',   #edit the path according to your own directory path
       'commentname': 'b2g',
      }

js2 = {'filename': r'C:\mozilla-inbound\mozilla-inbound\testing\mochitest\b2g-debug.json', #edit the path according to your own directory path
       'commentname': 'b2g-debug',
      }

js3 = {'filename': r'C:\mozilla-inbound\mozilla-inbound\testing\mochitest\b2g-desktop.json', #edit the path according to your own directory path
       'commentname': 'b2g-desktop',
      }

js1_json = json.load(open(js1['filename']))
js1_keys = js1_json['excludetests'].keys()

js2_json = json.load(open(js2['filename']))
js2_keys = js2_json['excludetests'].keys()

js3_json = json.load(open(js3['filename']))
js3_keys = js3_json['excludetests'].keys()


# function to build comments to be added to mochitest.ini files
def buildcomment(pre_a, a, pre_b, b, pre_c='', c=''):
    comment = ""
    if pre_a and a:
        comment = "%s %s(%s)" % (comment,pre_a, a)
 
    if pre_b and b:
        comment = "%s %s(%s)" % (comment,pre_b, b)
 
    if pre_c and c:
        comment = "%s %s(%s)" % (comment,pre_c, c)
    return comment

# function to find duplicates in dictionaries
def findDuplicatesAll(s1, s2, s3, c1, c2, c3):
    duplicates = {}
    s1keys = s1.keys()
    s2keys = s2.keys()
    s3keys = s3.keys()
    for key in s1keys:
        try:
            if s2keys.index(key)>=0 and s3keys.index(key)>=0:
                comment = buildcomment(c1, s1[key], c2, s2[key], c3, s3[key])
                duplicates[key] = comment
        except:
            continue

    for dup in duplicates:
        s1.pop(dup, None)
        s2.pop(dup, None)
        s3.pop(dup, None)
    return duplicates

def findDuplicates(s1, s2, c1, c2):
    duplicates = {}
    s1keys = s1.keys()
    s2keys = s2.keys()
    for key in s1keys:
        try:
            if s2keys.index(key)>=0:
                comment = buildcomment(c1, s1[key], c2, s2[key])
                duplicates[key] = comment
        except:
            continue
 
    for dup in duplicates:
        s1.pop(dup, None)
        s2.pop(dup, None)
    return duplicates

def find(notfound, key):
    if '(' in notfound[key]:
            tmp = notfound[key].split('(',1)
            notfound[key] = tmp[1].split(')',1)[0]
    return notfound


all_dups = findDuplicatesAll(js1_json['excludetests'], js2_json['excludetests'], js3_json['excludetests'], js1['commentname'], js2['commentname'], js3['commentname'])
desktop_debug_dups = findDuplicates(js2_json['excludetests'], js3_json['excludetests'], js2['commentname'], js3['commentname'])
mobile_debug_dups = findDuplicates(js1_json['excludetests'], js2_json['excludetests'], js1['commentname'], js2['commentname'])
mobile_desktop_dups = findDuplicates(js1_json['excludetests'], js3_json['excludetests'], js1['commentname'], js3['commentname'])

js1_out = dict(js1_json)
js1_out['excludetests'] = {}
 
js2_out = dict(js2_json)
js2_out['excludetests'] = {}
 
js3_out = dict(js3_json)
js3_out['excludetests'] = {}

    
notfound = annotateManifests(all_dups, "buildapp == 'b2g'")
if notfound:
    for key in notfound:
        notfound = find(notfound, key)
        js1_out['excludetests'][key] = notfound[key]
        js2_out['excludetests'][key] = notfound[key]
        js3_out['excludetests'][key] = notfound[key]

notfound = annotateManifests(mobile_debug_dups, "toolkit=='gonk'")
if notfound:
    for key in notfound:
        notfound = find(notfound, key)
        js1_out['excludetests'][key] = notfound[key]
        js2_out['excludetests'][key] = notfound[key]

notfound = annotateManifests(mobile_desktop_dups, "(buildapp == 'b2g' && !debug)")
if notfound:
    for key in notfound:
        notfound = find(notfound, key)
        js1_out['excludetests'][key] = notfound[key]
        js3_out['excludetests'][key] = notfound[key]

notfound = annotateManifests(desktop_debug_dups, "(buildapp == 'b2g' && (toolkit != 'gonk' || debug))")
if notfound:
    for key in notfound:
        notfound = find(notfound, key)
        js2_out['excludetests'][key] = notfound[key]
        js3_out['excludetests'][key] = notfound[key]

notfound = annotateManifests(js1_json['excludetests'], "(toolkit == 'gonk' && !debug)")
if notfound:
    for key in notfound:
        notfound = find(notfound, key)
        js1_out['excludetests'][key] = notfound[key]

notfound = annotateManifests(js2_json['excludetests'], "(toolkit == 'gonk' && debug)")
if notfound:
    for key in notfound:
        notfound = find(notfound, key)
        js2_out['excludetests'][key] = notfound[key]

notfound = annotateManifests(js3_json['excludetests'], "(buildapp == 'b2g' && toolkit != 'gonk')")
if notfound:
    for key in notfound:
        notfound = find(notfound, key)
        js3_out['excludetests'][key] = notfound[key]


#edit the path according to your own directory path
outfile1 = r'C:\mozilla-inbound\mozilla-inbound\testing\mochitest\b2g.json'    
outfile2 = r'C:\mozilla-inbound\mozilla-inbound\testing\mochitest\b2g-debug.json'
outfile3 = r'C:\mozilla-inbound\mozilla-inbound\testing\mochitest\b2g-desktop.json'

for outfile in [outfile1, outfile2, outfile3]:
    if outfile == outfile1:
        out = js1_out
    elif outfile == outfile2:
        out = js2_out
    else:
        out = js3_out
    with open(outfile,'wb') as fhandle:
        fhandle.write("{\n")
        fhandle.write('"runtests": {\n')
        for i,value in out['runtests'].iteritems():
            fhandle.write('    "%s": "%s",\n' % (i,value))
        fhandle.write("  },\n")
        fhandle.write('"excludetests": {\n')
        for i,value in out['excludetests'].iteritems():
            fhandle.write('    "%s": "%s",\n' % (i,value))
        fhandle.write("  }\n")
        fhandle.write("}\n")

'''

print "Duplicates in b2g, b2g-desktop, b2g-debug: "
print all_dups
print ""
print "Duplicates in b2g, b2g-debug: "
print mobile_debug_dups
print ""
print "Duplicates in b2g, b2g-desktop: "
print mobile_desktop_dups
print ""
print "Duplicates in b2g-debug, b2g-desktop: "
print desktop_debug_dups
print ""
print "Uniques in b2g: "
print js1_json['excludetests']
print ""
print "Uniques in b2g-debug: "
print js2_json['excludetests']
print ""
print "Uniques in b2g-desktop: "
print js3_json['excludetests']

'''
