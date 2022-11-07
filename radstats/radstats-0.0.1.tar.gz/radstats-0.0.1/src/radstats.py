### Stephen Lawrence, 2022

"""radstats -- radiation effects system modeling tool

"""

__version__ = "0.0.1"

from lxml import etree
import schemdraw
from schemdraw import flow,logic,segments
from PIL import Image
import pickle
import numpy as np
import pandas as pd
from scipy.integrate import cumtrapz
from scipy.interpolate import interp1d
from scipy.special import erf
import sys
import itertools

# import ctypes
# os.system('cc -fPIC -shared -o bayes.o bayes.c')
# bayes = ctypes.CDLL('bayes.o')

#####################################################################################################

class Box:
    """System element representing a logical combination of immediate subelements (a.k.a. children).

    Args:
        name (str): Unique identifier string for this Box.
        children (list): List of radstats.Effect or other radstats.Box objects that serve as inputs to this Box.
        gate (str): Logic gate descibing how the Box propagates values from its children.

    Returns:
        (radstats.Box): Object representing the system element.

    """
    def __init__(self,name:str,children:list=[],gate:str='OR',**kwargs):
        ### initialize attributes
        self.name = name
        self.children = children
        self.gate = gate
        ### update attributes from kwargs
        self.__dict__.update(kwargs)

    def __str__(self):
        string = f"{repr(self)}\n{etree.tostring(self.XML(),encoding='unicode',pretty_print=True)}"
        for series in string.split('="[')[1:]:
            series = series.split(']"')[0]
            string = string.replace(series,f'{series.split()[0]} ... {series.split()[-1]}')
        return string

    def __repr__(self): return object.__repr__(self).replace(' at',f' "{self.name}" at')

    def XML(self):
        """Convert the Box to XML format.

        Returns:
            (lxml.etree.Element) : XML element representing the Box and its descendants.

        """
        xml = etree.Element('box',{'name':self.name,'gate':self.gate})
        for child in self.children: xml.append(child.XML())
        return xml

    def to_xml(self,file):
        """Export the Box to an XML file.

        Args:
            file (str) : Path to save location.

        """
        open(file,'w').write(etree.tostring(self.XML(),encoding='unicode',pretty_print=True))

    def to_pickle(self,file):
        """Export the Box using Pickle.

        Args:
            file (str) : Path to save location.

        """
        pickle.dump(self,open(file,'wb'))

    def FT(self,file:str='.temp/ft.png',scale:int=3,shape:tuple=(3.5,1),spacing:tuple=(4,4),fontsize:int=36):
        """Generate a fault tree diagram of the Box and its descendants.

        Returns:
            (PIL.Image) : PIL-style Image object of the fault tree diagram.

        """
        system = self.XML()
        ### get element positions
        effects = system.xpath('.//*[local-name()="effect" or local-name()="ref"]')
        pos = {}
        for i,effect in enumerate(effects):
            pos[effect] = (i * spacing[0],-spacing[1] * len(effect.xpath('ancestor::box')))
        boxes = system.xpath('..//box')
        while len(boxes) > 0:
            for box in boxes:
                inputs = [i for i in box.xpath('*')]
                if all([i in pos.keys() for i in inputs]):
                    boxes.remove(box)
                    x = sum([pos[i][0] for i in inputs]) / len(inputs)
                    y = max([pos[i][1] for i in inputs]) + spacing[1]
                    pos[box] = (x,y)
        boxes = system.xpath('..//box')
        ### draw diagram
        schemdraw.config(inches_per_unit=scale,fontsize=fontsize*scale,lw=1.5*scale,font='Times New Roman') # monospace?
        with schemdraw.Drawing(file=file,show=False) as d:
            for effect in effects:
                [x,y] = shape
                label = effect.get('name')
                if len(label)/4 > x: x = len(label)/4
                if effect.tag == 'effect':
                    d += flow.Terminal(w=x,h=y).anchor('N').at(pos[effect]).label(label)
                if effect.tag == 'ref':
                    d += (new := flow.Box(w=x,h=y).anchor('N').at(pos[effect]).label('\n'+label))
                    new.segments.pop(0)
                    new.segments.append(segments.Segment([(0,-y/2),(x,-y/2)]))
                    new.segments.append(segments.Segment([(0,-y/2),(x/2,y/2)]))
                    new.segments.append(segments.Segment([(x/2,y/2),(x,-y/2)]))
            for box in boxes:
                [x,y] = shape
                label = box.get('name')
                if len(label)/4 > x: x = len(label)/4
                if box.get('name') in [n.get('name') for n in system.xpath('.//ref')]:
                    d += (new := flow.Box(w=x,h=y).anchor('N').at(pos[box]).label('\n'+label))
                    new.segments.pop(0)
                    new.segments.append(segments.Segment([(0,-y/2),(x,-y/2)]))
                    new.segments.append(segments.Segment([(0,-y/2),(x/2,y/2)]))
                    new.segments.append(segments.Segment([(x/2,y/2),(x,-y/2)]))
                else:
                    d += (new := flow.Box(w=x,h=y).anchor('N').at(pos[box]).label(label))
                if box.get('gate') == 'OR': d += (new := logic.Or(inputs=1).at(new.S).down().reverse())
                if box.get('gate') == 'AND': d += (new := logic.And(inputs=1).at(new.S).down().reverse())
                for sub in box.xpath('*'): d += flow.Wire('-|').at(new.in1).to(pos[sub])
        ### post process image
        image = Image.open(file)
        image.crop(image.getbbox())
        image.save(file)
        return image

    def find(self,name:str):
        """Find the first subelement of the Box matching a given `name`.

        Args:
            name (str) : Unique name of desired element.

        Returns:
            (radstats.Box or radstats.Effect) : Subelement matching the given `name`.

        """
        for child in self.children:
            if child.name == name: return child
            elif type(child) == Effect: continue
            else:
                found = child.find(name)
                if found is not None: return found
        return None
    
    def find_all(self):
        """Find all subelements of the Box.

        Returns:
            (list) : List of radstats.Box and/or radstats.Effect representing all subelements.

        """
        children = []
        for child in self.children:
            if type(child) == Box: children.append(child.find_all())
            children.append([child])
        return list(itertools.chain.from_iterable(children))

    def import_rates(self,file:str):
        """Import Poisson event or dose accumulation rates from a CSV.

        Note: Element `rates` are overwritten with the CSV column where the header matches the `name` of the Effect.
        
        For example ::
            {
                Effect1,Effect2,Effect3
                1,4,7
                2,5,8
                3,6,9
            }

        Leads to ::
            {
                Effect1.rates = [1,2,3]
                Effect2.rates = [4,5,6]
                Effect3.rates = [7,8,9]
            }

        Args:
            file (str) : path to properly formatted CSV file.

        """
        df = pd.read_csv(file)
        for name in df.columns:
            child = self.find(name)
            if child is not None: child.rate = df[name].to_numpy()

    def Q(self,time:list,file:str=None,**kwargs):
        """Compute the unavailability :math:`Q(t)` of the Box and its descendants given a time index.

        Args:
            time (iterable) : Numerical time index for the analysis (in seconds).
            file (str) : File to optionally save the results in CSV format.

        Returns:
            (dict) : Dictionary of lists containing the analysis results along with the time index.

        Keyword Args:
            force (dict) : Force a certain unavailability on specific elements, formatted as {name:forced_Q}.

        """
        force = kwargs['force'] if 'force' in kwargs.keys() else {}
        q = pd.DataFrame({'Time':time}).set_index('Time')
        if self.name in force.keys(): q[self.name] = force[self.name]
        else:
            for child in self.children: q = q.join(child.Q(time,force=force))
            f = getattr(sys.modules['bayes'],self.gate)
            q[self.name] = [f([q[child.name][t] for child in self.children]) for t in time]
        if file is not None: q.to_csv(kwargs['file'])
        return q


    def I(self,time:list,file:str=None):
        """Compute importance and worth metrics of the Box and its descendants given a time index.

        The metrics returned by this function are
            - Marginal importance :math:`I_M(t)=P_t(Z|A)-P_t(Z|A')`
            - Critical importance :math:`I_C(t)=I_M(t) P_t(A)/P_t(Z)`
            - Risk achievement worth :math:`\mathcal{A}(t)=P_t(Z|A)-P_t(Z)`
            - Risk reduction worth :math:`\mathcal{D}(t)=P_t(Z|A')-P_t(Z)`
        Where :math:`Z` is the Box calling the function and and :math:`A` is a descendant.

        Args:
            time (iterable) : Numerical time index for the analysis (in seconds).
            file (str) : File to optionally save the results in CSV format.

        Returns: 
            (dict) : Dictionary of lists containing the marginal importance of elements (sorted by name) along with the time index.

        """
        Q = self.Q(time)
        raw = pd.DataFrame(index=Q.index)
        rrw = pd.DataFrame(index=Q.index)
        im = pd.DataFrame(index=Q.index)
        ic = pd.DataFrame(index=Q.index)
        for sub in self.find_all() + [self]:
            yesQ = self.Q(time,force={sub.name:1})[self.name]
            notQ = self.Q(time,force={sub.name:0})[self.name]
            raw[sub.name] = np.subtract(yesQ,Q[self.name])
            rrw[sub.name] = np.subtract(notQ,Q[self.name])
            im[sub.name] = np.subtract(yesQ,notQ)
            ic[sub.name] = im[sub.name] * np.divide(Q[sub.name],Q[self.name]+1e-15)
        return {'M':im,'C':ic,'RAW':raw,'RRW':rrw}

#####################################################################################################

class Effect:
    """System element representing a radiation-induced failure mode.

    Args:
        name (str) : Unique identifier string for this Effect.
        type (str) : Type of effect (`SEE`, `TID`, or `DDD`). If `None`, the effect type will be deduced based on the `name`.
        rate (float or iterable) : Poisson event rate :math:`\lambda(t)` or dose accumulation rate :math:`\dot{D}(t)` (per second).

    Returns:
        (radstats.Effect) : Object representing the system element.

    Keyword Args:
        mttr (float) : Mean Time To Repair :math:`1/\mu_r` (in seconds), if any -- only relevant for SEE.
        mean (float) : Lognormal mean :math:`\mu_{\ln}` of failure doses -- only relevant for TDE.
        sd (float) : Lognormal standard deviation :math:`\sigma_{\ln}` of failure doses -- only relevant for TDE.

    """
    def __init__(self,name:str,type:str=None,rate:float=0,**kwargs):
        ### initialize attributes
        self.name = name
        self.type = type
        self.rate = rate
        if type is None:
            if 'SEL' in self.name: self.type = 'SEE'
            elif 'SEFI' in self.name: self.type = 'SEE'
            elif 'DSEE' in self.name: self.type = 'SEE'
            elif 'TID' in self.name: self.type = 'TID'
            elif 'DDD' in self.name: self.type = 'DDD'
        ### update attributes from kwargs
        self.__dict__.update(kwargs)
        
    def __str__(self):
        string = f"{repr(self)}\n{etree.tostring(self.XML(),encoding='unicode',pretty_print=True)}"
        for series in string.split('="[')[1:]:
            series = series.split(']"')[0]
            string = string.replace(series,f'{series.split()[0]} ... {series.split()[-1]}')
        return string

    def __repr__(self): return object.__repr__(self).replace(' at',f' "{self.name}" at')
    
    def XML(self):
        """Convert Effect to an XML format.

        Returns:
            (lxml.etree.Element) : XML element object representing the Effect.

        """
        return etree.Element('effect',{k:str(v) for k,v in self.__dict__.items()})
    
    def to_xml(self,file:str):
        """Export the Effect to an XML file.

        Args:
            file (str) : Path to save location.

        """
        open(file,'w').write(etree.tostring(self.XML(),encoding='unicode',pretty_print=True))

    def to_pickle(self,file:str):
        """Export the Effect using Pickle.

        Args:
            file (str) : Path to save location.

        """
        pickle.dump(self,open(file,'wb'))

    def import_rates(self,file:str):
        """Import Poisson event or dose accumulation rates from a CSV.

        Note: Element `rates` are overwritten with the CSV column where the header matches the `name` of the Effect.
        
        For example ::
            Effect1,Effect2,Effect3
            1,4,7
            2,5,8
            3,6,9

        Leads to ::
            Effect1.rates = [1,2,3]
            Effect2.rates = [4,5,6]
            Effect3.rates = [7,8,9]

        Args:
            file (str) : path to properly formatted CSV file.

        """
        df = pd.read_csv(file)
        if self.name in df.columns: self.rate = df[self.name].to_numpy()
    
    def Q(self,time:list,file:str=None,**kwargs):
        """Compute the unavailability :math:`Q(t)` of the Effect given a time index.

        Args:
            time (iterable) : Numerical time index for the analysis (in seconds).
            file (str) : File to optionally save the results in CSV format.

        Returns:
            (dict) : Dictionary of lists containing the analysis results along with the time index.

        Keyword Args:
            force (dict) : Force a certain unavailability on specific elements, formatted as {name:forcedQ}.

        """
        q = pd.DataFrame({'Time':time}).set_index('Time')
        force = kwargs['force'] if 'force' in kwargs.keys() else {}
        if self.name in force.keys(): q[self.name] = force[self.name]
        else:
            if self.type == 'SEE':
                rate = rescale(np.array(self.rate),time)
                if hasattr(self,'mttr'): q[self.name] = rate/(rate+rescale(1/np.array(float(self.mttr)),time))
                else: q[self.name] = 1 - np.exp(-cumtrapz(rate,time,initial=0))
            elif self.type == 'TID':
                rate = rescale(np.array(self.rate),time)
                dose = cumtrapz(rate,time,initial=1e-15)
                q[self.name] = (1/2)*(1+erf((np.log(dose)-float(self.mean))/(float(self.sd)*np.sqrt(2))))
        if file is not None: q.to_csv(kwargs['file'])
        return q

#####################################################################################################

def rescale(y,x):
    try: n = len(y)
    except TypeError: y = [y,y]; n = len(y)
    interp = interp1d(np.linspace(0,1,n),y)
    return interp(x / max(x))

def parse_xml(element):
    if element.tag == 'effect': return Effect(**element.attrib)
    elif element.tag == 'box':
        box = Box(**element.attrib)
        box.children = [parse_xml(child) for child in element]
        return box

def from_xml(file):
    tree = etree.parse(file)
    root = tree.getroot()
    return parse_xml(root)

def from_pickle(file):
    return pickle.load(open(file,'rb'))

#####################################################################################################
#####################################################################################################

import numpy as np
import itertools

decimals = 20

#####################################################################################################

class bayes:
    def marginal(probs):
        Pmarg = [None] * (2 ** len(probs))
        for i,truth in enumerate(itertools.product([True,False],repeat=len(probs))):
            Pmarg[i] = np.prod([p if truth[n] else 1 - p for n,p in enumerate(probs)])
        return np.around(Pmarg,decimals)

    def OR(probs):
        Pmarg = bayes.marginal(probs)
        Pcond = np.ones(len(Pmarg))
        Pcond[-1] = 0
        return np.around(np.dot(Pcond,Pmarg),decimals)

    def AND(probs):
        Pmarg = bayes.marginal(probs)
        Pcond = np.zeros(len(Pmarg))
        Pcond[0] = 1
        return np.around(np.dot(Pcond,Pmarg),decimals)

    def VOTE2(probs):
        Pmarg = bayes.marginal(probs)
        Pcond = [sum(i) >= 2 for i in itertools.product([True,False],repeat=len(probs))]
        return np.around(np.dot(Pcond,Pmarg),decimals)
