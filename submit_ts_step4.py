#!/usr/bin/env python
"""
  Transformation removing intermediate mandelbrot images
"""

from DIRAC.Core.Base import Script
Script.parseCommandLine()
Script.setUsageMessage( '\n'.join( [ __doc__.split( '\n' )[1],
                                     'Usage:',
                                     '  %s [option|cfgfile] ... [File List] ...' % Script.scriptName,
                                     'Arguments:',
                                     '  List of Files to remove'] ) )
import DIRAC
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
 
  t = Transformation( )
  tc = TransformationClient( )

  t.setType("Removal")
  t.setPlugin("Standard") # Not needed. The default is 'Standard'
  t.setDescription("Remove intermediate mandelbrot images")
  t.setLongDescription( "Remove intermediate mandelbrot images" ) # Mandatory
  #t.setGroupSize( 1 )  # Here you specify how many files should be grouped within the same request, e.g. 100
  t.setBody ( "Removal;RemoveFile" ) # Mandatory (the default is a ReplicateAndRegister operation)

  res = t.addTransformation()  # Transformation is created here
  if not res['OK']:
    print(res['Message'])
    DIRAC.exit( -1 )

  t.setStatus("Active")
  t.setAgentType("Automatic")
  transID = t.getTransformationID()
  tc.addFilesToTransformation(transID['Value'],infileList) # Files are added here

  return res

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
    


