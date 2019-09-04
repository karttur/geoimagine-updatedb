'''
Created on 6 Dec 2018

@author: thomasgumbricht
'''

from os import path
from geoimagine.gdalutilities import GDALstuff

class ProcessUpdateDB:
    '''class for layer updating'''   
    def __init__(self, process, session, verbose):
        self.session = session
        self.verbose = verbose
        self.process = process
        for locus in self.process.dstLayerD:
            print ('locus',locus)
            for datum in self.process.dstLayerD[locus]:
                #print ('    datum',datum)
                #print ('self.process.dstLayerD[locus][datum]',self.process.dstLayerD[locus][datum])
                for dstcomp in self.process.dstLayerD[locus][datum]:
                    #print ('        comp',dstcomp)
                    if path.exists(self.process.dstLayerD[locus][datum][dstcomp].FPN):
                        #print ('            processing ', self.process.dstLayerD[locus][datum][dstcomp].FPN)
                        if self.process.dstLayerD[locus][datum][dstcomp].comp.celltype == 'vector':
                            self.process.dstLayerD[locus][datum][dstcomp].comp.cellnull = -32768
                        else:
                            self.process.dstLayerD[locus][datum][dstcomp].GetRastermetadata()
                            self.process.dstLayerD[locus][datum][dstcomp].comp.cellnull = self.process.dstLayerD[locus][datum][dstcomp].metadata.cellnull
                            self.process.dstLayerD[locus][datum][dstcomp].comp.celltype = self.process.dstLayerD[locus][datum][dstcomp].metadata.celltype
                        if self.process.delete:
                            deleteDS = GDALstuff('',self.process.dstLayerD[locus][datum][dstcomp].FPN,'')
                            deleteDS.Delete()
                            self.session._DeleteLayer(self.process.dstLayerD[locus][datum][dstcomp], self.process.overwrite, self.process.delete)


                        else:
                            self.session._InsertLayer(self.process.dstLayerD[locus][datum][dstcomp], self.process.overwrite, self.process.delete)
                    else:
                        if self.process.delete:
                            #print ('deleting from db')
                            self.session._DeleteLayer(self.process.dstLayerD[locus][datum][dstcomp], self.process.overwrite, self.process.delete)
                        else:
                            print ('            non-existing ', self.process.dstLayerD[locus][datum][dstcomp].FPN)
        
        if self.process.delete:
            #If all layers are removed, also delete the compostion
            for locus in self.process.dstLayerD:
                for datum in self.process.dstLayerD[locus]:
                    for dstcomp in self.process.dstLayerD[locus][datum]:
                        self.session._DeleteComposition(self.process.dstLayerD[locus][datum][dstcomp].comp)
                    return