import FWCore.ParameterSet.Config as cms

process = cms.Process("demo")


process.load("FWCore.MessageService.MessageLogger_cfi")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

# first filter:
process.load("HeavyIonsAnalysis.VertexAnalysis.PAPileUpVertexFilter_cff")
process.load("HeavyIonsAnalysis.Configuration.hfCoincFilter_cff")
#process.load("HeavyIonsAnalysis.EventAnalysis.pileUpFilter_cff")

process.PAprimaryVertexFilter = cms.EDFilter("VertexSelector",
    src = cms.InputTag("offlinePrimaryVertices"),
    cut = cms.string("!isFake && abs(z) <= 25 && position.Rho <= 2 && tracksSize >= 2"),
    filter = cms.bool(True), # otherwise it won't filter the events
)

process.NoScraping = cms.EDFilter("FilterOutScraping",
 applyfilter = cms.untracked.bool(True),
 debugOn = cms.untracked.bool(False),
 numtrack = cms.untracked.uint32(10),
 thresh = cms.untracked.double(0.25)
)

#HLT Trigger
import HLTrigger.HLTfilters.hltHighLevel_cfi

process.hltMB = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltMB.HLTPaths = ["HLT_HLT1MinimumBiasHF2AND_*", "HLT_HLT1MinimumBiasHF1AND_*", ]
process.hltMB.andOr = cms.bool(True)
process.hltMB.throw = cms.bool(False)

#This will call all the necessary filters
process.eventSelection = cms.Sequence(process.hfCoincFilter * process.PAprimaryVertexFilter * process.NoScraping)

#Load the array maker
process.eventMaker = cms.EDProducer("eventMaker", trackSource_ = cms.untracked.InputTag("generalTracks"),
						  			 vertexSource_ = cms.untracked.InputTag("vertex"))

#Load the histogram maker
process.demo = cms.EDAnalyzer('ridge', etaSource_ = cms.untracked.InputTag("eventMaker", "eta"),
									    ptSource_ = cms.untracked.InputTag("eventMaker", "pt"),
									   phiSource_ = cms.untracked.InputTag("eventMaker", "phi") )

#Load the offlineNTrack maker
process.offlineNTracks = cms.EDProducer("offlineNTracks", 
										trackSource_ = cms.untracked.InputTag("generalTracks"))

process.TFileService = cms.Service("TFileService",
        fileNamoe = cms.string("minBiasTrigger.root"))

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
    	'file:/afs/cern.ch/work/q/qwang/public/00647CA3-B2B3-E611-9F32-02163E01459C.root'
    )
)

process.load('RecoHI.HiCentralityAlgos.CentralityFilter_cfi')
process.ppNoffFilter240 = process.centralityFilter.clone(
		selectedBins = cms.vint32(
			*range(240, 260)
			),
		BinLabel = cms.InputTag("Noff")
		)

process.p = cms.Path(process.eventSelection * process.offlineNTracks * process.ppNoffFilter240 * process.eventMaker * process.demo)	