import ROOT
from optparse import OptionParser
from operator import add
import math
import sys
import time
import array

parser = OptionParser()
parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
parser.add_option('--doMCLooping', action='store_true', dest='doMCLooping', default=False, help='go!')
parser.add_option('--doRhalphabet', action='store_true', dest='doRhalphabet', default=False, help='go!')
parser.add_option('--doData', action='store_true', dest='doData', default=False, help='go!')
parser.add_option('--doPlots', action='store_true', dest='doPlots', default=False, help='go!')
parser.add_option('--doCards', action='store_true', dest='doCards', default=False, help='go!')

parser.add_option("--lumi", dest="lumi", default = 0.44,help="mass of LSP", metavar="MLSP")
parser.add_option("--rholo", dest="rholo", default = 0.,help="mass of LSP", metavar="MLSP")
parser.add_option("--rhohi", dest="rhohi", default = 4.,help="mass of LSP", metavar="MLSP")
parser.add_option("--DDTcut", dest="DDTcut", default = 0.45,help="mass of LSP", metavar="MLSP")

# parser.add_option("--rholo", dest="rholo", default = 0.,help="mass of LSP", metavar="MLSP")
(options, args) = parser.parse_args()

from MCContainer import *
from rhalphabet import *
from plotHelpers import makeCanvas, makeCanvasDataMC, makeCanvasShapeComparison,makeCanvas2D,makeCanvasDataMC_wpred,makeCanvasComparison
from combineHelper import buildDatacards
#
import tdrstyle
tdrstyle.setTDRStyle()
ROOT.gStyle.SetPadTopMargin(0.06);
ROOT.gStyle.SetPadLeftMargin(0.16);
ROOT.gStyle.SetPadRightMargin(0.10);
ROOT.gStyle.SetPalette(1);
ROOT.gStyle.SetPaintTextFormat("1.1f");
ROOT.gStyle.SetOptFit(0000);

###############################################################################################################
# M A I N 
###############################################################################################################
def main(): 

	idir = "/Users/ntran/Documents/Research/CMS/WZpToQQ/bkgEst/sklim-v2";

	####################################################################################
	# do mc looping - a class that holds histograms
	bkgContainers = None;
	sigContainers = None;
	if options.doMCLooping: 
		
		bkgContainers = [];
		bkgNames = ["QCD.root","W.root"];
		bkgLabels = ["QCD","W(qq)"];
		bkgTags = ["QCD","Winc"];
		for i in range(len(bkgNames)):
			bkgContainers.append( MCContainer( idir+"/"+bkgNames[i], float(options.lumi)/3., bkgLabels[i], bkgTags[i], 1 ) );
			# random factor of 3 w.r.t. data

		sigContainers = [];
		sigNames = [];
		sigNames.append("ZPrimeToQQ_50GeV_v4_mc.root")
		sigNames.append("ZPrimeToQQ_100GeV_v4_mc.root")
		sigNames.append("ZPrimeToQQ_150GeV_v4_mc.root")
		sigNames.append("ZPrimeToQQ_200GeV_v4_mc.root")
		sigNames.append("ZPrimeToQQ_250GeV_v4_mc.root")
		sigNames.append("ZPrimeToQQ_300GeV_v4_mc.root")	
		sigLabels = ["Z\'(50 GeV)","Z\'(100 GeV)","Z\'(150 GeV)","Z\'(200 GeV)","Z\'(250 GeV)","Z\'(300 GeV)"]
		sigTags = ["Zprime50","Zprime100","Zprime150","Zprime200","Zprime250","Zprime300"];
		# sigXS = [139300.,19430.,5706.,2322.,1131.,619.];
		sigXS = [11.,10.,10.,10.,10.,10.]; # in pb

		for i in range(len(sigNames)):
			sigContainers.append( MCContainer( idir+"/"+sigNames[i], float(options.lumi)*sigXS[i]*1.2, sigLabels[i], sigTags[i], 1 ) );
			# k-factor is 1.2

	####################################################################################
	# do background estimation
	theRhalphabet = None;
	if options.doRhalphabet: 
		isData = True;
		theRhalphabet = rhalphabet(idir+"/"+"JetHT.root",1,"rhalphabet",1, False);
		theRhalphabet.GetPredictedDistributions( idir+"/"+"JetHT.root", 1, 5, isData);
		
		# there is a flag to do a closure test as well
		# isData = False;
		# theRhalphabet = rhalphabet(idir+"/"+"QCD.root",1,"rhalphabetClosure",1, False);
		# theRhalphabet.GetPredictedDistributions( idir+"/"+"QCD.root", 0.44, 10, isData );

	####################################################################################
	# do the loop on data
	theData = None;
	if options.doData:
		isData = True;
		theData = MCContainer( idir+"/"+"JetHT.root", 1, "data" ,"data" , 5, isData);

	####################################################################################
	# do some plotting
	if options.doCards: 
		buildDatacards(bkgContainers,sigContainers,theRhalphabet,theData);

	####################################################################################
	# do some plotting
	if options.doPlots: 
		BuildPlots(bkgContainers,sigContainers,theRhalphabet,theData);


def BuildPlots(bkgContainers,sigContainers,theRhalphabet,theData):

	print "making plots...";

	if options.doMCLooping:

		names = [];
		names.append( "h_jetmsd" );
		names.append( "h_jetmsd_passcut" );

		for n in names: 
	
			harray = [];
			hlabels = [];
			for b in bkgContainers: 
				harray.append( getattr( b, n ) );
				hlabels.append( b._name );
			for s in sigContainers: 
				harray.append( getattr( s, n ) );
				hlabels.append( s._name );

			makeCanvasComparison(harray,hlabels,"mc_"+n,"plots/yields/");
			makeCanvasShapeComparison(harray,hlabels,"mc_"+n,"plots/shapes/");


	if options.doMCLooping and options.doRhalphabet and options.doData: 

		makeCanvasDataMC_wpred( theData.h_jetmsd_passcut,
								theRhalphabet.grpred_jetmsd, 
								[bkgContainers[0].h_jetmsd_passcut],
								['qcd'],
								'jetmsd_pred',
								'plots/results/',
								False);

		makeCanvasDataMC_wpred( theData.h_rhoDDT_passcut,
								theRhalphabet.grpred_rhoDDT, 
								[bkgContainers[0].h_rhoDDT_passcut],
								['qcd'],
								'rhoDDT_pred',
								'plots/results/',
								False);


	# makeCanvasDataMC_wpred( bkgContainers[0].h_jetmsd_passcut,
	# 						theRhalphabet.grpred_jetmsd, 
	# 						[bkgContainers[0].h_jetmsd_passcut],
	# 						['qcd'],
	# 						'jetmsd_pred',
	# 						'plots/results/',
	# 						False);

	# makeCanvasDataMC_wpred( bkgContainers[0].h_rhoDDT_passcut,
	# 						theRhalphabet.grpred_rhoDDT, 
	# 						[bkgContainers[0].h_rhoDDT_passcut],
	# 						['qcd'],
	# 						'rhoDDT_pred',
	# 						'plots/results/',
	# 						False);






#----------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	main();
#----------------------------------------------------------------------------------------------------------------
