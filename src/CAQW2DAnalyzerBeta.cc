#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TMath.h"
#include <iostream>
#include <tuple>

using namespace std;

// This class is going to be the node class
class forwardListNode
{
	public:
	forwardListNode(vector<double>*, vector<double>*, vector<double>*, vector<double>*);
	vector<double> *phi;
	vector<double> *eta;
	vector<double> *vz;
	vector<double> *w;
};

forwardListNode::forwardListNode(vector<double> *p, vector<double> *e, vector<double> *z,vector<double> *we)
{
	phi = p;
	eta = e;
	vz  = z;
	we  = w;
}

class CAQW2DAnalyzerBeta : public edm::EDAnalyzer {
public:
	explicit CAQW2DAnalyzerBeta(const edm::ParameterSet&);
	~CAQW2DAnalyzerBeta() {};
private:
	virtual void beginJob() {};
	virtual void analyze(const edm::Event&, const edm::EventSetup&);
	virtual void endJob() {};

	edm::InputTag   srcPhi_;
	edm::InputTag   srcEta_;
	edm::InputTag   srcW_;
	edm::InputTag   srcVz_;
	TH1D * h;
  TH1D * histogramNumberBackgroundUsed;
  TH2D * hc;
  TH2D * hm;

	bool	bWeight;

	std::vector<double>	mphi_;
	std::vector<double>	meta_;
	std::vector<double>	mw_;
	std::vector<double> mz_;

	int eventNumber = 0;
	
	const double DphiMax = TMath::Pi() * 3/2;
	const double DphiMin = -TMath::Pi() / 2;

	vector<forwardListNode> temporaryVector;	
};


CAQW2DAnalyzerBeta::CAQW2DAnalyzerBeta(const edm::ParameterSet& pset)
{

	srcVz_ = pset.getUntrackedParameter<edm::InputTag>("srcVz");
  srcPhi_ = pset.getUntrackedParameter<edm::InputTag>("srcPhi");
  srcEta_ = pset.getUntrackedParameter<edm::InputTag>("srcEta");
  srcW_ = pset.getUntrackedParameter<edm::InputTag>("srcW", std::string("NA"));
  
  consumes<std::vector<double> >(srcPhi_);
	consumes<std::vector<double> >(srcEta_);
	consumes<std::vector<double> >(srcVz_);
	bWeight = false;

	if ( srcW_.label() != std::string("NA") ) {
		consumes<std::vector<double> >(srcW_);
		bWeight = true;
	}
	int hNbins  = pset.getUntrackedParameter<int>("hNbins");
	double hstart = pset.getUntrackedParameter<double>("hstart");
	double hend = pset.getUntrackedParameter<double>("hend");

	edm::Service<TFileService> fs;
	h = fs->make<TH1D>("h", "h", hNbins, hstart, hend);
	h->Sumw2();
	hc = fs->make<TH2D>("hc", "hc", 28, DphiMin, DphiMax, 28, -4.0, 4.0);
	hc->Sumw2();
	hm = fs->make<TH2D>("hm", "hm", 28, DphiMin, DphiMax, 28, -4.0, 4.0);
	hm->Sumw2();
}

void
CAQW2DAnalyzerBeta::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
	using namespace edm;
	Handle<std::vector<double> > phi;
	Handle<std::vector<double> > eta;
	Handle<std::vector<double> > w;
	Handle<std::vector<double> > vz;


  eventNumber++;
  int NTrigger = 0;

  TH2D *tempDPhi_signal = new TH2D("hc"+eventNumber, "hc"+eventNumber, 28, DphiMin, DphiMax, 28, -4.0, 4.0);
//  TH2D *tempDPhi_background = new TH2D("hm"+eventNumber, "hm"+eventNumber, 28, DphiMin, DphiMax, 28, -4.0, 4.0);

	iEvent.getByLabel(srcPhi_, phi);
 	iEvent.getByLabel(srcEta_, eta);
	iEvent.getByLabel(srcVz_,   vz);


	if ( bWeight ) {
		iEvent.getByLabel(srcW_, w);
	}

//	unsigned int numberOfBackgroundUsed = 0;

	int sz = phi->size();
	h->Fill(sz);
	for ( int i = 0; i < sz; i++ ) {
    NTrigger++;
		for ( int j = 0; j < sz; j++ ) {
			if ( i == j ) continue;
			double Dphi = (*phi)[i] - (*phi)[j];
			double Deta = (*eta)[i] - (*eta)[j];
			while (Dphi > DphiMax) Dphi -= TMath::Pi()*2.;
			while (Dphi < DphiMin) Dphi += TMath::Pi()*2.;

			if ( bWeight ) {
				tempDPhi_signal->Fill(Dphi, Deta, (*w)[i] * (*w)[j]);
			} else {
				tempDPhi_signal->Fill(Dphi, Deta);
			}
		}
		// DO MIX
		int tempVectorSize = temporaryVector.size();
		for(int j = 0; j < tempVectorSize; ++j){
      if(TMath::Abs( (*vz)[i] - (*(temporaryVector[j].vz))[0] ) <= 0.5){
      for(int u = 0; u < (*(temporaryVector[j].phi)).size(); ++u){
        double Dphi = (*phi)[i] - (*(temporaryVector[j].phi))[u];
        double Deta = (*eta)[i] - (*(temporaryVector[j].eta))[u];
        while (Dphi > DphiMax) Dphi -= TMath::Pi()*2.;
        while (Dphi < DphiMin) Dphi += TMath::Pi()*2.;
			  if ( bWeight ) {
		      hm->Fill(Dphi, Deta, (*w)[i] * (mw_)[j]);
        } else {
		      hm->Fill(Dphi, Deta); 
        }
      }
      }
		}
	}
	tempDPhi_signal->Sumw2();
//  tempDPhi_background->Sumw2();
  tempDPhi_signal->Multiply(1/NTrigger);
//  tempDPhi_background->Multiply(1/NTrigger);
  mphi_ = *phi;
	meta_ = *eta;
	mz_   = *vz;
	while(temporaryVector.size() > 40)
	{
		temporaryVector.pop_back();
	}
//	if ( bWeight ) {
//	    mw_ = *w;
//  }
  mw_ = *w;
  forwardListNode tempNode(&mphi_, &meta_, &mz_, &mw_);
  temporaryVector.insert(temporaryVector.begin(),tempNode);
  hc->Add(tempDPhi_signal);
//  hm->Add(tempDPhi_background);
  
//  delete tempDPhi_background;
  delete tempDPhi_signal;

	return;
}

DEFINE_FWK_MODULE(CAQW2DAnalyzerBeta);