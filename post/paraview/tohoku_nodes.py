#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

####################
### Initialize
####################
# find source
swe = GetActiveSource()
# create a new 'Clean to Grid'
cleantoGrid1 = CleantoGrid(Input=swe)
# create a new 'Cell Data to Point Data'
cellDatatoPointData1 = CellDatatoPointData(Input=cleantoGrid1)


####################
### Bathymetry
####################
# create a new 'Warp By Scalar'
warpByScalar1 = WarpByScalar(Input=cellDatatoPointData1)
warpByScalar1.Scalars = ['POINTS', 'bathymetry']
warpByScalar1.ScaleFactor = 200
# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
renderView1.OrientationAxesVisibility = 0
# show data in view
SetActiveSource(warpByScalar1)
warpByScalar1Display = Show(warpByScalar1, renderView1)
# trace defaults for the display properties.
warpByScalar1Display.Representation = 'Surface'
warpByScalar1Display.AmbientColor = [0.0, 0.0, 0.0]
warpByScalar1Display.ColorArrayName = [None, '']
warpByScalar1Display.OSPRayScaleArray = 'bathymetry'
warpByScalar1Display.OSPRayScaleFunction = 'PiecewiseFunction'
warpByScalar1Display.SelectOrientationVectors = 'None'
warpByScalar1Display.ScaleFactor = 700050.0
warpByScalar1Display.SelectScaleArray = 'None'
warpByScalar1Display.GlyphType = 'Arrow'
warpByScalar1Display.GlyphTableIndexArray = 'None'
warpByScalar1Display.DataAxesGrid = 'GridAxesRepresentation'
warpByScalar1Display.PolarAxes = 'PolarAxesRepresentation'
warpByScalar1Display.ScalarOpacityUnitDistance = 134493.00080998472
warpByScalar1Display.GaussianRadius = 350025.0
warpByScalar1Display.SetScaleArray = ['POINTS', 'bathymetry']
warpByScalar1Display.ScaleTransferFunction = 'PiecewiseFunction'
warpByScalar1Display.OpacityArray = ['POINTS', 'bathymetry']
warpByScalar1Display.OpacityTransferFunction = 'PiecewiseFunction'
# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
warpByScalar1Display.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
warpByScalar1Display.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
warpByScalar1Display.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
warpByScalar1Display.DataAxesGrid.GridColor = [0.0, 0.0, 0.0]
warpByScalar1Display.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
warpByScalar1Display.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
warpByScalar1Display.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]
# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
warpByScalar1Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
warpByScalar1Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
warpByScalar1Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
warpByScalar1Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]
# set scalar coloring
ColorBy(warpByScalar1Display, ('POINTS', 'bathymetry'))
warpByScalar1Display.RescaleTransferFunctionToDataRange(True, False)
warpByScalar1Display.SetScalarBarVisibility(renderView1, False)
warpByScalar1Display.Opacity = 1.0
# get color transfer function/color map for 'bathymetry'
bathymetryLUT = GetColorTransferFunction('bathymetry')
bathymetryLUT.ApplyPreset('Viridis (matplotlib)', True)
bathymetryLUT.LockDataRange = 1
bathymetryLUT.RescaleTransferFunction(-8400.0, 2000.0)
bathymetryLUT.NanColor = [0.25, 0.0, 0.0]
bathymetryLUT.ScalarRangeInitialized = 1.0
# get opacity transfer function/opacity map for 'bathymetry'
bathymetryPWF = GetOpacityTransferFunction('bathymetry')
bathymetryPWF.Points = [-8378.454650878906, 0.0, 0.5, 0.0, 1740.581974029541, 1.0, 0.5, 0.0]
bathymetryPWF.ScalarRangeInitialized = 1
bathymetryPWF.RescaleTransferFunction(-8400.0, 2000.0)



####################
### Water Height
####################
# set active source
SetActiveSource(cellDatatoPointData1)
# create a new 'Warp By Scalar'
warpByScalar2 = WarpByScalar(Input=cellDatatoPointData1)
warpByScalar2.Scalars = ['POINTS', 'water height']
WarpByScalar2.ScaleFactor = 20000
# set active source
SetActiveSource(warpByScalar2)
warpByScalar2Display = Show(warpByScalar2, renderView1)
# trace defaults for the display properties.
warpByScalar2Display.Representation = 'Surface'
warpByScalar2Display.AmbientColor = [0.0, 0.0, 0.0]
warpByScalar2Display.ColorArrayName = [None, '']
warpByScalar2Display.OSPRayScaleArray = 'bathymetry'
warpByScalar2Display.OSPRayScaleFunction = 'PiecewiseFunction'
warpByScalar2Display.SelectOrientationVectors = 'None'
warpByScalar2Display.ScaleFactor = 700050.0
warpByScalar2Display.SelectScaleArray = 'None'
warpByScalar2Display.GlyphType = 'Arrow'
warpByScalar2Display.GlyphTableIndexArray = 'None'
warpByScalar2Display.DataAxesGrid = 'GridAxesRepresentation'
warpByScalar2Display.PolarAxes = 'PolarAxesRepresentation'
warpByScalar2Display.ScalarOpacityUnitDistance = 131768.024917349
warpByScalar2Display.GaussianRadius = 350025.0
warpByScalar2Display.SetScaleArray = ['POINTS', 'bathymetry']
warpByScalar2Display.ScaleTransferFunction = 'PiecewiseFunction'
warpByScalar2Display.OpacityArray = ['POINTS', 'bathymetry']
warpByScalar2Display.OpacityTransferFunction = 'PiecewiseFunction'
# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
warpByScalar2Display.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
warpByScalar2Display.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
warpByScalar2Display.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
warpByScalar2Display.DataAxesGrid.GridColor = [0.0, 0.0, 0.0]
warpByScalar2Display.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
warpByScalar2Display.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
warpByScalar2Display.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]
# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
warpByScalar2Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
warpByScalar2Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
warpByScalar2Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
warpByScalar2Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]
# set scalar coloring
ColorBy(warpByScalar2Display, ('POINTS', 'water height'))
warpByScalar2Display.RescaleTransferFunctionToDataRange(True, False)
warpByScalar2Display.SetScalarBarVisibility(renderView1, True)
warpByScalar2Display.Opacity = 0.6
# get color transfer function/color map for 'waterheight'
waterheightLUT = GetColorTransferFunction('waterheight')
waterheightLUT.ApplyPreset('Cold and Hot', True)
waterheightLUT.ScalarRangeInitialized = 1.0
waterheightLUT.RescaleTransferFunction(-5.0, 10.0)
waterheightLUT.LockDataRange = 1
waterheightLUT.EnableOpacityMapping = 0
waterheightLUT.RGBPoints = [-5.0, 0.0, 1.0, 1.0, -1.0, 0.0, 0.0, 1.0, 0.1, 0.0, 0.0, 0.501960784314, 0.15, 0.11764705882352941, 0.0, 0.44313725490196076, 0.4, 1.0, 0.0, 0.0, 10.0, 1.0, 1.0, 0.0]
waterheightLUT.ColorSpace = 'RGB'
# get opacity transfer function/opacity map for 'waterheight'
waterheightPWF = GetOpacityTransferFunction('waterheight')
waterheightPWF.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]
waterheightPWF.ScalarRangeInitialized = 1.0
waterheightPWF.RescaleTransferFunction(-5.0, 10.0)
# get color legend/bar for waterheightLUT in view renderView1
waterheightLUTColorBar = GetScalarBar(waterheightLUT, renderView1)
waterheightLUTColorBar.WindowLocation = 'UpperRightCorner'
waterheightLUTColorBar.Title = 'Water Height'
waterheightLUTColorBar.ComponentTitle = ''
waterheightLUTColorBar.TitleColor = [0.0, 0.0, 0.0]
waterheightLUTColorBar.LabelColor = [0.0, 0.0, 0.0]


####################
### Split View
####################
# get layout and split
layout1 = GetLayout()
layout1.SplitHorizontal(0, 0.47)
# Create a new 'Render View'
renderView2 = CreateView('RenderView')
renderView2.AnnotationColor = [0.0, 0.0, 0.0]
renderView2.AxesGrid = 'GridAxes3DActor'
renderView2.OrientationAxesLabelColor = [0.0, 0.0, 0.0]
renderView2.OrientationAxesOutlineColor = [0.0, 0.0, 0.0]
renderView2.StereoType = 0
renderView2.Background = [1.0, 1.0, 1.0]
# init the 'GridAxes3DActor' selected for 'AxesGrid'
renderView2.AxesGrid.XTitleColor = [0.0, 0.0, 0.0]
renderView2.AxesGrid.YTitleColor = [0.0, 0.0, 0.0]
renderView2.AxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
renderView2.AxesGrid.GridColor = [0.0, 0.0, 0.0]
renderView2.AxesGrid.XLabelColor = [0.0, 0.0, 0.0]
renderView2.AxesGrid.YLabelColor = [0.0, 0.0, 0.0]
renderView2.AxesGrid.ZLabelColor = [0.0, 0.0, 0.0]


####################
### Nodes
####################
# set active view
SetActiveView(renderView2)
# get active source.
warpByScalar1 = GetActiveSource()
SetActiveSource(warpByScalar1)
# place view in the layout
layout1.AssignView(2, renderView2)
# show data in view
warpByScalar1Display = Show(warpByScalar1, renderView2)
# trace defaults for the display properties.
warpByScalar1Display.Representation = 'Surface'
warpByScalar1Display.AmbientColor = [0.0, 0.0, 0.0]
warpByScalar1Display.ColorArrayName = [None, '']
warpByScalar1Display.OSPRayScaleArray = 'bathymetry'
warpByScalar1Display.OSPRayScaleFunction = 'PiecewiseFunction'
warpByScalar1Display.SelectOrientationVectors = 'None'
warpByScalar1Display.ScaleFactor = 700050.0
warpByScalar1Display.SelectScaleArray = 'None'
warpByScalar1Display.GlyphType = 'Arrow'
warpByScalar1Display.GlyphTableIndexArray = 'None'
warpByScalar1Display.DataAxesGrid = 'GridAxesRepresentation'
warpByScalar1Display.PolarAxes = 'PolarAxesRepresentation'
warpByScalar1Display.ScalarOpacityUnitDistance = 134493.00080998472
warpByScalar1Display.GaussianRadius = 350025.0
warpByScalar1Display.SetScaleArray = ['POINTS', 'bathymetry']
warpByScalar1Display.ScaleTransferFunction = 'PiecewiseFunction'
warpByScalar1Display.OpacityArray = ['POINTS', 'bathymetry']
warpByScalar1Display.OpacityTransferFunction = 'PiecewiseFunction'
# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
warpByScalar1Display.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
warpByScalar1Display.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
warpByScalar1Display.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
warpByScalar1Display.DataAxesGrid.GridColor = [0.0, 0.0, 0.0]
warpByScalar1Display.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
warpByScalar1Display.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
warpByScalar1Display.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]
# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
warpByScalar1Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
warpByScalar1Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
warpByScalar1Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
warpByScalar1Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]
# reset view to fit data
renderView2.ResetCamera()
renderView2.InteractionMode = '2D'
renderView2.OrientationAxesVisibility = 0
# set scalar coloring
ColorBy(warpByScalar1Display, ('POINTS', 'node'))
warpByScalar1Display.RescaleTransferFunctionToDataRange(True, False)
warpByScalar1Display.SetScalarBarVisibility(renderView2, True)
warpByScalar1Display.SetRepresentationType('Wireframe')
# get color transfer function/color map for 'node'
nodeLUT = GetColorTransferFunction('node')
nodeLUT.ApplyPreset('Rainbow Desaturated', True)
nodeLUT.RescaleTransferFunction(0, 31)
nodeLUT.LockDataRange = 1
nodeLUT.NumberOfTableValues = 32
nodeLUT.ColorSpace = 'RGB'
nodeLUT.ScalarRangeInitialized = 1.0
# get color legend/bar for nodeLUT in view renderView2
nodeLUTColorBar = GetScalarBar(nodeLUT, renderView2)
nodeLUTColorBar.WindowLocation = 'UpperRightCorner'
nodeLUTColorBar.Title = 'Utilized Nodes'
nodeLUTColorBar.ComponentTitle = ''
nodeLUTColorBar.TitleColor = [0.0, 0.0, 0.0]
nodeLUTColorBar.LabelColor = [0.0, 0.0, 0.0]


#########################
### Camera placements
#########################
# current camera placement for renderView1
renderView1.InteractionMode = '3D'
renderView1.CameraPosition = [3000000.0, -10352804.801670311, 13533330.38000944]
renderView1.CameraFocalPoint = [3000000.0, -2000000.0, -663787.234375]
renderView1.CameraViewUp = [0.0, 0.8618928466972772, 0.5070904463821655]
renderView1.CameraParallelScale = 5166093.358573748
# current camera placement for renderView2
renderView2.InteractionMode = '2D'
renderView2.CameraPosition = [3000000.0, -2000000.0, 27140429.637672078]
renderView2.CameraFocalPoint = [3000000.0, -2000000.0, -663787.234375]
renderView2.CameraParallelScale = 4135381.692367198

#### uncomment the following to render all views
#RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
