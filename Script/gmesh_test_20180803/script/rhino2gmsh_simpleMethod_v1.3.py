import rhinoscriptsyntax as rs
import os
#parameter box is point list containing 8 points in a counter-clockwise order
def offsetBox(box,dist):
    newBox=box
    #point 0
    newBox[0][0]=box[0][0]-dist
    newBox[0][1]=box[0][1]-dist
    newBox[0][2]=box[0][2]
    #point 1
    newBox[1][0]=box[1][0]+dist
    newBox[1][1]=box[1][1]-dist
    newBox[1][2]=box[1][2]
    #point 2
    newBox[2][0]=box[2][0]+dist
    newBox[2][1]=box[2][1]+dist
    newBox[2][2]=box[2][2]
    #point 3
    newBox[3][0]=box[3][0]-dist
    newBox[3][1]=box[3][1]+dist
    newBox[3][2]=box[3][2]
    #point 4
    newBox[4][0]=box[4][0]-dist
    newBox[4][1]=box[4][1]-dist
    newBox[4][2]=box[4][2]+dist
    #point 5
    newBox[5][0]=box[5][0]+dist
    newBox[5][1]=box[5][1]-dist
    newBox[5][2]=box[5][2]+dist
    #point 6
    newBox[6][0]=box[6][0]+dist
    newBox[6][1]=box[6][1]+dist
    newBox[6][2]=box[6][2]+dist
    #point 7
    newBox[7][0]=box[7][0]-dist
    newBox[7][1]=box[7][1]+dist
    newBox[7][2]=box[7][2]+dist
    newBoxId=rs.AddBox(newBox)
    return newBoxId
    
    
def rhino2gmsh():
    tetMeshSize=3.0
    f= open("test.geo","w+")
    f.write("tetMeshSize=%s;\n" %tetMeshSize)
    
    [mPtDict,mLineDict,mSurfDict,mVolDict]=load2GeoDict()
    
    for i in range(len(mPtDict)):
        #rebuild points 
        if mPtDict[i]['isRepeated']==False:
            f.write("Point(%d)={%s,tetMeshSize};\n" %(mPtDict[i]['ptIndex'],str(mPtDict[i]['pt'])))
        #end if
    #end for
    
    for i in range(len(mLineDict)):
        if mLineDict[i]['isRepeated']==False:
            f.write("Line(%d)={%s,%s};\n" %(mLineDict[i]['lineIndex'],mLineDict[i]['line'][0],mLineDict[i]['line'][1]))
        #end if
    #end for
    
    for i in range(len(mSurfDict)):
        lineLoopStr=""
        for j in range(len(mSurfDict[i]['lineLoopList'])):
            lineLoopStr+=str(mSurfDict[i]['lineLoopList'][j])+','
            
        f.write("Line Loop(%d)={%s};\n" %(mSurfDict[i]['surfIndex'],lineLoopStr[:-1]))
        f.write("Plane Surface(%d)={%d};\n" %(mSurfDict[i]['surfIndex'],mSurfDict[i]['surfIndex']))
    #end for

    for i in range(len(mVolDict)):
        surfLoopStr=""
        for j in range(len(mVolDict[i]['surfLoopList'])):
            surfLoopStr+=str(mVolDict[i]['surfLoopList'][j])+','
        f.write("Surface Loop(%d)={%s};\n" %(mVolDict[i]['volIndex'],surfLoopStr[:-1]))
        f.write("Volume(%d)={%d};\n" %(mVolDict[i]['volIndex'],mVolDict[i]['volIndex']))
    #end for
    
    
    
    f.close()
    return
    
def addDummyBox():
    objs1=rs.ObjectsByLayer("Surr",False)
    objs2=rs.ObjectsByLayer("Proj",False)
    objs=objs1+objs2
    myBox=rs.BoundingBox(objs)
    newBoxId=offsetBox(myBox,10)
    rs.ObjectLayer(newBoxId,"dummy")
    return

def load2GeoDict():
    objs=rs.ObjectsByLayer("test",False) #return polysurfaces id list
    
    countVolume=0
    countSurface=0
    countLine=0
    countPt=0
    ptDict=[] #define empty list
    ##########################################################################################
    #creat point dict
    #ptDict[i]={ptIndex, ptCoordinate, isRepeated, surfaceMark, volumeMark}
    for obj in objs: #each obj stands for a polysurface i.e a volume
        countVolume+=1
        surfaces=rs.ExplodePolysurfaces(obj)
        for surface in surfaces:
            countSurface+=1
            lines=rs.DuplicateSurfaceBorder(surface) #return a closed line
            pts=rs.CurvePoints(lines) #return edit points in the line
            for pt in pts: #ignore the last point as it is same as the first point
                countPt+=1
                ptDict.append({'ptIndex':countPt,'pt':pt,'isRepeated':False,'surfaceMark':countSurface,'volumeMark':countVolume})
            #end for
            rs.DeleteObjects(lines) #delete the duplicate lines
        #end for
        rs.DeleteObjects(surfaces)
    #end for

    #same point location is assigned with same pointId in ptDict - this is a O(n^2), which can be optimized by balance tree data structure
    #ptDict[1]={ptIndex:1, ptCoordinate:pt, isRepeated, surfaceMark:1, volumeMark:1}
    #if ptDict[5]={ptIndex:5, ptCoordinate:sameAs pt, isRepeated, surfaceMark:1, volumeMark:1} has ptCoordinate same as ptDict[1]
    #transfer2 ptDict[5]={ptIndex:1, ptCoordinate:sameAs pt, isRepeated, surfaceMark:1, volumeMark:1}
    for i in range(len(ptDict)):
        for j in range(len(ptDict)):
            if ptDict[i]['pt']==ptDict[j]['pt'] and i!=j and ptDict[i]['ptIndex']!=ptDict[j]['ptIndex']:
                ptDict[j]['ptIndex']=ptDict[i]['ptIndex']
                ptDict[j]['isRepeated']=True
        #end for
    #end for
    
    ################################################################################################################
    #create lineDict from ptDict
    #lineDict[i]={lineIndex, lineBy2PtIndex, signedLineIndex, isRepeated, surfaceMark, volumeMark}
    lineDict=[]
    lineIndex=0
    for i in range(1,len(ptDict)):
        if ptDict[i]['volumeMark']==ptDict[i-1]['volumeMark'] and ptDict[i]['surfaceMark']==ptDict[i-1]['surfaceMark']:#pt in same surface
            lineIndex+=1
            lineDict.append({'lineIndex':lineIndex,'line':(ptDict[i-1]['ptIndex'],ptDict[i]['ptIndex']),'signedLineIndex':lineIndex,'isRepeated':False,'surfaceMark':ptDict[i]['surfaceMark'],'volumeMark':ptDict[i]['volumeMark']})
        #end if
    #end for
    
    #line with same ptIndex problem: 
    #1. assign line with same ptIndex into same lineIndex
    #2. assign lineIndex direction into signLineIndex
    for i in range(len(lineDict)):
        for j in range(len(lineDict)):
            if isSameLine(lineDict[i]['line'],lineDict[j]['line']) and lineDict[i]['lineIndex']!=lineDict[j]['lineIndex'] and i!=j:
                lineDict[j]['lineIndex']=lineDict[i]['lineIndex']
                if isSameLineDir(lineDict[i]['line'],lineDict[j]['line']):
                    lineDict[j]['signedLineIndex']=lineDict[i]['signedLineIndex']
                    lineDict[j]['isRepeated']=True
                else:
                    lineDict[j]['signedLineIndex']=-lineDict[i]['signedLineIndex']
                    lineDict[j]['isRepeated']=True
    ################################################################################################################
    #create surfDict from lineDict
    #surfDict[i]={surfIndex, lineLoopList, volumeMark}
    surfDict=[]
    surfIndex=0
    lineLoopList=[lineDict[0]['signedLineIndex']]
    for i in range(1,len(lineDict)):
        if lineDict[i]['volumeMark']==lineDict[i-1]['volumeMark'] and lineDict[i]['surfaceMark']==lineDict[i-1]['surfaceMark']:#pt in same surface
            lineLoopList.append(lineDict[i]['signedLineIndex'])
        else:
            surfIndex+=1
            surfDict.append({'surfIndex':surfIndex,'lineLoopList':lineLoopList,'volumeMark':lineDict[i-1]['volumeMark']})
            lineLoopList=[lineDict[i]['signedLineIndex']]
        
        if i==len(lineDict)-1: #last element
            surfIndex+=1
            surfDict.append({'surfIndex':surfIndex,'lineLoopList':lineLoopList,'volumeMark':lineDict[i]['volumeMark']})
            
    ################################################################################################################
    #create volumeDict from surfDict
    #volumeDict[i]={volIndex, surfLoopList}
    volDict=[]
    volIndex=0
    surfLoopList=[surfDict[0]['surfIndex']]
    for i in range(1,len(surfDict)):
        if surfDict[i]['volumeMark']==surfDict[i-1]['volumeMark']:
            surfLoopList.append(surfDict[i]['surfIndex'])
        else:
            volIndex+=1
            volDict.append({'volIndex':volIndex,'surfLoopList':surfLoopList})
            surfLoopList=[surfDict[i]['surfIndex']]
            
        if i==len(surfDict)-1:#last element
            volIndex+=1
            volDict.append({'volIndex':volIndex,'surfLoopList':surfLoopList})
    
    return [ptDict,lineDict,surfDict, volDict]

def isSameLine(line1,line2):
    res = False
    if line1[0]==line2[1] and line1[1]==line2[0]:
        res=True
    elif line1[0]==line2[0] and line1[1]==line2[1]:
        res=True
    return res 
    
def isSameLineDir(line1,line2):
    res = False
    if line1[0]==line2[1] and line1[1]==line2[0]:
        res=False
    elif line1[0]==line2[0] and line1[1]==line2[1]:
        res=True
    return res 
    
rhino2gmsh()
