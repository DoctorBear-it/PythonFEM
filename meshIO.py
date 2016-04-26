# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 16:56:56 2016

@author: Timothy
"""

import numpy as np
import Tkinter as tk
import tkFileDialog
import sys
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

#arrays = [np.array(map(int,line.split())) for line in open(file_path)]

class gmsh:
    """
    mesh class reads the .msh file generated from Gmsh 
    
    .msh file format is located at: 
    http://gmsh.info/doc/texinfo/gmsh.html#MSH-ASCII-file-format
    
    """
    
    def __init__(self):
        #initialize the gmsh class 
        self.nodes = []
        self.elements = {}
        self.elementData = []
        self.nNodes = 0
        self.nElements = 0
        self.d = {}
        self.xy = []        
        
    def read(self,file_path):
        fileSections = [        
            ('$MeshFormat',
            '$EndMeshFormat'),
            ('$PhysicalNames',
            '$EndPhysicalNames'),
            ('$Nodes',
            '$EndNodes'),
            ('$Elements',
            '$EndElements'),
            ('$Periodic',
            '$EndPeriodic'),
            ('$NodeData',
            '$EndNodeData'),
            ('$ElementData',
            '$EndElementData'),
            ('$ElementNodeData',
            '$EndElementNodeData'),
            ('$InterpolationScheme',
            '$EndInterpolationScheme'),
        ]

        with open(file_path,'r') as f:
            text = f.read()
        
        lines = text.splitlines()
        
        sectionStart = []        
        sectionEnd = []
        for begin,end in fileSections:
            if begin in lines:
                sectionStart.append(lines.index(begin))
            if end in lines:
                sectionEnd.append(lines.index(end))
            

        for i in zip(sectionStart,sectionEnd):
            key = lines[i[0]]
            values = lines[i[0]+1:i[1]]
            values = [values[i].split() for i,val in enumerate(values)]
            values = [[float(i) for i in j] for j in values]           
            self.d[key] = values
        

    
    def splitshitup(self):
        nodeInput = self.d['$Nodes']
        self.nNodes = nodeInput[0]
        self.nodes = np.array(nodeInput[1::])
        self.xy = self.nodes[::,1:3]
        
        elementInput = self.d['$Elements']
        self.nElements = elementInput[0]
        self.elementData = elementInput[1::]
        
        for i in xrange(31):
            self.elements["element_type_%s" %(i+1)] = [el for n,el in enumerate(self.elementData) if el[1]==(i+1)]
               
    def plotMesh(self):
        #Plots the mesh for element type 2 (3 node triangular mesh)
        
        codes = [Path.MOVETO,
                 Path.LINETO,
                 Path.LINETO,
                 Path.CLOSEPOLY,
                 ]
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        #ax.scatter(*zip(*self.xy))     
        
        for n,el in enumerate(self.elements['element_type_2']):
            elnodes = el[-3:]
            verts = [self.xygen(i) for i in elnodes]          
            verts.append(verts[0])            
            path = Path(verts,codes)
            patch = patches.PathPatch(path, facecolor='none',lw=1)
            ax.add_patch(patch)
        
        ax.set_xlim(self.xy[::,0].min()-1,self.xy[::,0].max()+1)
        ax.set_ylim(self.xy[::,1].min()-1,self.xy[::,1].max()+1)        
        plt.gca().set_aspect('equal')        
        plt.show()        
            
    def xygen(self, i):
        for n,elm in enumerate(self.nodes):
            if i==elm[0]:
                p = elm[-3:-1] 
        return p
            
    def elm_types(self):
        elm_type = {}
        elm_type[1] = 2     # 2-node line
        elm_type[2] = 3     # 3-node triangle
        elm_type[3] = 4     # 4-node quadrangle
        elm_type[4] = 4     # 4-node tetrahedron
        elm_type[5] = 8     # 8-node hexahedron
        elm_type[6] = 6     # 6-node prism
        elm_type[7] = 5     # 5-node pyramid
        elm_type[8] = 3     # 3-node second order line
                            # (2 nodes at vertices and 1 with edge)
        elm_type[9] = 6     # 6-node second order triangle
                            # (3 nodes at vertices and 3 with edges)
        elm_type[10] = 9    # 9-node second order quadrangle
                            # (4 nodes at vertices,
                            #  4 with edges and 1 with face)
        elm_type[11] = 10   # 10-node second order tetrahedron
                            # (4 nodes at vertices and 6 with edges)
        elm_type[12] = 27   # 27-node second order hexahedron
                            # (8 nodes at vertices, 12 with edges,
                            #  6 with faces and 1 with volume)
        elm_type[13] = 18   # 18-node second order prism
                            # (6 nodes at vertices,
                            #  9 with edges and 3 with quadrangular faces)
        elm_type[14] = 14   # 14-node second order pyramid
                            # (5 nodes at vertices,
                            #  8 with edges and 1 with quadrangular face)
        elm_type[15] = 1    # 1-node point
        elm_type[16] = 8    # 8-node second order quadrangle
                            # (4 nodes at vertices and 4 with edges)
        elm_type[17] = 20   # 20-node second order hexahedron
                            # (8 nodes at vertices and 12 with edges)
        elm_type[18] = 15   # 15-node second order prism
                            # (6 nodes at vertices and 9 with edges)
        elm_type[19] = 13   # 13-node second order pyramid
                            # (5 nodes at vertices and 8 with edges)
        elm_type[20] = 9    # 9-node third order incomplete triangle
                            # (3 nodes at vertices, 6 with edges)
        elm_type[21] = 10   # 10-node third order triangle
                            # (3 nodes at vertices, 6 with edges, 1 with face)
        elm_type[22] = 12   # 12-node fourth order incomplete triangle
                            # (3 nodes at vertices, 9 with edges)
        elm_type[23] = 15   # 15-node fourth order triangle
                            # (3 nodes at vertices, 9 with edges, 3 with face)
        elm_type[24] = 15   # 15-node fifth order incomplete triangle
                            # (3 nodes at vertices, 12 with edges)
        elm_type[25] = 21   # 21-node fifth order complete triangle
                            # (3 nodes at vertices, 12 with edges, 6 with face)
        elm_type[26] = 4    # 4-node third order edge
                            # (2 nodes at vertices, 2 internal to edge)
        elm_type[27] = 5    # 5-node fourth order edge
                            # (2 nodes at vertices, 3 internal to edge)
        elm_type[28] = 6    # 6-node fifth order edge
                            # (2 nodes at vertices, 4 internal to edge)
        elm_type[29] = 20   # 20-node third order tetrahedron
                            # (4 nodes at vertices, 12 with edges,
                            #  4 with faces)
        elm_type[30] = 35   # 35-node fourth order tetrahedron
                            # (4 nodes at vertices, 18 with edges,
                            #  12 with faces, 1 in volume)
        elm_type[31] = 56   # 56-node fifth order tetrahedron
                            # (4 nodes at vertices, 24 with edges,
                            #  24 with faces, 4 in volume)
        
        self.elm_type = elm_type
        
        
        
if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    file_path = tkFileDialog.askopenfilename(filetypes = [('Gmsh files','*.msh')])
    
    mesh = gmsh()
    mesh.read(file_path)
    mesh.splitshitup()
    mesh.plotMesh()