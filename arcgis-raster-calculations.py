#1.)Describe raster properties
#Set up the environment

folderPath = r'\\Mac\Home\Documents\GIS\Geography_173\Week_6\LabData\LabData'

import arcpy
from arcpy import env
from arcpy.sa import *
import os
env.workspace = folderPath
arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("spatial")

#Describe the raster properties

desc = arcpy.Describe(os.path.join(folderPath, 'Landsat.tif')+"/Band_1")
print 'Image size:', desc.width, 'by', desc.height, 'pixels'
print 'Spatial resolution:', desc.meanCellHeight,'m', 'by', desc.meanCellWidth, 'm'

raster = "Landsat.tif"
desc = arcpy.Describe(raster)
print 'The coordinate system is:',desc.spatialReference.Name
print 'Number of bands:',desc.bandCount

#######################################################################3
#2.) Calculate NDVI
#Inputs/outputs/variables
input = 'Landsat.tif'
result = "NDVI.tif"
NIR = input + "\Band_4"
Red = input + "\Band_3"
NIR_out = "NIR.tif"
Red_out = "Red.tif"

#Copies Rasters
arcpy.CopyRaster_management(NIR,NIR_out)
arcpy.CopyRaster_management(Red, Red_out)

#NDVI Calculation
Num = arcpy.sa.Float(Raster(NIR_out) - Raster(Red_out))
Denom = arcpy.sa.Float(Raster(NIR_out) + Raster(Red_out))
NIR_eq = arcpy.sa.Divide(Num, Denom)

NIR_eq.save(result)

########################################################################
#3.) Reclassify the raster
#Inputs
inRaster = "NDVI.tif"
reclassField = "VALUE"
remap = RemapRange([[-1,0, 1], [0, 0.3, 2], [0.3, 1, 3]])

#Execute Reclassify
outReclassify = Reclassify(inRaster, reclassField, remap)

#Save the output 
outReclassify.save(os.path.join(folderPath, 'reclassed'))

##########################################################################                   
#4.) Prints the values at (349908, 3768856)
result = arcpy.GetCellValue_management('NDVI.tif',"349908 3768856")
result2 = arcpy.GetCellValue_management('reclassed', "349908 3768856")
print 'NDVI Value:',result
print 'Category:',result2



