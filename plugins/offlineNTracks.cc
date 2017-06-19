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

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

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

class offlineNTracks : public edm::one::EDProducer<edm::one::SharedResources>  {
   public:
      explicit offlineNTracks(const edm::ParameterSet&);
      ~offlineNTracks();

   private:
      virtual void produce(edm::Event&, const edm::EventSetup&) override;

      edm::InputTag trackSource;
      edm::InputTag vertexSource;
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
offlineNTracks::offlineNTracks( const edm::ParameterSet& iConfig)
: trackSource(iConfig.getUntrackedParameter<edm::InputTag>("trackSource_")),
  vertexSource(iConfig.getUntrackedParameter<edm::InputTag>("vertexSource_"))
{
   //now do what ever initialization is needed
   consumes<reco::TrackCollection>(trackSource);
   consumes<reco::VertexCollection>(vertexSource);
   produces<std::auto_ptr<int>>("pNoff");
}

offlineNTracks::~offlineNTracks()
{ 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)
}


//
// member functions
//

// ------------ method called for each event  ------------
void
offlineNTracks::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;
  using namespace reco;

  Handle<TrackCollection> tracks;
  iEvent.getByLabel(trackSource, tracks);

  Handle<VertexCollection> vertices;
  iEvent.getByLabel(vertexSource, vertices);
  VertexCollection recoVertices = *vertices;

  sort(recoVertices.begin(), recoVertices.end(), [](const reco::Vertex &a, const reco::Vertex &b){
			return a.tracksSize() > b.tracksSize();
			});
  int primaryvtx = 0;
  math::XYZPoint v1( recoVertices[primaryvtx].position().x(), recoVertices[primaryvtx].position().y(), recoVertices[primaryvtx].position().z() );
  double vxError = recoVertices[primaryvtx].xError();
  double vyError = recoVertices[primaryvtx].yError();
  double vzError = recoVertices[primaryvtx].zError();
  
  int NTracks = 0;

  // Loop through every track in the file
  for(TrackCollection::const_iterator itTrack = tracks->begin(); itTrack != tracks->end(); ++itTrack)
  {
  			if( itTrack->quality(TrackBase::highPurity) && itTrack->charge() == 0 
  			 && (itTrack->ptError() / itTrack->pt() > 0.1)  && TMath::Abs(itTrack->eta()) > 2.4)
  			{
  				double d0 = -1.* itTrack->dxy(v1);
				double derror=sqrt(itTrack->dxyError()*itTrack->dxyError()+vxError*vyError);
				double dz=itTrack->dz(v1);
				double dzerror=sqrt(itTrack->dzError()*itTrack->dzError()+vzError*vzError);
				if(TMath::Abs(dz/dzerror) > 3 && TMath::Abs(d0/dzerror) > 3 )
				{
	  				NTracks++;
				}
  			}
  } 
  std::auto_ptr<int> pNoff(new int(NTracks));
  iEvent.put(pNoff);
}

DEFINE_FWK_MODULE(offlineNTracks);