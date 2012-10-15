#!/usr/bin/env python

import hwwinfo
import logging
import os.path


class AlienDict(dict):
    """Implementation of perl's autovivification feature."""
    def __init__(self,*args, **kwargs):
        # init the dict
        super(self.__class__,self).__init__(self, *args, **kwargs)
        self._lock = False
    
    def lock(self):
        self._lock = True
        for a in self.itervalues():
            if type(a) == type(self):
                a.lock()

    def unlock(self):
        self._lock = False
        for a in self.itervalues():
            if type(a) == type(self):
                a.unlock()

    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            if self._lock:
                raise
            else:
                value = self[item] = type(self)()
                return value

class DDCardReader:
    _logger = logging.getLogger("DDCardReader")
    def __init__(self, path):
        self._path = path

        self._iszombie = False
        self._read()

    @property
    def iszombie(self): return self._iszombie

    def _read(self):
        if not self._path:
            print 'No datadriven'
            self._iszombie = True
            return

        print 'Reading data driven estimates from',self._path

        # data driven systematics
        basemapping  = {'of_0j': ('0j',['of']), 'sf_0j': ('0j',['sf']),
                       'of_1j': ('1j',['of']), 'sf_1j': ('1j',['sf']),
                       'of_2j': ('2j',['of']), 'sf_2j': ('2j',['sf'])}
        wwmapping    = {'of_0j': ('0j',['of']), 'sf_0j': ('0j',['sf']),
                       'of_1j': ('1j',['of']), 'sf_1j': ('1j',['sf']),
                       }
        llmapping   = {'sf_0j': ('0j',['sf']), 
                       'sf_1j': ('1j',['sf']),
                       }
        lleemmmapping  = {
                       'sf_2j': ('2j',['sf'])
                       }

        readmap = {}
        readmap['Top']  = basemapping.copy()
        readmap['WW']   = wwmapping.copy()
        readmap['ggWW'] = wwmapping.copy()
        readmap['DYLL'] = llmapping.copy()
        readmap['DYee'] = lleemmmapping.copy()
        readmap['DYmm'] = lleemmmapping.copy()


        ddcards = AlienDict()

        for p,mapping in readmap.iteritems():
            for ch,(cat,fls) in mapping.iteritems():
                self._logger.debug('- '+p+' '+ch+' '+cat+' '+str(fls))

                try:
                    cards = [ self._load(p,cat,fl) for fl in fls ]
                except IOError as ioe:
                    self._logger.info(str(ioe))
                    continue;

                masses = cards[0].keys()
                check = [ (masses == card.keys()) for card in cards ]

                if check.count(False) > 0:
                    raise RuntimeError('Sanity check failed')


                for mass in masses:
                    value = None
                    for card in cards:
                        value = value+card[mass] if value else card[mass] 

                    ddcards[mass][ch][p] = value

        ddcards.lock()
        self.estimates = ddcards

    def _load(self,process, cat, channel):
        ''' Read the Data driven datacar for a given process, jet bin, channel at all masses'''
        
        filename = os.path.join( self._path,'{0}Card_{1}_{2}.txt'.format(process,channel,cat) )
        self._logger.debug('opening file: '+filename)
        cardFile = open(filename)
        card = {}
        for line in cardFile:
            # <mass> <events in ctrl region> <scale factor> <unc scale factor>
            tokens = line.split()
            mass = int(tokens[0])
            evInCtrlReg = int(float(tokens[1]))
            scale2Sig = float(tokens[2])
            scale2SigUnc = float(tokens[3])
            if len(tokens) >= 5  :
              scale2SigUncCorr = float(tokens[4])
            else :
              scale2SigUncCorr = -1

    #         card[mass] = (evInCtrlReg, scale2Sig, scale2SigUnc)
            if scale2SigUncCorr == -1 :
                card[mass] = DDEntry(evInCtrlReg, scale2Sig, scale2SigUnc)
            else :
                card[mass] = DDEntry(evInCtrlReg, scale2Sig, scale2SigUnc, scale2SigUncCorr)

        cardFile.close()
        return card


    def get(self, mass, channel):
        try:
            return (self.estimates[mass][channel],(mass,channel))
        except KeyError as ke:
            raise KeyError('{0} {1}'.format(mass,channel))

class DDEntry:
    def __init__(self,Nctr,alpha,delta,deltaCorr=0):
        self.Nctr     = Nctr
        self.alpha = alpha
        self.delta = delta
        self.deltaCorr = deltaCorr

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '(Nctr = {Nctr}, alpha = {alpha:.3f}, delta = {delta:.3f})'.format(**self.__dict__)

    def __add__(self,other):
        sum = DDEntry(0,0,0)
        if self.Nctr != other.Nctr:
            raise ValueError('Trying to add 2 entries with different Nctr: {0}, {1}'.format(self.Nctr,other.Nctr))
        
        sum.Nctr = self.Nctr
        sum.alpha = self.alpha+other.alpha
        sum.delta = self.delta+other.delta

        return sum

    def Nsig(self):
        return self.Nctr*self.alpha

    def Usig(self):
        return self.Nctr*self.delta
        
class DDWWFilter:
    _logger = logging.getLogger("DDWWFilter")

    def __init__(self, reader, nowwabove):
        self._reader    = reader
        self._nowwabove = nowwabove
        if self._nowwabove:
            self._logger.debug('Filtering WW data driven for masses >  %d',self._nowwabove)
        else:
            self._logger.debug('WW datadriven will be applied at all masses')

        #print self._nowwabove, not self._nowwabove
        #for i in xrange(100,1000,50):
        #    print i,self.haswwdd(i)

    def haswwdd(self, mass):
        return (not self._nowwabove or mass < self._nowwabove)

    def get(self, mass,channel):
        import copy

        x,y = self._reader.get(mass,channel)
        z = copy.deepcopy(x)

#         if mass >= self._noddmass:
        if not self.haswwdd(mass):
            for p in ['WW','ggWW']:
              if p in z:
                del z[p]

        return z,y





if __name__ == '__main__':
    print 'DDCardReader test'
    logging.basicConfig(level=logging.DEBUG)

    ddPath = "/shome/thea/HWW/work/shape2012/data/Anal_HWW/"
    ddPath = '/shome/thea/HWW/work/shape2012/data/bdt_2012_51fb/'
    reader = DDCardReader(ddPath)

    ddcards = reader.estimates

#     print ddcards[130]['2j']['DYLL']
    print ddcards[130]['sf_0j']['DYLL']
    print ddcards[160]['of_1j']['WW']
    print ddPath
    print '190','of_0j', reader.get(190,'of_0j')
    print '190','of_1j', reader.get(190,'of_1j')
    print '190','sf_0j', reader.get(190,'sf_0j')
    print '190','sf_1j', reader.get(190,'sf_1j')
    print '-'*100
    e,d = reader.get(190,'sf_0j')
    eWW = e['WW']

    print '190',0,'sf', eWW.Nsig(), eWW.Usig(), eWW.delta/eWW.alpha

    filt = DDWWFilter(reader)

    e,d = filt.get(300,'sf_0j')
    print e

