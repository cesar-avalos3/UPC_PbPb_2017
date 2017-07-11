import FWCore.ParameterSet.Config as cms

process = cms.Process("PCA")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring('ProductNotFound')
)

process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring("file:/afs/cern.ch/work/q/qwang/public/00647CA3-B2B3-E611-9F32-02163E01459C.root")
)

# We are going to forego this here fella
#import HLTrigger.HLTfilters.hltHighLevel_cfi
#process.hltMB = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
#process.hltMB.HLTPaths = [
#	"HLT_HIL1MinimumBiasHF2AND_*",
#	"HLT_HIL1MinimumBiasHF1AND_*",
#]
#process.hltMB.andOr = cms.bool(True)
#process.hltMB.throw = cms.bool(False)

import HLTrigger.HLTfilters.hltHighLevel_cfi
process.hltHM120 = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltHM120.HLTPaths = [
	"HLT_PAFullTracks_Multiplicity120_v*",
#	"HLT_PAFullTracks_Multiplicity150_v*",
#	"HLT_PAFullTracks_Multiplicity185_*",
#	"HLT_PAFullTracks_Multiplicity220_v*",
#	"HLT_PAFullTracks_Multiplicity250_v*",
#	"HLT_PAFullTracks_Multiplicity280_v*",
]
process.hltHM120.andOr = cms.bool(True)
process.hltHM120.throw = cms.bool(False)

process.hltHM150 = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltHM150.HLTPaths = [
	"HLT_PAFullTracks_Multiplicity120_v*",
	"HLT_PAFullTracks_Multiplicity150_v*",
#	"HLT_PAFullTracks_Multiplicity185_*",
#	"HLT_PAFullTracks_Multiplicity220_v*",
#	"HLT_PAFullTracks_Multiplicity250_v*",
#	"HLT_PAFullTracks_Multiplicity280_v*",
]
process.hltHM150.andOr = cms.bool(True)
process.hltHM150.throw = cms.bool(False)

process.hltHM185 = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltHM185.HLTPaths = [
#	"HLT_PAFullTracks_Multiplicity120_v*",
#	"HLT_PAFullTracks_Multiplicity150_v*",
	"HLT_PAFullTracks_Multiplicity185_*",
#	"HLT_PAFullTracks_Multiplicity220_v*",
#	"HLT_PAFullTracks_Multiplicity250_v*",
#	"HLT_PAFullTracks_Multiplicity280_v*",
]
process.hltHM185.andOr = cms.bool(True)
process.hltHM185.throw = cms.bool(False)

process.hltHM250 = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltHM250.HLTPaths = [
#	"HLT_PAFullTracks_Multiplicity120_v*",
#	"HLT_PAFullTracks_Multiplicity150_v*",
#	"HLT_PAFullTracks_Multiplicity185_*",
#	"HLT_PAFullTracks_Multiplicity220_v*",
	"HLT_PAFullTracks_Multiplicity250*_v*",
#	"HLT_PAFullTracks_Multiplicity280_v*",
]
process.hltHM250.andOr = cms.bool(True)
process.hltHM250.throw = cms.bool(False)


process.hltHM280 = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltHM280.HLTPaths = [
        "HLT_PAFullTracks_Multiplicity250*_v*",
]
process.hltHM280.andOr = cms.bool(True)
process.hltHM280.throw = cms.bool(False)


process.TFileService = cms.Service("TFileService",
    fileName = cms.string('thatsTheJoke.root')
)

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

process.load("HeavyIonsAnalysis.Configuration.hfCoincFilter_cff")
#process.load("HeavyIonsAnalysis.EventAnalysis.pileUpFilter_cff")

#process.eventSelection = cms.Sequence(process.hfCoincFilter * process.PAprimaryVertexFilter * process.NoScraping * process.olvFilter_pPb8TeV_dz1p0)
process.eventSelection = cms.Sequence(process.hfCoincFilter * process.PAprimaryVertexFilter * process.NoScraping )

process.load('RecoHI.HiCentralityAlgos.CentralityFilter_cfi')
process.ppNoffFilter120 = process.centralityFilter.clone(
		selectedBins = cms.vint32(
			*range(120, 150)
			),
		BinLabel = cms.InputTag("Noff")
		)

process.ppNoffFilter150 = process.centralityFilter.clone(
		selectedBins = cms.vint32(
			*range(150, 185)
			),
		BinLabel = cms.InputTag("Noff")
		)

process.ppNoffFilter185 = process.centralityFilter.clone(
		selectedBins = cms.vint32(
			*range(185, 250)
			),
		BinLabel = cms.InputTag("Noff")
		)

process.ppNoffFilter250 = process.centralityFilter.clone(
		selectedBins = cms.vint32(
			*range(250, 600)
			),
		BinLabel = cms.InputTag("Noff")
		)

process.ppNoffFilter360 = process.centralityFilter.clone(
                selectedBins = cms.vint32(
                        *range(330, 360)
                        ),
                BinLabel = cms.InputTag("Noff")
                )

process.load('pPb_HM_eff')
process.QWEvent.fweight = cms.untracked.InputTag('Hijing_8TeV_dataBS.root')
process.QWEvent.ptMin = cms.untracked.double(1.0)


process.corr2D120 = cms.EDAnalyzer('CAQW2DAnalyzer',
		srcPhi = cms.untracked.InputTag("QWEvent", "phi"),
		srcVz  = cms.untracked.InputTag("QWEvent",  "vz"),
		srcEta = cms.untracked.InputTag("QWEvent", "eta"),
    hNbins = cms.untracked.int32(5000),
    hstart = cms.untracked.double(0),
    hend = cms.untracked.double(5000),
		)

process.corr2D150 = process.corr2D120.clone()
process.corr2D185 = process.corr2D120.clone()
process.corr2D250 = process.corr2D120.clone()
process.corr2D360 = process.corr2D120.clone()

process.path120 = cms.Path(process.hltHM120 * process.eventSelection*process.Noff * process.ppNoffFilter120 * process.QWEvent * process.vectMon * process.corr2D120)
process.path150 = cms.Path(process.hltHM150 * process.eventSelection*process.Noff * process.ppNoffFilter150 * process.QWEvent * process.vectMon * process.corr2D150)
process.path185 = cms.Path(process.hltHM185 * process.eventSelection*process.Noff * process.ppNoffFilter185 * process.QWEvent * process.vectMon * process.corr2D185)
process.path250 = cms.Path(process.hltHM250 * process.eventSelection*process.Noff * process.ppNoffFilter250 * process.QWEvent * process.vectMon * process.corr2D250)
process.path360 = cms.Path(process.hltHM250 * process.eventSelection*process.Noff * process.ppNoffFilter360 * process.QWEvent * process.vectMon * process.corr2D360)

process.schedule = cms.Schedule(
	process.path120,
	process.path150,
	process.path185,
	process.path250,
	process.path360,
)
