import FWCore.ParameterSet.Config as cms

process = cms.Process("PCA")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:/afs/cern.ch/work/q/qwang/public/00647CA3-B2B3-E611-9F32-02163E01459C.root')
)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring('ProductNotFound')
)

process.MEtoEDMConverter = cms.EDProducer("MEtoEDMConverter",
    Frequency = cms.untracked.int32(50),
    MEPathToSave = cms.untracked.string(''),
    Name = cms.untracked.string('MEtoEDMConverter'),
    Verbosity = cms.untracked.int32(0),
    deleteAfterCopy = cms.untracked.bool(True)
)


process.Noff = cms.EDProducer("QWNtrkOfflineProducer",
    trackSrc = cms.untracked.InputTag("generalTracks"),
    vertexSrc = cms.untracked.InputTag("offlinePrimaryVertices")
)


process.QWEvent = cms.EDProducer("QWEventProducer",
    Etamax = cms.untracked.double(2.4),
    Etamin = cms.untracked.double(-2.4),
    centralitySrc = cms.untracked.InputTag("Noff"),
    d0d0error = cms.untracked.double(3.0),
    dzdzerror = cms.untracked.double(3.0),
    fweight = cms.untracked.InputTag("NA"),
    ptMax = cms.untracked.double(3.0),
    ptMin = cms.untracked.double(0.3),
    pterrorpt = cms.untracked.double(0.1),
    trackSrc = cms.untracked.InputTag("generalTracks"),
    vertexSrc = cms.untracked.InputTag("offlinePrimaryVertices")
)


process.randomEngineStateProducer = cms.EDProducer("RandomEngineStateProducer")


process.towersAboveThreshold = cms.EDProducer("CaloTowerCandidateCreator",
    minimumE = cms.double(3.0),
    minimumEt = cms.double(0.0),
    src = cms.InputTag("towerMaker"),
    verbose = cms.untracked.int32(0)
)


process.NoScraping = cms.EDFilter("FilterOutScraping",
    applyfilter = cms.untracked.bool(True),
    debugOn = cms.untracked.bool(False),
    numtrack = cms.untracked.uint32(10),
    thresh = cms.untracked.double(0.25)
)


process.PAprimaryVertexFilter = cms.EDFilter("VertexSelector",
    cut = cms.string('!isFake && abs(z) <= 25 && position.Rho <= 2 && tracksSize >= 2'),
    filter = cms.bool(True),
    src = cms.InputTag("offlinePrimaryVertices")
)


process.centralityFilter = cms.EDFilter("CentralityFilter",
    BinLabel = cms.InputTag("centralityBin","HFtowers"),
    selectedBins = cms.vint32(0)
)


process.hfNegFilter = cms.EDFilter("CandCountFilter",
    minNumber = cms.uint32(1),
    src = cms.InputTag("hfNegTowers")
)


process.hfNegFilter2 = cms.EDFilter("CandCountFilter",
    minNumber = cms.uint32(2),
    src = cms.InputTag("hfNegTowers")
)


process.hfNegFilter3 = cms.EDFilter("CandCountFilter",
    minNumber = cms.uint32(3),
    src = cms.InputTag("hfNegTowers")
)


process.hfNegFilter4 = cms.EDFilter("CandCountFilter",
    minNumber = cms.uint32(4),
    src = cms.InputTag("hfNegTowers")
)


process.hfNegFilter5 = cms.EDFilter("CandCountFilter",
    minNumber = cms.uint32(5),
    src = cms.InputTag("hfNegTowers")
)


process.hfNegTowers = cms.EDFilter("EtaPtMinCandSelector",
    etaMax = cms.double(-3.0),
    etaMin = cms.double(-6.0),
    ptMin = cms.double(0),
    src = cms.InputTag("towersAboveThreshold")
)


process.hfPosFilter = cms.EDFilter("CandCountFilter",
    minNumber = cms.uint32(1),
    src = cms.InputTag("hfPosTowers")
)


process.hfPosFilter2 = cms.EDFilter("CandCountFilter",
    minNumber = cms.uint32(2),
    src = cms.InputTag("hfPosTowers")
)


process.hfPosFilter3 = cms.EDFilter("CandCountFilter",
    minNumber = cms.uint32(3),
    src = cms.InputTag("hfPosTowers")
)


process.hfPosFilter4 = cms.EDFilter("CandCountFilter",
    minNumber = cms.uint32(4),
    src = cms.InputTag("hfPosTowers")
)


process.hfPosFilter5 = cms.EDFilter("CandCountFilter",
    minNumber = cms.uint32(5),
    src = cms.InputTag("hfPosTowers")
)


process.hfPosTowers = cms.EDFilter("EtaPtMinCandSelector",
    etaMax = cms.double(6.0),
    etaMin = cms.double(3.0),
    ptMin = cms.double(0),
    src = cms.InputTag("towersAboveThreshold")
)


process.hltHM120 = cms.EDFilter("HLTHighLevel",
    HLTPaths = cms.vstring('HLT_PAFullTracks_Multiplicity120_v*'),
    TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
    andOr = cms.bool(True),
    eventSetupPathsKey = cms.string(''),
    throw = cms.bool(False)
)


process.hltHM150 = cms.EDFilter("HLTHighLevel",
    HLTPaths = cms.vstring('HLT_PAFullTracks_Multiplicity120_v*', 
        'HLT_PAFullTracks_Multiplicity150_v*'),
    TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
    andOr = cms.bool(True),
    eventSetupPathsKey = cms.string(''),
    throw = cms.bool(False)
)


process.hltHM185 = cms.EDFilter("HLTHighLevel",
    HLTPaths = cms.vstring('HLT_PAFullTracks_Multiplicity185_*'),
    TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
    andOr = cms.bool(True),
    eventSetupPathsKey = cms.string(''),
    throw = cms.bool(False)
)


process.hltHM250 = cms.EDFilter("HLTHighLevel",
    HLTPaths = cms.vstring('HLT_PAFullTracks_Multiplicity250*_v*'),
    TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
    andOr = cms.bool(True),
    eventSetupPathsKey = cms.string(''),
    throw = cms.bool(False)
)


process.hltHM280 = cms.EDFilter("HLTHighLevel",
    HLTPaths = cms.vstring('HLT_PAFullTracks_Multiplicity250*_v*'),
    TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
    andOr = cms.bool(True),
    eventSetupPathsKey = cms.string(''),
    throw = cms.bool(False)
)


process.ppNoffFilter120 = cms.EDFilter("CentralityFilter",
    BinLabel = cms.InputTag("Noff"),
    selectedBins = cms.vint32(120, 121, 122, 123, 124, 
        125, 126, 127, 128, 129, 
        130, 131, 132, 133, 134, 
        135, 136, 137, 138, 139, 
        140, 141, 142, 143, 144, 
        145, 146, 147, 148, 149)
)


process.ppNoffFilter150 = cms.EDFilter("CentralityFilter",
    BinLabel = cms.InputTag("Noff"),
    selectedBins = cms.vint32(150, 151, 152, 153, 154, 
        155, 156, 157, 158, 159, 
        160, 161, 162, 163, 164, 
        165, 166, 167, 168, 169, 
        170, 171, 172, 173, 174, 
        175, 176, 177, 178, 179, 
        180, 181, 182, 183, 184)
)


process.ppNoffFilter185 = cms.EDFilter("CentralityFilter",
    BinLabel = cms.InputTag("Noff"),
    selectedBins = cms.vint32(185, 186, 187, 188, 189, 
        190, 191, 192, 193, 194, 
        195, 196, 197, 198, 199, 
        200, 201, 202, 203, 204, 
        205, 206, 207, 208, 209, 
        210, 211, 212, 213, 214, 
        215, 216, 217, 218, 219, 
        220, 221, 222, 223, 224, 
        225, 226, 227, 228, 229, 
        230, 231, 232, 233, 234, 
        235, 236, 237, 238, 239, 
        240, 241, 242, 243, 244, 
        245, 246, 247, 248, 249)
)


process.ppNoffFilter250 = cms.EDFilter("CentralityFilter",
    BinLabel = cms.InputTag("Noff"),
    selectedBins = cms.vint32( (250, 251, 252, 253, 254, 
        255, 256, 257, 258, 259, 
        260, 261, 262, 263, 264, 
        265, 266, 267, 268, 269, 
        270, 271, 272, 273, 274, 
        275, 276, 277, 278, 279, 
        280, 281, 282, 283, 284, 
        285, 286, 287, 288, 289, 
        290, 291, 292, 293, 294, 
        295, 296, 297, 298, 299, 
        300, 301, 302, 303, 304, 
        305, 306, 307, 308, 309, 
        310, 311, 312, 313, 314, 
        315, 316, 317, 318, 319, 
        320, 321, 322, 323, 324, 
        325, 326, 327, 328, 329, 
        330, 331, 332, 333, 334, 
        335, 336, 337, 338, 339, 
        340, 341, 342, 343, 344, 
        345, 346, 347, 348, 349, 
        350, 351, 352, 353, 354, 
        355, 356, 357, 358, 359, 
        360, 361, 362, 363, 364, 
        365, 366, 367, 368, 369, 
        370, 371, 372, 373, 374, 
        375, 376, 377, 378, 379, 
        380, 381, 382, 383, 384, 
        385, 386, 387, 388, 389, 
        390, 391, 392, 393, 394, 
        395, 396, 397, 398, 399, 
        400, 401, 402, 403, 404, 
        405, 406, 407, 408, 409, 
        410, 411, 412, 413, 414, 
        415, 416, 417, 418, 419, 
        420, 421, 422, 423, 424, 
        425, 426, 427, 428, 429, 
        430, 431, 432, 433, 434, 
        435, 436, 437, 438, 439, 
        440, 441, 442, 443, 444, 
        445, 446, 447, 448, 449, 
        450, 451, 452, 453, 454, 
        455, 456, 457, 458, 459, 
        460, 461, 462, 463, 464, 
        465, 466, 467, 468, 469, 
        470, 471, 472, 473, 474, 
        475, 476, 477, 478, 479, 
        480, 481, 482, 483, 484, 
        485, 486, 487, 488, 489, 
        490, 491, 492, 493, 494, 
        495, 496, 497, 498, 499, 
        500, 501, 502, 503, 504, 
        505, 506, 507, 508, 509, 
        510, 511, 512, 513, 514, 
        515, 516, 517, 518, 519, 
        520, 521, 522, 523, 524, 
        525, 526, 527, 528, 529, 
        530, 531, 532, 533, 534, 
        535, 536, 537, 538, 539, 
        540, 541, 542, 543, 544, 
        545, 546, 547, 548, 549, 
        550, 551, 552, 553, 554, 
        555, 556, 557, 558, 559, 
        560, 561, 562, 563, 564, 
        565, 566, 567, 568, 569, 
        570, 571, 572, 573, 574, 
        575, 576, 577, 578, 579, 
        580, 581, 582, 583, 584, 
        585, 586, 587, 588, 589, 
        590, 591, 592, 593, 594, 
        595, 596, 597, 598, 599 ) )
)


process.ppNoffFilter360 = cms.EDFilter("CentralityFilter",
    BinLabel = cms.InputTag("Noff"),
    selectedBins = cms.vint32(330, 331, 332, 333, 334, 
        335, 336, 337, 338, 339, 
        340, 341, 342, 343, 344, 
        345, 346, 347, 348, 349, 
        350, 351, 352, 353, 354, 
        355, 356, 357, 358, 359)
)


process.MEtoMEComparitor = cms.EDAnalyzer("MEtoMEComparitor",
    Diffgoodness = cms.double(0.1),
    KSgoodness = cms.double(0.9),
    MEtoEDMLabel = cms.string('MEtoEDMConverter'),
    OverAllgoodness = cms.double(0.9),
    autoProcess = cms.bool(True),
    dirDepth = cms.uint32(1),
    lumiInstance = cms.string('MEtoEDMConverterLumi'),
    processNew = cms.string('RERECO'),
    processRef = cms.string('HLT'),
    runInstance = cms.string('MEtoEDMConverterRun')
)


process.corr2D120 = cms.EDAnalyzer("CAQW2DAnalyzer",
    hNbins = cms.untracked.int32(5000),
    hend = cms.untracked.double(5000),
    hstart = cms.untracked.double(0),
    srcEta = cms.untracked.InputTag("QWEvent","eta"),
    srcPhi = cms.untracked.InputTag("QWEvent","phi"),
    srcVz = cms.untracked.InputTag("QWEvent","vz")
)


process.corr2D150 = cms.EDAnalyzer("CAQW2DAnalyzer",
    hNbins = cms.untracked.int32(5000),
    hend = cms.untracked.double(5000),
    hstart = cms.untracked.double(0),
    srcEta = cms.untracked.InputTag("QWEvent","eta"),
    srcPhi = cms.untracked.InputTag("QWEvent","phi"),
    srcVz = cms.untracked.InputTag("QWEvent","vz")
)


process.corr2D185 = cms.EDAnalyzer("CAQW2DAnalyzer",
    hNbins = cms.untracked.int32(5000),
    hend = cms.untracked.double(5000),
    hstart = cms.untracked.double(0),
    srcEta = cms.untracked.InputTag("QWEvent","eta"),
    srcPhi = cms.untracked.InputTag("QWEvent","phi"),
    srcVz = cms.untracked.InputTag("QWEvent","vz")
)


process.corr2D250 = cms.EDAnalyzer("CAQW2DAnalyzer",
    hNbins = cms.untracked.int32(5000),
    hend = cms.untracked.double(5000),
    hstart = cms.untracked.double(0),
    srcEta = cms.untracked.InputTag("QWEvent","eta"),
    srcPhi = cms.untracked.InputTag("QWEvent","phi"),
    srcVz = cms.untracked.InputTag("QWEvent","vz")
)


process.corr2D360 = cms.EDAnalyzer("CAQW2DAnalyzer",
    hNbins = cms.untracked.int32(5000),
    hend = cms.untracked.double(5000),
    hstart = cms.untracked.double(0),
    srcEta = cms.untracked.InputTag("QWEvent","eta"),
    srcPhi = cms.untracked.InputTag("QWEvent","phi"),
    srcVz = cms.untracked.InputTag("QWEvent","vz")
)


process.histNoff = cms.EDAnalyzer("QWHistAnalyzer",
    Nbins = cms.untracked.int32(600),
    end = cms.untracked.double(600),
    src = cms.untracked.InputTag("Noff"),
    start = cms.untracked.double(0)
)


process.vectEta = cms.EDAnalyzer("QWVectorAnalyzer",
    cNbins = cms.untracked.int32(1000),
    cend = cms.untracked.double(2.5),
    cstart = cms.untracked.double(-2.5),
    hNbins = cms.untracked.int32(5000),
    hend = cms.untracked.double(5000),
    hstart = cms.untracked.double(0),
    src = cms.untracked.InputTag("QWEvent","eta")
)


process.vectEtaW = cms.EDAnalyzer("QWVectorAnalyzer",
    cNbins = cms.untracked.int32(1000),
    cend = cms.untracked.double(2.5),
    cstart = cms.untracked.double(-2.5),
    hNbins = cms.untracked.int32(5000),
    hend = cms.untracked.double(5000),
    hstart = cms.untracked.double(0),
    src = cms.untracked.InputTag("QWEvent","eta"),
    srcW = cms.untracked.InputTag("QWEvent","weight")
)


process.vectPhi = cms.EDAnalyzer("QWVectorAnalyzer",
    cNbins = cms.untracked.int32(1000),
    cend = cms.untracked.double(3.14159265359),
    cstart = cms.untracked.double(-3.14159265359),
    hNbins = cms.untracked.int32(5000),
    hend = cms.untracked.double(5000),
    hstart = cms.untracked.double(0),
    src = cms.untracked.InputTag("QWEvent","phi")
)


process.vectPhiW = cms.EDAnalyzer("QWVectorAnalyzer",
    cNbins = cms.untracked.int32(1000),
    cend = cms.untracked.double(3.14159265359),
    cstart = cms.untracked.double(-3.14159265359),
    hNbins = cms.untracked.int32(5000),
    hend = cms.untracked.double(5000),
    hstart = cms.untracked.double(0),
    src = cms.untracked.InputTag("QWEvent","phi"),
    srcW = cms.untracked.InputTag("QWEvent","weight")
)


process.vectPt = cms.EDAnalyzer("QWVectorAnalyzer",
    cNbins = cms.untracked.int32(1000),
    cend = cms.untracked.double(5),
    cstart = cms.untracked.double(0),
    hNbins = cms.untracked.int32(5000),
    hend = cms.untracked.double(5000),
    hstart = cms.untracked.double(0),
    src = cms.untracked.InputTag("QWEvent","pt")
)


process.vectPtW = cms.EDAnalyzer("QWVectorAnalyzer",
    cNbins = cms.untracked.int32(1000),
    cend = cms.untracked.double(5),
    cstart = cms.untracked.double(0),
    hNbins = cms.untracked.int32(5000),
    hend = cms.untracked.double(5000),
    hstart = cms.untracked.double(0),
    src = cms.untracked.InputTag("QWEvent","pt"),
    srcW = cms.untracked.InputTag("QWEvent","weight")
)


process.hfCoincFilter5 = cms.Sequence(process.towersAboveThreshold+process.hfPosTowers+process.hfNegTowers+process.hfPosFilter5+process.hfNegFilter5)


process.hfCoincFilter = cms.Sequence(process.towersAboveThreshold+process.hfPosTowers+process.hfNegTowers+process.hfPosFilter+process.hfNegFilter)


process.eventSelection = cms.Sequence(process.hfCoincFilter+process.PAprimaryVertexFilter+process.NoScraping)


process.endOfProcess_withComparison = cms.Sequence(process.MEtoEDMConverter+process.MEtoMEComparitor)


process.endOfProcess = cms.Sequence(process.MEtoEDMConverter)


process.hfposTowers = cms.Sequence(process.towersAboveThreshold+process.hfPosTowers)


process.vectMonW = cms.Sequence(process.histNoff+process.vectPhi+process.vectPt+process.vectEta+process.vectPhiW+process.vectPtW+process.vectEtaW)


process.makeEvent = cms.Sequence(process.Noff+process.QWEvent)


process.vectMon = cms.Sequence(process.histNoff+process.vectPhi+process.vectPt+process.vectEta)


process.hfnegTowers = cms.Sequence(process.towersAboveThreshold+process.hfNegTowers)


process.hfCoincFilter4 = cms.Sequence(process.towersAboveThreshold+process.hfPosTowers+process.hfNegTowers+process.hfPosFilter4+process.hfNegFilter4)


process.hfnegFilter = cms.Sequence(process.hfnegTowers+process.hfNegFilter)


process.hfposFilter4 = cms.Sequence(process.hfposTowers+process.hfPosFilter4)


process.hfposFilter5 = cms.Sequence(process.hfposTowers+process.hfPosFilter5)


process.hfposFilter2 = cms.Sequence(process.hfposTowers+process.hfPosFilter2)


process.hfnegFilter5 = cms.Sequence(process.hfnegTowers+process.hfNegFilter5)


process.hfCoincFilter2 = cms.Sequence(process.towersAboveThreshold+process.hfPosTowers+process.hfNegTowers+process.hfPosFilter2+process.hfNegFilter2)


process.hfCoincFilter3 = cms.Sequence(process.towersAboveThreshold+process.hfPosTowers+process.hfNegTowers+process.hfPosFilter3+process.hfNegFilter3)


process.hfnegFilter2 = cms.Sequence(process.hfnegTowers+process.hfNegFilter2)


process.hfnegFilter3 = cms.Sequence(process.hfnegTowers+process.hfNegFilter3)


process.hfposFilter = cms.Sequence(process.hfposTowers+process.hfPosFilter)


process.hfnegFilter4 = cms.Sequence(process.hfnegTowers+process.hfNegFilter4)


process.hfposFilter3 = cms.Sequence(process.hfposTowers+process.hfPosFilter3)


process.path120 = cms.Path(process.hltHM120+process.eventSelection+process.Noff+process.ppNoffFilter120+process.QWEvent+process.vectMon+process.corr2D120)


process.path150 = cms.Path(process.hltHM150+process.eventSelection+process.Noff+process.ppNoffFilter150+process.QWEvent+process.vectMon+process.corr2D150)


process.path185 = cms.Path(process.hltHM185+process.eventSelection+process.Noff+process.ppNoffFilter185+process.QWEvent+process.vectMon+process.corr2D185)


process.path250 = cms.Path(process.hltHM250+process.eventSelection+process.Noff+process.ppNoffFilter250+process.QWEvent+process.vectMon+process.corr2D250)


process.path360 = cms.Path(process.hltHM250+process.eventSelection+process.Noff+process.ppNoffFilter360+process.QWEvent+process.vectMon+process.corr2D360)


process.DQMStore = cms.Service("DQMStore")


process.MessageLogger = cms.Service("MessageLogger",
    FrameworkJobReport = cms.untracked.PSet(
        FwkJob = cms.untracked.PSet(
            limit = cms.untracked.int32(10000000),
            optionalPSet = cms.untracked.bool(True)
        ),
        default = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        optionalPSet = cms.untracked.bool(True)
    ),
    categories = cms.untracked.vstring('FwkJob', 
        'FwkReport', 
        'FwkSummary', 
        'Root_NoDictionary'),
    cerr = cms.untracked.PSet(
        FwkJob = cms.untracked.PSet(
            limit = cms.untracked.int32(0),
            optionalPSet = cms.untracked.bool(True)
        ),
        FwkReport = cms.untracked.PSet(
            limit = cms.untracked.int32(10000000),
            optionalPSet = cms.untracked.bool(True),
            reportEvery = cms.untracked.int32(100)
        ),
        FwkSummary = cms.untracked.PSet(
            limit = cms.untracked.int32(10000000),
            optionalPSet = cms.untracked.bool(True),
            reportEvery = cms.untracked.int32(1)
        ),
        INFO = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        Root_NoDictionary = cms.untracked.PSet(
            limit = cms.untracked.int32(0),
            optionalPSet = cms.untracked.bool(True)
        ),
        default = cms.untracked.PSet(
            limit = cms.untracked.int32(10000000)
        ),
        noTimeStamps = cms.untracked.bool(False),
        optionalPSet = cms.untracked.bool(True),
        threshold = cms.untracked.string('INFO')
    ),
    cerr_stats = cms.untracked.PSet(
        optionalPSet = cms.untracked.bool(True),
        output = cms.untracked.string('cerr'),
        threshold = cms.untracked.string('WARNING')
    ),
    cout = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    ),
    debugModules = cms.untracked.vstring(),
    debugs = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    ),
    default = cms.untracked.PSet(

    ),
    destinations = cms.untracked.vstring('warnings', 
        'errors', 
        'infos', 
        'debugs', 
        'cout', 
        'cerr'),
    errors = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    ),
    fwkJobReports = cms.untracked.vstring('FrameworkJobReport'),
    infos = cms.untracked.PSet(
        Root_NoDictionary = cms.untracked.PSet(
            limit = cms.untracked.int32(0),
            optionalPSet = cms.untracked.bool(True)
        ),
        optionalPSet = cms.untracked.bool(True),
        placeholder = cms.untracked.bool(True)
    ),
    statistics = cms.untracked.vstring('cerr_stats'),
    suppressDebug = cms.untracked.vstring(),
    suppressInfo = cms.untracked.vstring(),
    suppressWarning = cms.untracked.vstring(),
    warnings = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    )
)


process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
    LHCTransport = cms.PSet(
        engineName = cms.untracked.string('TRandom3'),
        initialSeed = cms.untracked.uint32(87654321)
    ),
    MuonSimHits = cms.PSet(
        engineName = cms.untracked.string('TRandom3'),
        initialSeed = cms.untracked.uint32(987346)
    ),
    VtxSmeared = cms.PSet(
        engineName = cms.untracked.string('HepJamesRandom'),
        initialSeed = cms.untracked.uint32(98765432)
    ),
    ecalPreshowerRecHit = cms.PSet(
        engineName = cms.untracked.string('TRandom3'),
        initialSeed = cms.untracked.uint32(6541321)
    ),
    ecalRecHit = cms.PSet(
        engineName = cms.untracked.string('TRandom3'),
        initialSeed = cms.untracked.uint32(654321)
    ),
    externalLHEProducer = cms.PSet(
        engineName = cms.untracked.string('HepJamesRandom'),
        initialSeed = cms.untracked.uint32(234567)
    ),
    famosPileUp = cms.PSet(
        engineName = cms.untracked.string('TRandom3'),
        initialSeed = cms.untracked.uint32(918273)
    ),
    famosSimHits = cms.PSet(
        engineName = cms.untracked.string('TRandom3'),
        initialSeed = cms.untracked.uint32(13579)
    ),
    g4SimHits = cms.PSet(
        engineName = cms.untracked.string('HepJamesRandom'),
        initialSeed = cms.untracked.uint32(11)
    ),
    generator = cms.PSet(
        engineName = cms.untracked.string('HepJamesRandom'),
        initialSeed = cms.untracked.uint32(123456789)
    ),
    hbhereco = cms.PSet(
        engineName = cms.untracked.string('TRandom3'),
        initialSeed = cms.untracked.uint32(541321)
    ),
    hfreco = cms.PSet(
        engineName = cms.untracked.string('TRandom3'),
        initialSeed = cms.untracked.uint32(541321)
    ),
    hiSignal = cms.PSet(
        engineName = cms.untracked.string('HepJamesRandom'),
        initialSeed = cms.untracked.uint32(123456789)
    ),
    hiSignalG4SimHits = cms.PSet(
        engineName = cms.untracked.string('HepJamesRandom'),
        initialSeed = cms.untracked.uint32(11)
    ),
    hiSignalLHCTransport = cms.PSet(
        engineName = cms.untracked.string('TRandom3'),
        initialSeed = cms.untracked.uint32(88776655)
    ),
    horeco = cms.PSet(
        engineName = cms.untracked.string('TRandom3'),
        initialSeed = cms.untracked.uint32(541321)
    ),
    l1ParamMuons = cms.PSet(
        engineName = cms.untracked.string('TRandom3'),
        initialSeed = cms.untracked.uint32(6453209)
    ),
    mix = cms.PSet(
        engineName = cms.untracked.string('HepJamesRandom'),
        initialSeed = cms.untracked.uint32(12345)
    ),
    mixData = cms.PSet(
        engineName = cms.untracked.string('HepJamesRandom'),
        initialSeed = cms.untracked.uint32(12345)
    ),
    mixGenPU = cms.PSet(
        engineName = cms.untracked.string('TRandom3'),
        initialSeed = cms.untracked.uint32(918273)
    ),
    mixRecoTracks = cms.PSet(
        engineName = cms.untracked.string('TRandom3'),
        initialSeed = cms.untracked.uint32(918273)
    ),
    mixSimCaloHits = cms.PSet(
        engineName = cms.untracked.string('TRandom3'),
        initialSeed = cms.untracked.uint32(918273)
    ),
    paramMuons = cms.PSet(
        engineName = cms.untracked.string('TRandom3'),
        initialSeed = cms.untracked.uint32(54525)
    ),
    saveFileName = cms.untracked.string(''),
    siTrackerGaussianSmearingRecHits = cms.PSet(
        engineName = cms.untracked.string('TRandom3'),
        initialSeed = cms.untracked.uint32(24680)
    ),
    simBeamSpotFilter = cms.PSet(
        engineName = cms.untracked.string('HepJamesRandom'),
        initialSeed = cms.untracked.uint32(87654321)
    ),
    simMuonCSCDigis = cms.PSet(
        engineName = cms.untracked.string('HepJamesRandom'),
        initialSeed = cms.untracked.uint32(11223344)
    ),
    simMuonDTDigis = cms.PSet(
        engineName = cms.untracked.string('HepJamesRandom'),
        initialSeed = cms.untracked.uint32(1234567)
    ),
    simMuonRPCDigis = cms.PSet(
        engineName = cms.untracked.string('HepJamesRandom'),
        initialSeed = cms.untracked.uint32(1234567)
    ),
    simSiStripDigiSimLink = cms.PSet(
        engineName = cms.untracked.string('HepJamesRandom'),
        initialSeed = cms.untracked.uint32(1234567)
    )
)


process.TFileService = cms.Service("TFileService",
    fileName = cms.string('outW280.root')
)


process.CSCGeometryESModule = cms.ESProducer("CSCGeometryESModule",
    alignmentsLabel = cms.string(''),
    appendToDataLabel = cms.string(''),
    applyAlignment = cms.bool(True),
    debugV = cms.untracked.bool(False),
    useCentreTIOffsets = cms.bool(False),
    useDDD = cms.bool(False),
    useGangedStripsInME1a = cms.bool(True),
    useOnlyWiresInME1a = cms.bool(False),
    useRealWireGeometry = cms.bool(True)
)


process.CaloGeometryBuilder = cms.ESProducer("CaloGeometryBuilder",
    SelectedCalos = cms.vstring('HCAL', 
        'ZDC', 
        'CASTOR', 
        'EcalBarrel', 
        'EcalEndcap', 
        'EcalPreshower', 
        'TOWER')
)


process.CaloTopologyBuilder = cms.ESProducer("CaloTopologyBuilder")


process.CaloTowerGeometryFromDBEP = cms.ESProducer("CaloTowerGeometryFromDBEP",
    applyAlignment = cms.bool(False),
    hcalTopologyConstants = cms.PSet(
        maxDepthHB = cms.int32(2),
        maxDepthHE = cms.int32(3),
        mode = cms.string('HcalTopologyMode::LHC')
    )
)


process.CaloTowerTopologyEP = cms.ESProducer("CaloTowerTopologyEP")


process.CastorGeometryFromDBEP = cms.ESProducer("CastorGeometryFromDBEP",
    applyAlignment = cms.bool(False)
)


process.DTGeometryESModule = cms.ESProducer("DTGeometryESModule",
    alignmentsLabel = cms.string(''),
    appendToDataLabel = cms.string(''),
    applyAlignment = cms.bool(True),
    fromDDD = cms.bool(False)
)


process.EcalBarrelGeometryFromDBEP = cms.ESProducer("EcalBarrelGeometryFromDBEP",
    applyAlignment = cms.bool(True)
)


process.EcalElectronicsMappingBuilder = cms.ESProducer("EcalElectronicsMappingBuilder")


process.EcalEndcapGeometryFromDBEP = cms.ESProducer("EcalEndcapGeometryFromDBEP",
    applyAlignment = cms.bool(True)
)


process.EcalPreshowerGeometryFromDBEP = cms.ESProducer("EcalPreshowerGeometryFromDBEP",
    applyAlignment = cms.bool(True)
)


process.EcalTrigTowerConstituentsMapBuilder = cms.ESProducer("EcalTrigTowerConstituentsMapBuilder",
    MapFile = cms.untracked.string('Geometry/EcalMapping/data/EndCap_TTMap.txt')
)


process.GlobalTrackingGeometryESProducer = cms.ESProducer("GlobalTrackingGeometryESProducer")


process.HcalAlignmentEP = cms.ESProducer("HcalAlignmentEP")


process.HcalGeometryFromDBEP = cms.ESProducer("HcalGeometryFromDBEP",
    applyAlignment = cms.bool(True),
    hcalTopologyConstants = cms.PSet(
        maxDepthHB = cms.int32(2),
        maxDepthHE = cms.int32(3),
        mode = cms.string('HcalTopologyMode::LHC')
    )
)


process.MuonDetLayerGeometryESProducer = cms.ESProducer("MuonDetLayerGeometryESProducer")


process.MuonNumberingInitialization = cms.ESProducer("MuonNumberingInitialization")


process.ParabolicParametrizedMagneticFieldProducer = cms.ESProducer("AutoParametrizedMagneticFieldProducer",
    label = cms.untracked.string('ParabolicMf'),
    valueOverride = cms.int32(18268),
    version = cms.string('Parabolic')
)


process.RPCGeometryESModule = cms.ESProducer("RPCGeometryESModule",
    compatibiltyWith11 = cms.untracked.bool(True),
    useDDD = cms.untracked.bool(False)
)


process.TrackerRecoGeometryESProducer = cms.ESProducer("TrackerRecoGeometryESProducer")


process.VolumeBasedMagneticFieldESProducer = cms.ESProducer("VolumeBasedMagneticFieldESProducerFromDB",
    debugBuilder = cms.untracked.bool(False),
    label = cms.untracked.string(''),
    valueOverride = cms.int32(18268)
)


process.XMLFromDBSource = cms.ESProducer("XMLIdealGeometryESProducer",
    label = cms.string('Extended'),
    rootDDName = cms.string('cms:OCMS')
)


process.ZdcGeometryFromDBEP = cms.ESProducer("ZdcGeometryFromDBEP",
    applyAlignment = cms.bool(False)
)


process.fakeForIdealAlignment = cms.ESProducer("FakeAlignmentProducer",
    appendToDataLabel = cms.string('fakeForIdeal')
)


process.hcalDDDRecConstants = cms.ESProducer("HcalDDDRecConstantsESModule",
    appendToDataLabel = cms.string('')
)


process.hcalDDDSimConstants = cms.ESProducer("HcalDDDSimConstantsESModule",
    appendToDataLabel = cms.string('')
)


process.hcalTopologyIdeal = cms.ESProducer("HcalTopologyIdealEP",
    Exclude = cms.untracked.string(''),
    appendToDataLabel = cms.string('')
)


process.idealForDigiCSCGeometry = cms.ESProducer("CSCGeometryESModule",
    alignmentsLabel = cms.string('fakeForIdeal'),
    appendToDataLabel = cms.string('idealForDigi'),
    applyAlignment = cms.bool(False),
    debugV = cms.untracked.bool(False),
    useCentreTIOffsets = cms.bool(False),
    useDDD = cms.bool(False),
    useGangedStripsInME1a = cms.bool(True),
    useOnlyWiresInME1a = cms.bool(False),
    useRealWireGeometry = cms.bool(True)
)


process.idealForDigiDTGeometry = cms.ESProducer("DTGeometryESModule",
    alignmentsLabel = cms.string('fakeForIdeal'),
    appendToDataLabel = cms.string('idealForDigi'),
    applyAlignment = cms.bool(False),
    fromDDD = cms.bool(False)
)


process.idealForDigiTrackerGeometry = cms.ESProducer("TrackerDigiGeometryESModule",
    alignmentsLabel = cms.string('fakeForIdeal'),
    appendToDataLabel = cms.string('idealForDigi'),
    applyAlignment = cms.bool(False),
    fromDDD = cms.bool(False)
)


process.trackerGeometryDB = cms.ESProducer("TrackerDigiGeometryESModule",
    alignmentsLabel = cms.string(''),
    appendToDataLabel = cms.string(''),
    applyAlignment = cms.bool(True),
    fromDDD = cms.bool(False)
)


process.trackerNumberingGeometryDB = cms.ESProducer("TrackerGeometricDetESModule",
    appendToDataLabel = cms.string(''),
    fromDDD = cms.bool(False)
)


process.trackerTopology = cms.ESProducer("TrackerTopologyEP",
    appendToDataLabel = cms.string('')
)


process.HepPDTESSource = cms.ESSource("HepPDTESSource",
    pdtFileName = cms.FileInPath('SimGeneral/HepPDTESSource/data/pythiaparticle.tbl')
)


process.eegeom = cms.ESSource("EmptyESSource",
    firstValid = cms.vuint32(1),
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('EcalMappingRcd')
)


process.schedule = cms.Schedule(*[ process.path120, process.path150, process.path185, process.path250, process.path360 ])
