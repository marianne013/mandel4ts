""" Transformation creating the job building the final mandelbrot image
"""

from DIRAC.Core.Base import Script
Script.parseCommandLine()

import DIRAC
from DIRAC.Interfaces.API.Job import Job
from DIRAC.TransformationSystem.Client.Transformation import Transformation
from DIRAC.TransformationSystem.Client.TransformationClient import TransformationClient

def submitTS( args ):
  
  # get arguments
  infile = args[0]
  f = open( infile, 'r' )
  infileList = []
  for line in f:
    infile = line.strip()
    if line != "\n":
      infileList.append( infile )
 
  job = Job()
  job.setName('build mandelbrot image')
  
  job.setExecutable('git clone https://github.com/bregeon/mandel4ts.git')
  job.setExecutable('./mandel4ts/build_merged_img.py')
  job.setOutputData( ['merged_image.bmp'],outputPath='mandelbrot/images/final')
  
  t = Transformation()
  tc = TransformationClient()

  t.setType( "DataReprocessing" ) 
  t.setDescription( "Build the final mandelbrot image" )
  t.setLongDescription( "Build the final mandelbrot image" )
  t.setGroupSize( 3 ) 
  t.setBody ( job.workflow.toXML() )

  res = t.addTransformation()  # Transformation is created here

  if not res['OK']:
    print(res['Message'])
    DIRAC.exit( -1 )

  t.setStatus( "Active" )
  t.setAgentType( "Automatic" )
  transID = t.getTransformationID()
  tc.addFilesToTransformation(transID['Value'],infileList) # files are added here
  
  return res


#########################################################
if __name__ == '__main__':

  args = Script.getPositionalArgs()
  if ( len( args ) != 1):
    Script.showHelp()
  try:
    res = submitTS( args )
    if not res['OK']:
      DIRAC.gLogger.error ( res['Message'] )
      DIRAC.exit( -1 )
  except Exception:
    DIRAC.gLogger.exception()
    DIRAC.exit( -1 )
