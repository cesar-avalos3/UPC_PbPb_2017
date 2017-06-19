// -*- C++ -*-
//
// Package:    ridge/ridge
// Class:      ridge
// 
/**\class ridge ridge.cc ridge/ridge/plugins/ridge.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
// 
// Original Author:  Cesar Avalos Baddouh
//         Created:  Thu, 08 Jun 2017 09:28:53 GMT
//
//


// TODO: More user control through untracked variables

// user include files
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

//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<> and also remove the line from
// constructor "usesResource("TFileService");"
// This will improve performance in multithreaded jobs.

class ridge : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
   public:
      explicit ridge(const edm::ParameterSet&);
      ~ridge(){};

   private:
      virtual void beginJob(){};
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob(){};

      TH1D *firstHistogram;
      TH1D *secondHistogram;
      TH1D *thirdHistogram;
      TH1D *fourthHistogram;
      TH2D *ridgeS;
      TH2D *ridgeB;     
      TH2D *ridgeF;

      edm::InputTag ptSource;
      edm::InputTag phiSource;
      edm::InputTag etaSource;

      std::vector<double> bphi_;
      std::vector<double> beta_;



      // ----------member data ---------------------------
};

ridge::ridge(const edm::ParameterSet& iConfig)
{
   //now do what ever initialization is needed

   ptSource  = edm::InputTag(iConfig.getUntrackedParameter<edm::InputTag>("ptSource_")); 
   etaSource = edm::InputTag(iConfig.getUntrackedParameter<edm::InputTag>("etaSource_"));
   phiSource = edm::InputTag(iConfig.getUntrackedParameter<edm::InputTag>("phiSource_"));

   consumes<std::vector<double>>(ptSource);
   consumes<std::vector<double>>(phiSource);
   consumes<std::vector<double>>(etaSource);

   edm::Service<TFileService> fs;

   firstHistogram  = fs->make<TH1D>("tracks", "Tracks", 100, 0, 5000);
   firstHistogram->Sumw2();
   secondHistogram = fs->make<TH1D>("pt", "Pt", 300, 0, 15);
   secondHistogram->Sumw2();
   thirdHistogram  = fs->make<TH1D>("eta","Eta",300,-4,4);
   thirdHistogram->Sumw2();
   fourthHistogram = fs->make<TH1D>("phi","Phi",300,-6,5);
   fourthHistogram->Sumw2();
   ridgeS = fs->make<TH2D>("ridge_signal","Signal",100,-10,10,100,-10,10);
	 ridgeS->Sumw2();
   ridgeB = fs->make<TH2D>("ridge_bkgrnd","Background",100,-10,10,100,-10,10); 
 	 ridgeB->Sumw2();
   ridgeF = fs->make<TH2D>("ridge_finale","Final",100,-10,10,100,-10,10);
   ridgeF->Sumw2();
}
  
// ------------ method called for each event  ------------
void
ridge::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;

  Handle<std::vector<double>> phiVector;
  Handle<std::vector<double>> etaVector;
  Handle<std::vector<double>>  ptVector;

  iEvent.getByLabel(phiSource, phiVector);
  iEvent.getByLabel(etaSource, etaVector);
  iEvent.getByLabel( ptSource,  ptVector);

  int eventSize = phiVector->size();

  for(int i = 0; i < eventSize; ++i)
  {

    // Signal Part
    for (int j = 0; j < eventSize; ++j)
    {
      if(i != j)
      {
        double DeltaPhi = (*phiVector)[i] - (*phiVector)[j];
        double DeltaEta = (*etaVector)[i] - (*etaVector)[j];
        ridgeS->Fill(DeltaPhi, DeltaEta);
      }
    }

    // Mix part
    for (int j = 0; j < i; ++j)
    {
        double DeltaPhi = (*phiVector)[i] - (*phiVector)[j];
        double DeltaEta = (*etaVector)[i] - (*phiVector)[j];
        ridgeB->Fill(DeltaPhi, DeltaEta);
    }

  } 
}

//define this as a plug-in
DEFINE_FWK_MODULE(ridge);
