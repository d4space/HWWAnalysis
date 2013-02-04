import hwwtools
import re


backgrounds = {
    'WW'                      : ['nominals/latino_000_WWJets2LMad.root'],
    'ggWW'                    : ['nominals/latino_001_GluGluToWWTo4L.root'],
    'VgS'                     : ['nominals/latino_082_WGstarToElNuMad.root',
                                 'nominals/latino_083_WGstarToMuNuMad.root',
                                 'nominals/latino_084_WGstarToTauNuMad.root',
                                ],
    'VgS-template'            : ['vgTemplate/latino_082_WGstarToElNuMad.root',
                                 'vgTemplate/latino_083_WGstarToMuNuMad.root',
                                 'vgTemplate/latino_084_WGstarToTauNuMad.root',
                                ],
    'Vg'                      : ['nominals/latino_085_WgammaToLNuG.root',
                                 'nominals/latino_086_ZgammaToLLuG.root',
                                ],
    'Vg-template'             : ['vgTemplate/latino_085_WgammaToLNuG.root',
                                 'vgTemplate/latino_086_ZgammaToLLuG.root',
                                ],
    'WJet'                    : ['wjets/latino_RunA_892pbinv_LooseLoose.root',
                                 'wjets/latino_RunB_4404pbinv_LooseLoose.root',
                                 'wjets/latino_RunC_7032pbinv_LooseLoose.root',
                                 'wjets/latino_RunD_7274pbinv_LooseLoose.root',
                                ],
    'WJetSS'                  : ['wjets/latino_RunA_892pbinv_LooseLoose.root',
                                 'wjets/latino_RunB_4404pbinv_LooseLoose.root',
                                 'wjets/latino_RunC_7032pbinv_LooseLoose.root',
                                 'wjets/latino_RunD_7274pbinv_LooseLoose.root',
                                ],
    'WJetFakeRate-eUp'        : ['wjets/latino_RunA_892pbinv_LooseLoose.root',
                                 'wjets/latino_RunB_4404pbinv_LooseLoose.root',
                                 'wjets/latino_RunC_7032pbinv_LooseLoose.root',
                                 'wjets/latino_RunD_7274pbinv_LooseLoose.root',
                                ],
    'WJetFakeRate-eDn'        : ['wjets/latino_RunA_892pbinv_LooseLoose.root',
                                 'wjets/latino_RunB_4404pbinv_LooseLoose.root',
                                 'wjets/latino_RunC_7032pbinv_LooseLoose.root',
                                 'wjets/latino_RunD_7274pbinv_LooseLoose.root',
                                ],
    'WJetFakeRate-mUp'        : ['wjets/latino_RunA_892pbinv_LooseLoose.root',
                                 'wjets/latino_RunB_4404pbinv_LooseLoose.root',
                                 'wjets/latino_RunC_7032pbinv_LooseLoose.root',
                                 'wjets/latino_RunD_7274pbinv_LooseLoose.root',
                                ],
    'WJetFakeRate-mDn'        : ['wjets/latino_RunA_892pbinv_LooseLoose.root',
                                 'wjets/latino_RunB_4404pbinv_LooseLoose.root',
                                 'wjets/latino_RunC_7032pbinv_LooseLoose.root',
                                 'wjets/latino_RunD_7274pbinv_LooseLoose.root',
                                ],
    'WJet-template-2j'        : ['wjetsTemplate/latino_RunA_892pbinv_LooseLoose.root',
                                 'wjetsTemplate/latino_RunB_4404pbinv_LooseLoose.root',
                                 'wjetsTemplate/latino_RunC_6807pbinv_LooseLoose.root',
                                ],
    'WJetFakeRate-template-2j': ['wjetsTemplate/latino_RunA_892pbinv_LooseLoose.root',
                                 'wjetsTemplate/latino_RunB_4404pbinv_LooseLoose.root',
                                 'wjetsTemplate/latino_RunC_6807pbinv_LooseLoose.root',
                                ],
    'Top'                     : ['nominals/latino_019_TTTo2L2Nu2B.root',
                                 'nominals/latino_011_TtWFullDR.root',
                                 'nominals/latino_012_TbartWFullDR.root',
                                ],
    'VV'                      : ['nominals/latino_074_WZJetsMad.root',
                                 'nominals/latino_075_ZZJetsMad.root',
                                 'nominals/latino_078_WZTo2L2QMad.root',
                                 'nominals/latino_079_ZZTo2L2QMad.root',
                                ],
    'DYTT'                    : ['nominals/latino_DYtt_19.5fb.root'], # for ee/mm channels DYTT is included in DD
    'DYLL'                    : ['nominals/latino_036_DY10toLLMad.root',
                                 'nominals/latino_037_DY50toLLMad.root',
                                ],
    'DYee'                    : ['nominals/latino_000_WWJets2LMad.root',   # dummy, just to have the histogram in cut based
                                ],
    'DYmm'                    : ['nominals/latino_000_WWJets2LMad.root',   # dummy, just to have the histogram in cut based
                                ],
    'DYLL-template-0j1j'      : ['dyTemplate/latino_036_DY10toLLMad.root',
                                 'dyTemplate/latino_037_DY50toLLMad.root',
                                ],
    'DYLL-templatesyst-0j1j'  : ['dyTemplate/latino_036_DY10toLLMad.root',
                                 'dyTemplate/latino_037_DY50toLLMad.root',
                                ],
    'WWnlo'                   : ['nominals/latino_002_WWto2L2NuMCatNLO.root'],
    'WWnloUp'                 : ['nominals/latino_004_WWto2L2NuMCatNLOUp.root'],
    'WWnloDown'               : ['nominals/latino_003_WWto2L2NuMCatNLODown.root'],
    'Top-template'            : ['topTemplate/latino_000_WWJets2LMad.root',
                                 'topTemplate/latino_001_GluGluToWWTo4L.root',
                                 'topTemplate/latino_074_WZJetsMad.root',
                                 'topTemplate/latino_075_ZZJetsMad.root',
                                 'topTemplate/latino_078_WZTo2L2QMad.root',
                                 'topTemplate/latino_079_ZZTo2L2QMad.root',
                                 'topTemplate/latino_082_WGstarToElNuMad.root',
                                 'topTemplate/latino_083_WGstarToMuNuMad.root',
                                 'topTemplate/latino_084_WGstarToTauNuMad.root',
                                 'topTemplate/latino_085_WgammaToLNuG.root',
                                 'topTemplate/latino_086_ZgammaToLLuG.root',
                                 'topTemplate/latino_RunA_892pbinv_LooseLoose.root',
                                 'topTemplate/latino_RunB_4404pbinv_LooseLoose.root',
                                 'topTemplate/latino_RunC_7032pbinv_LooseLoose.root',
                                 'topTemplate/latino_RunD_7274pbinv_LooseLoose.root',
                                ],
    'TopTW'                   : ['nominals/latino_019_TTTo2L2Nu2B.root',
                                 'tW/latino_011_TtWFullDR.root',
                                 'tW/latino_012_TbartWFullDR.root',
                                 ],
    'TopCtrl'                 : ['nominals/latino_019_TTTo2L2Nu2B.root',
                                 'nominals/latino_011_TtWFullDR.root',
                                 'nominals/latino_012_TbartWFullDR.root',
                                 ],
    'DYLL-template-dd'        : ['dyTemplate-dd/latino_036_DY10toLLMad.root',
                                 'dyTemplate-dd/latino_037_DY50toLLMad.root',
                                ],
    'DYLL-template-vbf'       : ['dyTemplate/latino_036_DY10toLLMad.root',
                                 'dyTemplate/latino_037_DY50toLLMad.root',
                                ],
}

backgrounds_7TeV = {
    'WW'                      : ['nominals/latino_000_WWJets2LMad.root'],
    'ggWW'                    : ['nominals/latino_001_GluGluToWWTo4L.root'],
    'VgS'                     : ['nominals/latino_085_WGstarToLNu2Mu.root',
                                 'nominals/latino_086_WGstarToLNu2E.root',
                                ],
    'VgS-template'            : ['vgTemplate/latino_082_WGstarToElNuMad.root',
                                 'vgTemplate/latino_083_WGstarToMuNuMad.root',
                                 'vgTemplate/latino_084_WGstarToTauNuMad.root',
                                ],
    'Vg'                      : ['nominals/latino_082_WgammaToElNuMad.root',
                                 'nominals/latino_083_WgammaToMuNuMad.root',
                                 'nominals/latino_084_WgammaToTauNuMad.root',
                                ],
    'Vg-template'             : ['vgTemplate/latino_085_WgammaToLNuG.root'],
    'WJet'                    : ['wjets/WJetsEstimated_Full2011_added.root'],
    'WJetFakeRate-eUp'        : ['vgTemplate/latino_RunA_892pbinv_LooseLoose.root',
                                 'vgTemplate/latino_RunB_4404pbinv_LooseLoose.root',
                                 'vgTemplate/latino_RunC_7032pbinv_LooseLoose.root',
                                 'vgTemplate/latino_RunD_7274pbinv_LooseLoose.root',
                                ],
    'WJetFakeRate-eDn'        : ['vgTemplate/latino_RunA_892pbinv_LooseLoose.root',
                                 'vgTemplate/latino_RunB_4404pbinv_LooseLoose.root',
                                 'vgTemplate/latino_RunC_7032pbinv_LooseLoose.root',
                                 'vgTemplate/latino_RunD_7274pbinv_LooseLoose.root',
                                ],
    'WJetFakeRate-mUp'        : ['vgTemplate/latino_RunA_892pbinv_LooseLoose.root',
                                 'vgTemplate/latino_RunB_4404pbinv_LooseLoose.root',
                                 'vgTemplate/latino_RunC_7032pbinv_LooseLoose.root',
                                 'vgTemplate/latino_RunD_7274pbinv_LooseLoose.root',
                                ],
    'WJetFakeRate-mDn'        : ['vgTemplate/latino_RunA_892pbinv_LooseLoose.root',
                                 'vgTemplate/latino_RunB_4404pbinv_LooseLoose.root',
                                 'vgTemplate/latino_RunC_7032pbinv_LooseLoose.root',
                                 'vgTemplate/latino_RunD_7274pbinv_LooseLoose.root',
                                ],
    'WJet-template-2j'        : ['wjetsTemplate/latino_RunA_892pbinv_LooseLoose.root',
                                 'wjetsTemplate/latino_RunB_4404pbinv_LooseLoose.root',
                                 'wjetsTemplate/latino_RunC_6807pbinv_LooseLoose.root',
                                ],
    'WJetFakeRate-template-2j': ['wjetsTemplate/latino_RunA_892pbinv_LooseLoose.root',
                                 'wjetsTemplate/latino_RunB_4404pbinv_LooseLoose.root',
                                 'wjetsTemplate/latino_RunC_6807pbinv_LooseLoose.root',
                                ],
    'Top'                     : ['nominals/latino_011_TtWFullDR.root',
                                 'nominals/latino_012_TbartWFullDR.root',
                                 'nominals/latino_013_TtFull.root',
                                 'nominals/latino_014_TbartFull.root',
                                 'nominals/latino_015_TsFull.root',
                                 'nominals/latino_016_TbarsFull.root',
                                 'nominals/latino_019_TTTo2L2Nu2B.root',
                                ],
    'VV'                      : ['nominals/latino_074_WZJetsMad.root',
                                 'nominals/latino_071_ZZFull.root',
                                ],
    'DYTT'                    : ['nominals/latino_DYtt_2011_added.root'], # for ee/mm channels DYTT is included in DD
    'DYLL'                    : ['nominals/latino_036_DY10toLLMad.root',
                                 'nominals/latino_037_DY50toLLMad.root'
                                ],
    'DYee'                    : ['nominals/latino_000_WWJets2LMad.root',   # dummy, just to have the histogram in cut based
                                ],
    'DYmm'                    : ['nominals/latino_000_WWJets2LMad.root',   # dummy, just to have the histogram in cut based
                                ],
    'DYLL-template-0j1j'      : ['dyTemplate/latino_036_DY10toLLMad.root',
                                 'dyTemplate/latino_037_DY50toLLMad.root',
                                ],
    'DYLL-templatesyst-0j1j'  : ['dyTemplate/latino_036_DY10toLLMad.root',
                                 'dyTemplate/latino_037_DY50toLLMad.root',
                                ],
    'WWnlo'                   : ['nominals/latino_002_WWto2L2NuMCatNLO.root'],
    'WWnloUp'                 : ['nominals/latino_003_WWto2L2NuMCatNLOUp.root'],
    'WWnloDown'               : ['nominals/latino_004_WWto2L2NuMCatNLODown.root'],
    'TopTW'                   : ['tW/latino_011_TtWFullDR.root',
                                 'tW//latino_012_TbartWFullDR.root',
                                 'tW//latino_013_TtFull.root',
                                 'tW//latino_014_TbartFull.root',
                                 'tW//latino_015_TsFull.root',
                                 'tW//latino_016_TbarsFull.root',
                                 'nominals/latino_019_TTTo2L2Nu2B.root',
                                 ],
    'TopCtrl'                 : ['nominals/latino_011_TtWFullDR.root',
                                 'nominals/latino_012_TbartWFullDR.root',
                                 'nominals/latino_013_TtFull.root',
                                 'nominals/latino_014_TbartFull.root',
                                 'nominals/latino_015_TsFull.root',
                                 'nominals/latino_016_TbarsFull.root',
                                 'nominals/latino_019_TTTo2L2Nu2B.root',
                                ],
    'DYLL-template-dd'        : ['dyTemplate-dd/latino_036_DY10toLLMad.root',
                                 'dyTemplate-dd/latino_037_DY50toLLMad.root',
                                ],
    'DYLL-template-vbf'       : ['dyTemplate/latino_036_DY10toLLMad.root',
                                 'dyTemplate/latino_037_DY50toLLMad.root',
                                ],
}

data = {
    'Data2011A' : ['data/latino_150_SingleElectron2011AMay10.root',
                   'data/latino_151_SingleMuon2011AMay10.root',
                   'data/latino_152_DoubleMuon2011AMay10.root',
                   'data/latino_153_DoubleElectron2011AMay10.root',
                   'data/latino_154_MuEG2011AMay10.root',

                   'data/latino_100_SingleElectron2011Av4.root',
                   'data/latino_101_SingleMuon2011Av4.root',
                   'data/latino_102_DoubleElectron2011Av4.root',
                   'data/latino_103_DoubleMuon2011Av4.root',
                   'data/latino_104_MuEG2011Av4.root',

                   'data/latino_160_SingleElectron2011AAug05.root',
                   'data/latino_161_SingleMuon2011AAug05.root',
                   'data/latino_162_DoubleElectron2011AAug05.root',
                   'data/latino_163_DoubleMuon2011AAug05.root',
                   'data/latino_164_MuEG2011AAug05.root',

                   'data/latino_120_SingleElectron2011Av6.root',
                   'data/latino_121_SingleMuon2011Av6.root',
                   'data/latino_122_DoubleElectron2011Av6.root',
                   'data/latino_123_DoubleMuon2011Av6.root',
                   'data/latino_124_MuEG2011Av6.root',
                  ],

    'Data2011B'  :['data/latino_140_SingleElectron2011Bv1a.root',
                   'data/latino_141_SingleMuon2011Bv1a.root',
                   'data/latino_142_DoubleElectron2011Bv1a.root',
                   'data/latino_143_DoubleMuon2011Bv1a.root',
                   'data/latino_144_MuEG2011Bv1a.root',
                  ],

    'Data2012A' : ['data/latino_RunA_892pbinv.root'],

    'Data2012B' : ['data/latino_RunB_4404pbinv.root'],

    'Data2012C' : ['data/latino_RunC_7032pbinv.root'],

    'Data2012D' : ['data/latino_RunD_7274pbinv.root'],
}

data['Data2011'] = data['Data2011A']+data['Data2011B']

data['Data2012'] = data['Data2012A']+data['Data2012B']+data['Data2012C']+data['Data2012D']

#--------------
# signal samples labels and generation

signals = ['ggH','vbfH','vbfH_ALT','wzttH','wzttH_ALT','jhu','jhu_ALT','wH','zH','ttH']

def signalSamples(sigtag,mass=125):

    signals = {}

    if sigtag == 'SM':
        ggH   = ['nominals/latino_1{mass}_ggToH{mass}toWWTo2LAndTau2Nu.root',
                ]
        vbfH  = ['nominals/latino_2{mass}_vbfToH{mass}toWWTo2LAndTau2Nu.root',
                ]
        wzttH = ['nominals/latino_3{mass}_wzttH{mass}ToWW.root']
        wH    = ['nominals/latino_3{mass}_wzttH{mass}ToWW.root']
        zH    = ['nominals/latino_3{mass}_wzttH{mass}ToWW.root']
        ttH   = ['nominals/latino_3{mass}_wzttH{mass}ToWW.root']



        if mass <= 300:
            signals['ggH']   = [f.format(mass = mass) for f in ggH]
            signals['vbfH']  = [f.format(mass = mass) for f in vbfH]
            signals['wzttH'] = [f.format(mass = mass) for f in wzttH]
            signals['wH']    = [f.format(mass = mass) for f in wH]
            signals['zH']    = [f.format(mass = mass) for f in zH]
            signals['ttH']   = [f.format(mass = mass) for f in ttH]
        else:
            signals['ggH']   = [f.format(mass = mass) for f in ggH]
            signals['vbfH']  = [f.format(mass = mass) for f in vbfH]

# Test from Alessandro:
    elif sigtag == 'JHU' and mass==125:
       signals['jhu']     = ['nominals/latino_1125_ggToH125toWWTo2LAndTau2Nu.root']
       signals['jhu_ALT'] = ['nominals/latino_1125_ggToH125toWWTo2LAndTau2Nu.root']

    elif sigtag == 'JHUSMONLY' and mass==125:
        signals['jhu']     = ['nominals/latino_8001_SMH125ToWW2L2Nu.root',
                              'nominals/latino_8004_SMH125ToWW2Tau2Nu.root',
                              'nominals/latino_8007_SMH125ToWWLTau2Nu.root' 
                             ]

    elif sigtag == 'JHU0MONLY' and mass==125:
        signals['jhu']     = ['nominals/latino_8002_Higgs0M125ToWW2L2Nu.root',
                              'nominals/latino_8005_Higgs0M125ToWW2Tau2Nu.root',
                              'nominals/latino_8008_Higgs0M125ToWWLTau2Nu.root'
                             ]
    elif sigtag == 'JHU2MONLY' and mass==125:
        signals['jhu']     = ['nominals/latino_8003_Graviton2PM.root',
                              'nominals/latino_8006_Graviton2PMToWW2Tau2nu.root',
                              'nominals/latino_8009_Graviton2PMToWWLTau2nu.root'
                             ]

    elif sigtag == 'JHUSMvs0M' and mass==125:
        signals['jhu']     = ['nominals/latino_8001_SMH125ToWW2L2Nu.root',
                              'nominals/latino_8004_SMH125ToWW2Tau2Nu.root',
                              'nominals/latino_8007_SMH125ToWWLTau2Nu.root' 
                             ]
        signals['jhu_ALT'] = ['nominals/latino_8002_Higgs0M125ToWW2L2Nu.root',
                              'nominals/latino_8005_Higgs0M125ToWW2Tau2Nu.root', 
                              'nominals/latino_8008_Higgs0M125ToWWLTau2Nu.root' 
                             ]

    elif sigtag == 'JHUSMvs2M' and mass==125:
        signals['jhu']     = ['nominals/latino_8001_SMH125ToWW2L2Nu.root',
                              'nominals/latino_8004_SMH125ToWW2Tau2Nu.root',
                              'nominals/latino_8007_SMH125ToWWLTau2Nu.root' 
                             ]
        signals['jhu_ALT'] = ['nominals/latino_8003_Graviton2PM.root',
                              'nominals/latino_8006_Graviton2PMToWW2Tau2nu.root',
                              'nominals/latino_8009_Graviton2PMToWWLTau2nu.root'
                             ]

    elif sigtag == 'JHUSMvs2MplOthers' and mass==125:
        signals['jhu']     = ['nominals/latino_8001_SMH125ToWW2L2Nu.root',
                              'nominals/latino_8004_SMH125ToWW2Tau2Nu.root',
                              'nominals/latino_8007_SMH125ToWWLTau2Nu.root'
                             ]
        signals['vbfH']    = ['nominals/latino_2125_vbfToH125toWWTo2LAndTau2Nu.root']
        signals['wzttH']   = ['nominals/latino_3125_wzttH125ToWW.root']

        signals['jhu_ALT'] = ['nominals/latino_8003_Graviton2PM.root',
                              'nominals/latino_8006_Graviton2PMToWW2Tau2nu.root',
                              'nominals/latino_8009_Graviton2PMToWWLTau2nu.root'
                             ]
        signals['vbfH_ALT'] = ['nominals/latino_2125_vbfToH125toWWTo2LAndTau2Nu.root']
        signals['wzttH_ALT']= ['nominals/latino_3125_wzttH125ToWW.root']

    elif sigtag == 'PWGSMvs2MplOthers' and mass==125:
        signals['jhu']     = ['nominals/latino_1125_ggToH125toWWTo2LAndTau2Nu.root']
        signals['vbfH']    = ['nominals/latino_2125_vbfToH125toWWTo2LAndTau2Nu.root']
        signals['wzttH']   = ['nominals/latino_3125_wzttH125ToWW.root']
               
        signals['jhu_ALT'] = ['nominals/latino_8003_Graviton2PM.root',
                              'nominals/latino_8006_Graviton2PMToWW2Tau2nu.root',
                              'nominals/latino_8009_Graviton2PMToWWLTau2nu.root'
                             ]
        signals['vbfH_ALT'] = ['nominals/latino_2125_vbfToH125toWWTo2LAndTau2Nu.root']
        signals['wzttH_ALT']= ['nominals/latino_3125_wzttH125ToWW.root']


    else:
        raise ValueError('Signal tag %s not found for mass %d' % (sigtag,mass) )
    return signals

def signalSamples_7TeV(sigtag,mass=125):

    signals = {}

    if sigtag == 'SM':
        ggH = ['nominals/latino_1{mass}_ggToH{mass}toWWto2L2Nu.root',
               'nominals/latino_2{mass}_ggToH{mass}toWWtoLNuTauNu.root',
               'nominals/latino_3{mass}_ggToH{mass}toWWto2Tau2Nu.root',
              ]
        ggHnew = ['nominals/latino_9{mass}_ggToH{mass}toWWTo2LAndTau2Nu.root']
        vbfH   = ['nominals/latino_4{mass}_vbfToH{mass}toWWto2L2Nu.root',
                  'nominals/latino_5{mass}_vbfToH{mass}toWWtoLNuTauNu.root',
                  'nominals/latino_6{mass}_vbfToH{mass}toWWto2Tau2Nu.root',
                 ]
        vbfHnew = ['nominals/latino_8{mass}_vbfToH{mass}toWWTo2LAndTau2Nu.root']
        wzttH   = ['nominals/latino_7{mass}_wzttH{mass}ToWW.root']
        
        if int(mass)==122:
            signals['ggH']  = [f.format(mass = mass) for f in ggHnew]
            signals['wzttH'] = [f.format(mass = mass) for f in wzttH]
        elif int(mass)==118 or (int(mass)>120 and int(mass)<130) or int(mass)==135:
            signals['ggH']  = [f.format(mass = mass) for f in ggHnew]
            signals['vbfH'] = [f.format(mass = mass) for f in vbfHnew]
            signals['wzttH'] = [f.format(mass = mass) for f in wzttH]
        elif int(mass) > 115:
            signals['ggH']  = [f.format(mass = mass) for f in ggH]
            signals['vbfH'] = [f.format(mass = mass) for f in vbfH]
            signals['wzttH'] = [f.format(mass = mass) for f in wzttH]
        else:
            signals['ggH']  = ['nominals/latino_9{mass}_ggToH{mass}toWWTo2LAndTau2Nu.root'.format(mass = mass)]
            signals['vbfH'] = ['nominals/latino_8{mass}_vbfToH{mass}toWWTo2LAndTau2Nu.root'.format(mass = mass)]
            
# and the JHU case:
    elif sigtag == 'JHUSMONLY' and mass==125:
        signals['jhu']     = ['nominals/latino_8001_SMH125ToWW2L2Nu.root',
                              'nominals/latino_8004_SMH125ToWW2Tau2Nu.root',
                              'nominals/latino_8007_SMH125ToWWLTau2Nu.root' 
                             ]
        signals['jhu_NORM']= ['nominals/latino_1125_ggToH125toWWTo2LAndTau2Nu.root']

    elif sigtag == 'JHU0MONLY' and mass==125:
        signals['jhu']     = ['nominals/latino_8002_Higgs0M125ToWW2L2Nu.root',
                              'nominals/latino_8005_Higgs0M125ToWW2Tau2Nu.root',
                              'nominals/latino_8008_Higgs0M125ToWWLTau2Nu.root'
                             ]
        signals['jhu_NORM']= ['nominals/latino_1125_ggToH125toWWTo2LAndTau2Nu.root']

    elif sigtag == 'JHU2MONLY' and mass==125:
        signals['jhu']     = ['nominals/latino_8003_Graviton2PM.root',
                              'nominals/latino_8006_Graviton2PMToWW2Tau2nu.root',
                              'nominals/latino_8009_Graviton2PMToWWLTau2nu.root'
                             ]
        signals['jhu_NORM']= ['nominals/latino_1125_ggToH125toWWTo2LAndTau2Nu.root']

    elif sigtag == 'JHUSMvs0M' and mass==125:
        signals['jhu']     = ['nominals/latino_8001_SMH125ToWW2L2Nu.root',
                              'nominals/latino_8004_SMH125ToWW2Tau2Nu.root',
                              'nominals/latino_8007_SMH125ToWWLTau2Nu.root' 
                             ]
        signals['jhu_ALT'] = ['nominals/latino_8002_Higgs0M125ToWW2L2Nu.root',
                              'nominals/latino_8005_Higgs0M125ToWW2Tau2Nu.root', 
                              'nominals/latino_8008_Higgs0M125ToWWLTau2Nu.root' 
                             ]
        signals['jhu_NORM']= ['nominals/latino_1125_ggToH125toWWTo2LAndTau2Nu.root']

    elif sigtag == 'JHUSMvs2M' and mass==125:
        signals['jhu']     = ['nominals/latino_8001_SMH125ToWW2L2Nu.root',
                              'nominals/latino_8004_SMH125ToWW2Tau2Nu.root',
                              'nominals/latino_8007_SMH125ToWWLTau2Nu.root' 
                             ]
        signals['jhu_ALT'] = ['nominals/latino_8003_Graviton2PM.root',
                              'nominals/latino_8006_Graviton2PMToWW2Tau2nu.root',
                              'nominals/latino_8009_Graviton2PMToWWLTau2nu.root'
                             ]
        signals['jhu_NORM']= ['nominals/latino_1125_ggToH125toWWTo2LAndTau2Nu.root']
        signals['jhu_NLO']= ['nominals/latino_1125_ggToH125toWWTo2LAndTau2Nu.root']

    elif sigtag == 'JHUSMvs2MplOthers' and mass==125:
        signals['jhu']     = ['nominals/latino_8001_SMH125ToWW2L2Nu.root',
                              'nominals/latino_8004_SMH125ToWW2Tau2Nu.root',
                              'nominals/latino_8007_SMH125ToWWLTau2Nu.root'
                             ]
        signals['vbfH']    = ['nominals/latino_2125_vbfToH125toWWTo2LAndTau2Nu.root']
        signals['wzttH']   = ['nominals/latino_3125_wzttH125ToWW.root']

        signals['jhu_ALT'] = ['nominals/latino_8003_Graviton2PM.root',
                              'nominals/latino_8006_Graviton2PMToWW2Tau2nu.root',
                              'nominals/latino_8009_Graviton2PMToWWLTau2nu.root'
                             ]
        signals['vbfH_ALT'] = ['nominals/latino_2125_vbfToH125toWWTo2LAndTau2Nu.root']
        signals['wzttH_ALT']= ['nominals/latino_3125_wzttH125ToWW.root']
        signals['jhu_NORM']= ['nominals/latino_1125_ggToH125toWWTo2LAndTau2Nu.root']

    elif sigtag == 'PWGSMvs2MplOthers' and mass==125:
        signals['jhu']     = ['nominals/latino_1125_ggToH125toWWTo2LAndTau2Nu.root']
        signals['vbfH']    = ['nominals/latino_2125_vbfToH125toWWTo2LAndTau2Nu.root']
        signals['wzttH']   = ['nominals/latino_3125_wzttH125ToWW.root']
               
        signals['jhu_ALT'] = ['nominals/latino_8003_Graviton2PM.root',
                              'nominals/latino_8006_Graviton2PMToWW2Tau2nu.root',
                              'nominals/latino_8009_Graviton2PMToWWLTau2nu.root'
                             ]
        signals['vbfH_ALT'] = ['nominals/latino_2125_vbfToH125toWWTo2LAndTau2Nu.root']
        signals['wzttH_ALT']= ['nominals/latino_3125_wzttH125ToWW.root']
        signals['jhu_NORM']= ['nominals/latino_1125_ggToH125toWWTo2LAndTau2Nu.root']

    else:
        raise ValueError('Signal tag %s not found for mass %d' % (sigtag,mass) )
    return signals

#--------------
# mcsets,
# list of samples and compact dictionary
#
# filter the list of samples
# and create association     label          -> label                  -> vector of root files
#                       used by mkShapes      just for association       blabla.root
#

mcsets = {
    '0j1j-JHU' : [
        #signals
        'jhu','jhu_ALT','jhu_NORM','jhu_NLO',
        # bkgs
        'WW','ggWW','VgS','Vg','WJet','Top','VV','DYTT','DYLL','WWnlo','WWnloUp','WWnloDown','TopTW','TopCtrl','WJetSS',
        # systematics
        'WJetFakeRate-eUp', 'WJetFakeRate-eDn','WJetFakeRate-mUp', 'WJetFakeRate-mDn',
        # templates
        'VgS-template', 'Vg-template','Top-template',
        # 0j1j specific
        ('DYLL-template',    'DYLL-template-0j1j'),              #    A   <-   sorgente
        ('DYLL-templatesyst','DYLL-templatesyst-0j1j')           #    mkmerged vuole "-template"
    ],
    '0j1j-JHUOthers' : [
        #signals
        'jhu','jhu_ALT','jhu_NORM','jhu_NLO','vbfH','vbfH_ALT','wzttH','wzttH_ALT',
        # bkgs
        'WW','ggWW','VgS','Vg','WJet','Top','VV','DYTT','DYLL','WWnlo','WWnloUp','WWnloDown','TopTW','TopCtrl','WJetSS',
        # systematics
        'WJetFakeRate-eUp', 'WJetFakeRate-eDn', 'WJetFakeRate-mUp', 'WJetFakeRate-mDn',
        # templates
        'VgS-template','Vg-template','Top-template',
        # 0j1j specific
        ('DYLL-template',    'DYLL-template-0j1j'),              #    A   <-   sorgente
        ('DYLL-templatesyst','DYLL-templatesyst-0j1j')           #    mkmerged vuole "-template"
    ],
    '0j1j' : [
        #signals
        'ggH','vbfH','wzttH',
        # bkgs
        'WW','ggWW','VgS','Vg','WJet','Top','VV','DYTT','DYLL','WWnlo','WWnloUp','WWnloDown','TopTW','TopCtrl','WJetSS',
        # systematics
        'WJetFakeRate-eUp', 'WJetFakeRate-eDn','WJetFakeRate-mUp', 'WJetFakeRate-mDn',
        # templates
        'VgS-template','Vg-template','Top-template',
        # 0j1j specific
        ('DYLL-template',    'DYLL-template-0j1j'),              #    A   <-   sorgente
        ('DYLL-templatesyst','DYLL-templatesyst-0j1j')           #    mkmerged vuole "-template"
    ],
    'cutbased' : [
        #signals
        'ggH','vbfH','wzttH',
        # bkgs
        'WW', 'VgS','Vg','WJet','Top','VV','DYTT',
        # templates
        'VgS-template','Vg-template',
        # replce ggWW and DYLL
        ('ggWW',    'WW'),
        ('DYLL',    'WW'),
    ],
    'vbf_sf' : [
        #signals
        'ggH','vbfH','wzttH',
        # bkgs
        #'WW','ggWW','VgS','Vg','WJet','Top','VV','DYTT','DYLL',
        'WW','ggWW','VgS','Vg','WJet','Top','VV','DYTT','DYee','DYmm'
        # templates
        'VgS-template','Vg-template',
    ],
   'vbf_of' : [
        #signals
        'ggH','vbfH','wzttH',
        # bkgs
        'WW','ggWW','VgS','Vg','WJet','Top','VV','DYTT',
        # templates
        'VgS-template','Vg-template',
        # 2j specific
        ('WJet-template',    'WJet-template-2j'),              #    A   <-   sorgente
        ('WJet-templatesyst','WJet-templatesyst-2j')           #    mkmerged vuole "-template"
    ],
    'vh_sf' : [
        #signals
        'ggH','vbfH','wH','zH','ttH',
        # bkgs
        #'WW','ggWW','VgS','Vg','WJet','Top','VV','DYTT','DYLL',
        'WW','ggWW','VgS','Vg','WJet','Top','VV','DYee','DYmm'
        # templates
        'VgS-template','Vg-template',
    ],
   'vh_of' : [
        #signals
        'ggH','vbfH','wH','zH','ttH',
        # bkgs
        'WW','ggWW','VgS','Vg','WJet','Top','VV','DYTT',
        # templates
        'VgS-template','Vg-template',
        # 2j specific
        #('WJet-template',    'WJet-template-2j'),              #    A   <-   sorgente
        #('WJet-templatesyst','WJet-templatesyst-2j')           #    mkmerged vuole "-template"
    ],
}

#--------------
def samples(mass, datatag='Data2012', sigtag='SM', mctag='all'):
    '''
    mass: mass for the higgs samples'
    datatag: tag for the dataset to be included
    sigtag: kind of signal (SM or Graviton)
    mctag: tag for the set of mc to be included
    '''
    if '2012' in datatag:
        print 'loading signals for 2012'
        signals = signalSamples(sigtag,mass)
    elif '2011' in datatag:
        print 'loading signals for 2011'
        signals = signalSamples_7TeV(sigtag,mass)
    else:
        print 'no signal samples defined'

    mcsamples = {}
    mcsamples.update(signals)
    if '2012' in datatag:
        print 'loading backgrounds for 2012'
        mcsamples.update(backgrounds)
    elif '2011' in datatag:
        print 'loading backgrounds for 2011'
        mcsamples.update(backgrounds_7TeV)
    else:
        print 'no background samples defined'

    if isinstance(mctag,list):
        mclabels = mctag
    else:
        if mctag not in mcsets:
            raise ValueError('MCtag '+mctag+' not supported')
        mclabels = mcsets[mctag]

    selectedMc = hwwtools.filterSamples( mcsamples, mclabels )

    # add data
    selectedData = {}
    if datatag == 'NoData':
        pass
    elif 'Data' in datatag:
        selectedData['Data'] = data[datatag]
    elif 'SI' in datatag:
        # add the signal samples of the given mass
        m = re.match('SI(\d+)',datatag)
        if not m:
            raise ValueError('Signal injection must have the format SImmm where mmm is the mass')
        simass = int(m.group(1))
        siSamples = signalSamples(sigtag, simass)
        # add the signal samples to the list with a _SI tag
        for s,f in siSamples.iteritems():
            selectedData[s+'-SI']=f
    else:
        raise ValueError('Data tag '+datatag+' not supported')

    samples = {}
    samples.update(selectedMc)
    samples.update(selectedData)

    return samples



