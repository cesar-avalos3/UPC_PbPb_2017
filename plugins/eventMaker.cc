// 
// Original Author:  Cesar Avalos Baddouh
//         Created:  Thu, 08 Jun 2017 09:28:53 GMT
//
//
// The aim is to create a more modular UPC analyzer 

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "FWCore/Utilities/interface/InputTag.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH1.h"
#include "TH2.h"
#include "TMath.h"
//
// class declaration
//

class eventMaker : public edm::one::EDProducer<edm::one::SharedResources>  {
   public:
      explicit eventMaker(const edm::ParameterSet&);
      ~eventMaker();

   private:
      virtual void produce(edm::Event&, const edm::EventSetup&) override;

      edm::InputTag trackSource;
      edm::InputTag vertexSource;
      edm::InputTag nTtracksSource;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
eventMaker::eventMaker( const edm::ParameterSet& iConfig)
: trackSource(iConfig.getUntrackedParameter<edm::InputTag>("trackSource_")),
  vertexSource(iConfig.getUntrackedParameter<edm::InputTag>("vertexSource_")),
  nTracksSource(iConfig.getUntrackedParameter<edm::InputTag>("nTracksSource_"))
{
   //now do what ever initialization is needed
   consumes<reco::TrackCollection>(trackSource);
   consumes<reco::TrackCollection>(vertexSource);
   consumes<int>(nTracksSource);

   produces<std::vector<double> >("phi");
   produces<std::vector<double> >("eta");
   produces<std::vector<double> >("pt");


}

eventMaker::~eventMaker()
{ 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)
}


//
// member functions
//

// ------------ method called for each event  ------------
void
eventMaker::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;
  using namespace reco;

  std::auto_ptr<std::vector<double> > phiVector( new std::vector<double> );
  std::auto_ptr<std::vector<double> > etaVector( new std::vector<double> );
  std::auto_ptr<std::vector<double> >  ptVector( new std::vector<double> );

  Handle<int> nT;
  iEvent.getByLabel(nTracksSource, nT);
  int nTracks = *(nT.product());
  
  Handle<TrackCollection> tracks;
  iEvent.getByLabel(trackSource, tracks);
  
  // Loop through every track in the file
  for(TrackCollection::const_iterator itTrack = tracks->begin(); itTrack != tracks->end(); ++itTrack)
  {
  			if( itTrack->quality(TrackBase::highPurity) 
         && itTrack->pt() < 3.0  && TMath::Abs(itTrack->eta()) < 2.4)
  			{
  				phiVector->push_back(itTrack->phi());
  				etaVector->push_back(itTrack->eta());
  				ptVector->push_back(itTrack->pt());
  			}		
  } 

  iEvent.put(phiVector, std::string("phi"));
  iEvent.put(etaVector, std::string("eta"));
  iEvent.put( ptVector, std::string("pt") );

}

DEFINE_FWK_MODULE(eventMaker);