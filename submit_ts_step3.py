""" Transformation creating merge mandelbrot jobs
"""

from DIRAC.Core.Base import Script
Script.parseCommandLine()

import DIRAC
from DIRAC.Interfaces.API.Job import Job
from DIRAC.Core.Workflow.Parameter import Parameter
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
  job.setName('merge mandelbrot')

  ### Temporary fix to initialize JOB_ID #######
  job.workflow.addParameter( Parameter( "JOB_ID", "000000", "string", "", "", True, False, "Temporary fix" ) ) 
  job.workflow.addParameter( Parameter( "PRODUCTION_ID", "000000", "string", "", "", True, False, "Temporary fix" ) ) 
  job.setType('DataReprocessing')
  
  job.setExecutable('git clone https://github.com/bregeon/mandel4ts.git')
  job.setExecutable('./mandel4ts/build_merged_img.py')
  job.setOutputData( ['merged_image.bmp'],outputPath='mandelbrot/image/merged')
  
  t = Transformation()
  tc = TransformationClient()

  t.setType( "DataReprocessing" ) 
  t.setDescription( "Merge mandelbrot images production" )
  t.setLongDescription( "Merge mandelbrot images production" )
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
