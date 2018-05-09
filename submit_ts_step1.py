""" Transformation launching Mandelbrot jobs
"""

from DIRAC.Core.Base import Script
Script.parseCommandLine()

import DIRAC
from DIRAC.Interfaces.API.Job import Job
from DIRAC.Core.Workflow.Parameter import Parameter
from DIRAC.TransformationSystem.Client.Transformation import Transformation

def submitTS():

 
  job = Job()

  job.setName('mandelbrot')

  ### Temporary fix to initialize JOB_ID #######
  job.workflow.addParameter( Parameter( "JOB_ID", "000000", "string", "", "", True, False, "Temporary fix" ) ) 
  job.workflow.addParameter( Parameter( "PRODUCTION_ID", "000000", "string", "", "", True, False, "Temporary fix" ) ) 
  job.setType('MCSimulation')
  
  job.setExecutable('git clone https://github.com/bregeon/mandel4ts.git')
  job.setExecutable('./mandel4ts/mandelbrot.py',arguments="-P 0.0005 -M 1000 -L @{JOB_ID}*200 -N 200 data_@{JOB_ID}*200.bmp")
  job.setOutputData( ['data_*.bmp','data*.txt'],outputPath='mandelbrot/image/raw')
  
  t = Transformation()

  t.setType( "MCSimulation" ) 
  t.setDescription( "Mandelbrot images production" )
  t.setLongDescription( "Mandelbrot images production" )  # mandatory
  t.setBody ( job.workflow.toXML() )

  res = t.addTransformation()  # Transformation is created here

  if not res['OK']:
    print(res['Message'])
    DIRAC.exit( -1 )

  t.setStatus( "Active" )
  t.setAgentType( "Automatic" )
  
  return res


#########################################################
if __name__ == '__main__':

  try:
    res = submitTS()
    if not res['OK']:
      DIRAC.gLogger.error ( res['Message'] )
      DIRAC.exit( -1 )
    #else:
      #DIRAC.gLogger.notice( 'Created transformation: %s' % res['Value'] )
  except Exception:
    DIRAC.gLogger.exception()
    DIRAC.exit( -1 )
