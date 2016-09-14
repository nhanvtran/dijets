import ROOT
from fullLims_1cat import getAsymLimits,makeAFillGraph,makeAGraph
from massplot import end,make2DGraph,avtotwidth,parser
import math,sys,time,os,glob,tdrstyle
from array import array
tdrstyle.setTDRStyle()
ROOT.gStyle.SetPadRightMargin(0.08);
ROOT.gStyle.SetPadLeftMargin(0.14);
ROOT.gStyle.SetPadTopMargin(0.10);
ROOT.gStyle.SetPalette(109);


def main():

	# read in the data: 
	fin = ROOT.TFile("limits_freq_qq_calodijet2016_pfdijet2016.root");

	obslo  = fin.Get("obs_qq_calodijet2016");
	explo1 = fin.Get("exp1sigma_qq_calodijet2016");
	explo2 = fin.Get("exp2sigma_qq_calodijet2016");

	obshi  = fin.Get("obs_qq_pfdijet2016");
	exphi1 = fin.Get("exp1sigma_qq_pfdijet2016");
	exphi2 = fin.Get("exp2sigma_qq_pfdijet2016");

	xs = dijetxs();
	obs_gq = getobs(obslo,obshi,xs);
	exp_gq, exp1s_gq = getexp(explo1,exphi1,xs);
	exp_gq_tmp2, exp2s_gq = getexp(explo2,exphi2,xs);

	exp_gq.SetLineStyle(2);
	exp1s_gq.SetFillStyle(1001);
	exp1s_gq.SetFillColor(3);
	exp2s_gq.SetFillStyle(1001);
	exp2s_gq.SetFillColor(5);

	#--------------------------------
	#--------------------------------
	# PLOTTING
	lowlim = 350;

	txta = ROOT.TLatex(0.16,0.92,"CMS"); txta.SetNDC();
	txtc = ROOT.TLatex(0.73,0.92,"12.9 fb^{-1} (13 TeV)");
	txtc.SetNDC(); txtc.SetTextFont(42); txtc.SetTextSize(0.04);
	
	leg = ROOT.TLegend(0.20,0.65,0.6,0.85);
	leg.SetFillStyle(0);
	leg.SetFillColor(0);    
	leg.SetBorderSize(0);
	leg.SetTextFont(42); 
	leg.AddEntry(obs_gq,"Observed, 95% CL Limit","l")
	leg.AddEntry(exp_gq,"Expected, 95% CL Limit","l")
	leg.AddEntry(exp1s_gq,"Expected, #pm 1 #sigma","f")
	leg.AddEntry(exp2s_gq,"Expected, #pm 2 #sigma","f")

	can_gB = ROOT.TCanvas("can_gB","can_gB",1200,800);
	hrl = can_gB.DrawFrame(lowlim,0,4001,0.45);
	hrl.GetYaxis().SetTitle("coupling g_{q}");
	hrl.GetYaxis().SetTitleOffset(1.0);
	hrl.GetXaxis().SetTitle("Z\' mass (GeV)");

	exp2s_gq.Draw("f");
	exp1s_gq.Draw("fsames");
	obs_gq.Draw("l");
	exp_gq.Draw("l");
	txta.Draw();
	txtc.Draw();
	leg.Draw();
	can_gB.SaveAs('limplotsHighMass/gB.pdf');

	hrl.GetXaxis().SetMoreLogLabels(True); 
	hrl.GetXaxis().SetNdivisions(10);      
	hrl.GetXaxis().SetNoExponent(True);   
	ROOT.gPad.SetLogx();
	can_gB.SaveAs('limplotsHighMass/gB_logx.pdf');	

def getobs(obslo,obshi,xs):

	x = [];
	y = [];

	for i in range( obslo.GetN() ):

		factor = xs.Eval( obslo.GetX()[i] ) / (5./6.); 

		x.append( obslo.GetX()[i] );
		y.append( math.sqrt( obslo.GetY()[i] / factor ) / 4. );

	for i in range( obshi.GetN() ):

		if obshi.GetX()[i] > 3700.: break;

		factor = xs.Eval( obshi.GetX()[i] ) / (5./6.);

		x.append( obshi.GetX()[i] );
		y.append( math.sqrt( obshi.GetY()[i] / factor ) / 4. );

	obs_gr = makeAGraph( x, y );
	
	return obs_gr

def getexp(explo,exphi,xs):

	x = [];
	y = [];
	yup = []; 
	ydn = []; 

	for i in range( explo.GetN() ):

		factor = xs.Eval( explo.GetX()[i] ) / (5./6.);
		cury   = explo.GetY()[i];
		curyup = explo.GetY()[i] + explo.GetEYhigh()[i];
		curydn = explo.GetY()[i] - explo.GetEYlow()[i];
		cury   /= factor;
		curyup /= factor;
		curydn /= factor;

		x.append( explo.GetX()[i] );
		y.append( math.sqrt(cury) / 4. );
		yup.append( math.sqrt(curyup) / 4. );
		ydn.append( math.sqrt(curydn) / 4. );

	for i in range( exphi.GetN() ):

		if exphi.GetX()[i] > 3700.: break;

		factor = xs.Eval( exphi.GetX()[i] ) / (5./6.);
		cury   = exphi.GetY()[i];
		curyup = exphi.GetY()[i] + exphi.GetEYhigh()[i];
		curydn = exphi.GetY()[i] - exphi.GetEYlow()[i];

		cury   /= factor;
		curyup /= factor;
		curydn /= factor;

		x.append( exphi.GetX()[i] );
		y.append( math.sqrt(cury) / 4. );
		yup.append( math.sqrt(curyup) / 4. );
		ydn.append( math.sqrt(curydn) / 4. );

	exp_gr = makeAGraph( x, y );
	exp_gr_band = makeAFillGraph( x, ydn, yup );

	return exp_gr, exp_gr_band


def dijetxs():

	## these cross-sections are for gq = 0.25
    x = array('d', [])
    y = array('d', [])
    x.append(528.7733914858716)
    y.append(57.269239965262344)
    x.append(631.2905390292997)
    y.append(26.146418729332762)
    x.append(795.7485275479014)
    y.append(10.943588903119819)
    x.append(980.9839334973528)
    y.append(4.998039360562294)
    x.append(1166.2193394468052)
    y.append(2.2826513012206147)
    x.append(1331.0361216730032)
    y.append(1.3151916426227461)
    x.append(1578.3102214269736)
    y.append(0.6008150098368491)
    x.append(1825.7147916200695)
    y.append(0.30829460763931776)
    x.append(2073.0541265936026)
    y.append(0.1492637583468037)
    x.append(2217.3544322672033)
    y.append(0.09943936422165509)
    x.append(2454.5170729888905)
    y.append(0.0556698333169542)
    x.append(2701.98687840155)
    y.append(0.03027483510044679)
    x.append(2928.9075896518298)
    y.append(0.018491825891702274)
    x.append(3104.1946246179077)
    y.append(0.011967992892333293)
    x.append(3310.4357712666806)
    y.append(0.007309405483957529)
    x.append(3475.513494371131)
    y.append(0.005313471607526083)
    x.append(3568.343211809438)
    y.append(0.004337281648532702)
    lGraph    = makeAGraph( x, y, 1, 3 )
    lGraph.SetMarkerColor(1)
    return lGraph

########################################################################################

def makeAGraph(listx,listy,linecolor = 1, linestyle = 1):

	a_m = array('d', []);
	a_g = array('d', []);

	for i in range(len(listx)):
		a_m.append(listx[i]);
		a_g.append(listy[i]);

	gr = ROOT.TGraph(len(listx),a_m,a_g);

	gr.SetLineColor(linecolor)
	gr.SetLineStyle(linestyle)
	gr.SetLineWidth(2)

	return gr

def makeAFillGraph(listx,listy1,listy2,linecolor = 1, fillcolor = 0, fillstyle = 0):

	a_m = array('d', []);
	a_g = array('d', []);

	for i in range(len(listx)):
		a_m.append(listx[i]);
		a_g.append(listy1[i]);
	
	for i in range(len(listx)-1,-1,-1):
		a_m.append(listx[i]);
		a_g.append(listy2[i]);

	gr = ROOT.TGraph(2*len(listx),a_m,a_g);

	gr.SetLineColor(linecolor)
	gr.SetFillColor(fillcolor)
	gr.SetFillStyle(fillstyle)

	return gr    

if __name__ == '__main__':
	
	main();