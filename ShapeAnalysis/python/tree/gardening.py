#!/bin/env python

import optparse
import sys
import ROOT
import numpy
import re
import warnings
import os.path
import traceback

import HWWAnalysis.Misc.odict as odict

# for trigger efficiency fits
from HWWAnalysis.ShapeAnalysis.hwwtools import confirm

#   _______                 
#  / ___/ /__  ___  ___ ____
# / /__/ / _ \/ _ \/ -_) __/
# \___/_/\___/_//_/\__/_/   
#                           

class TreeCloner(object):
    def __init__(self):
        self.ifile = None
        self.itree = None
        self.ofile = None
        self.otree = None
        self.label = None
    
    def _openRootFile(self,path, option=''):
        f =  ROOT.TFile.Open(path,option)
        if not f.__nonzero__() or not f.IsOpen():
            raise NameError('File '+path+' not open')
        return f

    def _getRootObj(self,d,name):
        o = d.Get(name)
        if not o.__nonzero__():
            raise NameError('Object '+name+' doesn\'t exist in '+d.GetName())
        return o

    def connect(self, tree, input):
        self.ifile = self._openRootFile(input)
        self.itree = self._getRootObj(self.ifile,tree)

    def clone(self,output,branches=[]):

        self.ofile = self._openRootFile(output, 'recreate')

        for b in self.itree.GetListOfBranches():
            if b.GetName() not in branches: continue
            b.SetStatus(0)

        self.otree = self.itree.CloneTree(0)

        ## BUT keep all branches "active" in the old tree
        self.itree.SetBranchStatus('*'  ,1)


    def disconnect(self):
        self.otree.Write()
        self.ofile.Close()
        self.ifile.Close()

        self.ifile = None
        self.itree = None
        self.ofile = None
        self.otree = None

#    ___                       
#   / _ \______ _____  ___ ____
#  / ___/ __/ // / _ \/ -_) __/
# /_/  /_/  \_,_/_//_/\__/_/   
#                              

class Pruner(TreeCloner):
    def __init__(self):
        self.filter = ''
        self.drops = []
        self.dryrun = False

    def help(self):
        return '''Produce a copy of the tree applying a filter'''

    def addOptions(self,parser):
        description=self.help()
        group = optparse.OptionGroup(parser,self.label, description)
        group.add_option('-f','--filter',dest='filter', help='cut string as undestood by TTree::Draw', default='')
        group.add_option('-d','--drop',  dest='drops',  help='drops the variables while cloning', action='append',default=[])
        group.add_option('-n','--dryrun',dest='dryrun', help='do nothing, just count', action='store_true')
        parser.add_option_group(group)
        return group

    def checkOptions(self, opts ):
        if not opts.filter and not opts.drops:
            raise ValueError('No filter defined?!?')

        self.filter = getattr(opts,'filter')
        self.dryrun = getattr(opts,'dryrun')
        self.drops  = getattr(opts,'drops')

    def process(self, **kwargs ):
        print 'Filtering \''+self.filter+'\''

        tree  = kwargs['tree']
        input = kwargs['input']
        output = kwargs['output']

        self.connect(tree,input)

        print 'Initial entries:',self.itree.GetEntries()
        evlist = ROOT.TEventList('prunerlist')
        self.itree.Draw('>>prunerlist',self.filter)
        print 'Filtered Entries',evlist.GetN()

        if self.dryrun:
            print 'Dryrun: eventloops skipped'
            return

        # do we want to support wildcards? with fnmatch?
        # complicated because here we can't access the input tree
        self.clone(output, self.drops)

        itree = self.itree
        otree = self.otree
        step = 5000
        for i in xrange(evlist.GetN()):
            if i > 0 and i%step == 0:
                print i,' events processed.'

            itree.GetEntry(evlist.GetEntry(i))

            otree.Fill()

        self.disconnect()
        print '- Eventloop completed'


#    ___                    __   _____         _____         
#   / _ )_______ ____  ____/ /  / ___/______ _/ _/ /____ ____
#  / _  / __/ _ `/ _ \/ __/ _ \/ (_ / __/ _ `/ _/ __/ -_) __/
# /____/_/  \_,_/_//_/\__/_//_/\___/_/  \_,_/_/ \__/\__/_/   
#                                                            

class Grafter(TreeCloner):
    '''Adds or replace variables to the tree'''

    def __init__(self):
        self.variables = {}
        self.regex = re.compile("([a-zA-Z0-9]*)/([FID])=(.*)")

    def help(self):
        return '''Makes a copy of the original tree adding or replacing variables'''

    def addOptions(self,parser):
        description = self.help()
        group = optparse.OptionGroup(parser,self.label, description)
        group.add_option('-v','--var',dest='variables',action='append',default=[])
        parser.add_option_group(group)
        return group

    def checkOptions(self,opts):
        if not opts.variables:
            raise ValueError('No variables defined?!?')

        for s in opts.variables:
            r = self.regex.match(s)
            if not r:
                raise RuntimeError('Malformed option '+s)
            name=r.group(1)
            type=r.group(2)
            formula=r.group(3)
            if type=='F':
                numtype = numpy.float32
            elif type=='D':
                numtype = numpy.float64
            elif type=='I':
                numtype = numpy.int32
            else:
                RuntimeError('Type '+type+' not supported')

            value=numpy.zeros(1, dtype = numtype)
            
            self.variables[name] = (value, type, formula)

    def process(self,**kwargs):

        tree  = kwargs['tree']
        input = kwargs['input']
        output = kwargs['output']

        self.connect(tree,input)

        vars = [ ( value, type, ROOT.TTreeFormula(name,formula, self.itree)) for name, (value, type, formula) in self.variables.iteritems() ]


        print 'Adding/replacing the following branches'
        template=' {0:10} | {1:^3} | "{2}"'
        for name  in sorted(self.variables):
            (value, type, formula) = self.variables[name]
            print template.format(name,type,formula)
        print


        oldbranches = [ b.GetName() for b in self.itree.GetListOfBranches() ]
        hasMutation = False
        for bname in self.variables:
            # not there, continue
            if bname not in oldbranches: continue
            # found, check for consistency
            branch = self.itree.GetBranch(bname)
            btype = self.variables[bname][1]
            newtitle = bname+'/'+btype
            if ( branch.GetTitle() != newtitle ):
                print 'WARNING: Branch mutation detected: from',branch.GetTitle(),'to',newtitle
                hasMutation = True

        if hasMutation:
            confirm('Mutation detected. Do you _really_ want to continue?') or sys.exit(0)

        self.clone(output,self.variables.keys())

        for (val,type,formula) in vars:
            name = formula.GetName()
            title = name+'/'+type
            self.otree.Branch(name,val,title)

        nentries = self.itree.GetEntries()
        print 'Entries:',nentries

        # avoid dots in the loop
        itree = self.itree
        otree = self.otree

        step = 5000
        for i in xrange(0,nentries):
            itree.GetEntry(i)

            if i > 0 and i%step == 0:
                print str(i)+' events processed.'

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                for (val,type,formula) in vars:
                    val[0] = formula.EvalInstance()

            otree.Fill()
        
        self.disconnect()
        print '- Eventloop completed'

      

#    ___   ___          _____         _____         
#   / _ | / (_)__ ____ / ___/______ _/ _/ /____ ____
#  / __ |/ / / _ `(_-</ (_ / __/ _ `/ _/ __/ -_) __/
# /_/ |_/_/_/\_,_/___/\___/_/  \_,_/_/ \__/\__/_/   
#                                                   
# TODO finish it!
class AliasGrafter(Grafter):

    def __init__(self):
#         super(AliasGrafter, self).__init__(key, value)
        pass
        

    def process(self):
        
        tree  = kwargs['tree']
        input = kwargs['input']
        output = kwargs['output']
        self.connect(tree,input)
        self.clone(output)

        for name, (value, type, formula) in self.variables.iteritems():
            self.otree.SetAlias(name,formula)

        self.disconnect()
        pass


#     ___            __ _      __    _      __   __         
#    / _ \___  ___  / /| | /| / /__ (_)__ _/ /  / /____ ____
#   / , _/ _ \/ _ \/ __/ |/ |/ / -_) / _ `/ _ \/ __/ -_) __/
#  /_/|_|\___/\___/\__/|__/|__/\__/_/\_, /_//_/\__/\__/_/   
#                                   /___/                   
class RootWeighter(TreeCloner):

    class H1WgtExtractor:
        def __init__(self,h):
            self._h = h
            self._xlo = h.GetXaxis().GetXmin()
            self._xhi = h.GetXaxis().GetXmax()

        def __call__(self,x):
            x = x if x < self._xhi else self._xhi-0.01
            x = x if x > self._xlo else self._xlo+0.01

            w = self._h.GetBinContent(self._h.FindBin(x))
            return w

    class F1WgtExtractor:
        def __init__(self,f):
            self._f = f
            self._xlo = f.GetXmin()
            self._xhi = f.GetXmax()

        def __call__(self,x):
            x = x if x < self._xhi else self._xhi-0.01
            x = x if x > self._xlo else self._xlo+0.01

            w = self._f.Eval(x)
            return w


    def __init__(self):
        pass

    def __del__(self):
        for f in ['weightfile']:
            if hasattr(self,f):
                getattr(self,f).Close()

    @staticmethod
    def _makeWgtExtractor(obj):
        
        if isinstance(obj, ROOT.TH1):
            print 'TH1 detected'
            return H1Weighter.H1WgtExtractor( obj )
        
        elif isinstance(obj, ROOT.TF1):
            print 'TF1 detected'
            return H1Weighter.F1WgtExtractor( obj )
        else:
            raise RuntimeError('cannot work with '+type(obj))

#     @staticmethod
    def _getBoundaries(self,obj):
        
        print type(obj)
        if isinstance(obj, ROOT.TH1):
            print 'TH1 detected'
            xlo = obj.GetXaxis().GetXmin()
            xhi = obj.GetXaxis().GetXmax()

        elif isinstance(obj, ROOT.TF1):
            print 'TF1 detected'
            xlo = obj.GetXmin()
            xhi = obj.GetXmax()
        else:
            raise RuntimeError('cannot work with '+type(obj))

        return (xlo,xhi,obj)

#     @staticmethod
    def _getWeight(self,x,bounds):

        xlo, xhi, hW = bounds
        
        x = x if x < xhi else xhi-0.01
        x = x if x > xlo else xlo+0.01

        w = hW.GetBinContent(hW.FindBin(x))
        return w

    def help(self):
        return '''Adds/replace a weight based on the content of a histogram'''

    def addOptions(self, parser):
        description = self.help()
        group = optparse.OptionGroup(parser,self.label, description)

        group.add_option('-p', '--path',      dest='path', help='Histogram file path',)
        group.add_option('-H', '--Histogram', dest='hist', help='Histogram name',)
        group.add_option('-k', '--key',       dest='key',  help='key variable used to extract the weight from the histogram',)
        group.add_option('-b', '--branch',    dest='branch',   help='Name of the lepton efficiency weight branch')

        parser.add_option_group(group)
        return group

    def checkOptions(self,opts):
        needed = ['branch','hist','path','key']
        if (False in [ hasattr(opts,o) for o in needed ] or 
            None in [ getattr(opts,o) for o in needed ] ):
            raise RuntimeError('Missing options: '+', '.join(needed) )


        self.weightfile  = self._openRootFile(opt.path)
        self.weightObj   = self._getRootObj(self.weightfile, opt.hist)
        self.branch      = opt.branch
        self.key         = opt.key

#         self.bounds = self._getBoundaries(self.weightObj)
        self._wgtEx       = H1Weighter._makeWgtExtractor(self.weightObj)

    def process(self, **kwargs):
        tree  = kwargs['tree']
        input = kwargs['input']
        output = kwargs['output']

        self.connect(tree,input)
        self.clone(output,[self.branch]) 

        from ctypes import c_float

        weight = numpy.ones(1, dtype=numpy.float32)
        weight = c_float(1)

        self.otree.Branch(self.branch,weight,self.branch+'/F')

        nentries = self.itree.GetEntries()
        print 'Total number of entries: ',nentries 
                
        # avoid dots to go faster
        itree     = self.itree
        otree     = self.otree

        step = 5000
        for i in xrange(nentries):
            itree.GetEntry(i)

            ## print event count
            if i > 0 and i%step == 0.:
                print i,'events processed.'

#             weight.value = self._getWeight( getattr(itree,self.key), self.bounds )
            weight.value = self._wgtEx( getattr(itree, self.key) )

            otree.Fill()

        self.disconnect()
        print '- Eventloop completed'




#    _____                              __  ___         
#   / ___/__  __ _  __ _  ___ ____  ___/ / / (_)__  ___ 
#  / /__/ _ \/  ' \/  ' \/ _ `/ _ \/ _  / / / / _ \/ -_)
#  \___/\___/_/_/_/_/_/_/\_,_/_//_/\_,_/ /_/_/_//_/\__/ 
#                                                       

class ModuleManager(odict.OrderedDict):
    
    def __setitem__(self,key,value):
        super(ModuleManager, self).__setitem__(key, value)
        value.label = key

def execute(module,tree,iofiles):
    nfiles=len(iofiles)
    for i,(ifile,ofile) in enumerate(iofiles):
        print '-'*80
        print 'Entry {0}/{1} | {2}'.format(i+1,nfiles,ifile)
        print '-'*80
        odir  = os.path.dirname(ofile)
        if odir and not os.path.exists(odir):
           os.system('mkdir -p '+odir)
           print file,ofile

        print 'Input: ',ifile
        print 'Output:',ofile
        print '-'*80
    
        module.process( input=ifile, output=ofile, tree=tree )


def gardener_cli( modules ):
    usage = '''
    Usage:
        %prog <command> <options> filein.root fileout.root
        %prog <command> <options> file1.root file2.root ... dirout
        %prog <command> -r <options> dirin dirout

    In the latter case the directory tree in dirin is rebuilt in dirout

    Valid commands:
        '''+', '.join(modules.keys()+['help'])+'''

    Type %prog <command> -h for the command specific help
    '''

    parser = optparse.OptionParser(usage)
    parser.add_option('-t','--tree',        dest='tree',                                default='latino',   help='Name of the tree to operate on (default = %default)')
    parser.add_option('-r','--recursive',   dest='recursive',   action='store_true',    default=False,      help='Recurse subdirectories (default = %default)')
    parser.add_option('-F','--force',       dest='force',       action='store_true',    default=False,      help='Don\'t ask for confirmation when recursing (default = %default)')

    # some boring argument handling
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    modname = sys.argv[1]
    if modname.startswith('-'):
        parser.print_help()
        sys.exit(0)

    if modname == 'help':
        if len(sys.argv) == 2:
            parser.print_help()
            sys.exit(0)
        
        module = sys.argv[2]
        if module not in modules:
            print 'Help: command',module,'not known'
            print 'The available commands are',', '.join(modules.keys())
            sys.exit(0)
        
        print 'Help for module',module+':'
        modules[module].help()
        modules[module].addOptions(parser)
        parser.print_help()
        sys.exit(0)


    if modname not in modules:
        print 'Command',modname,'unknown'
        print 'The available commands are',modules.keys()
        sys.exit(0)

    module = modules[modname]
    group = module.addOptions(parser)

    sys.argv.remove(modname)

    (opt, args) = parser.parse_args()

    print opt,args

    sys.argv.append('-b')

    try:
        module.checkOptions(opt)
    except Exception as e:
        print 'Error in module',module.label
#         print '*'*80
#         print 'Fatal exception '+type(e).__name__+': '+str(e)
#         print '*'*80
#         exc_type, exc_value, exc_traceback = sys.exc_info()
#         traceback.print_tb(exc_traceback, file=sys.stdout)
#         print '*'*80
        print e
        sys.exit(1)

    tree = opt.tree

    nargs = len(args)
    if nargs < 2:
        parser.error('Input and/or output files missing')


    # file1 file2 file3 > outdir
    elif nargs > 2:
        inputs = args[:-1]
        output = args[-1]

        print inputs
        
        # sanitise output
        output = output if output[-1]=='/' else output+'/'
        iofiles = [ (f,os.path.join(output,os.path.basename(f))) for f in inputs ]

        execute( module, tree, iofiles )
    
    elif nargs == 2:
        input  = args[0]
        output = args[1]


        # recursiveness here
        if os.path.isdir(input):
            if not opt.recursive:
                print input,'is a directory. Use -r to go recursive'
                sys.exit(0)

            # sanitize the input/output
            input  = input  if input [-1]=='/' else input +'/'
            output = output if output[-1]=='/' else output+'/'

            if os.path.exists(output) and not os.path.isdir(output):
                print output,'exists and is not a directory!'
                sys.exit(0)

            fileList = []
            for root, subFolders, files in os.walk(input):
                for file in files:
                    if not file.endswith('.root'): continue
                    fileList.append(os.path.join(root,file))

            print 'The directory tree',input,'will be gardened and copied to',output
            print 'The following files will be copied:'
            print '\n'.join(fileList)
            print 'for a grand total of',len(fileList),'files'
            opt.force or ( confirm('Do you want to continue?') or sys.exit(0) )

            iofiles = [ (f,f.replace(input,output)) for f in fileList ]

            execute( module, tree, iofiles )

        else:
            if os.path.exists(output) and os.path.isdir(output):
                # sanitise output
                output = output if output[-1]=='/' else output+'/'
                output = os.path.join( output , os.path.basename(input) )
            execute(module,tree,[(input,output)])


if __name__ == '__main__':

    modules = ModuleManager()
    modules['filter']     = Pruner()
    modules['wwfilter']   = WWPruner()
    modules['adder']      = Grafter()
    modules['wwflagger']  = WWFlagsGrafter()
    modules['puadder']    = PUpper()
    modules['effwfiller'] = EffLepFiller()
    modules['efftfiller'] = EffTrgFiller()
    modules['h1weighter'] = H1Weighter()

    gardener_cli( modules )
