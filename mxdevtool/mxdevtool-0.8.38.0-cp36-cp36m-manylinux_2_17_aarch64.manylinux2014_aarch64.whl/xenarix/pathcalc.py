import mxdevtool as mx
import mxdevtool.utils as utils
import inspect, numbers
from typing import List


class DeterministicParameter(mx.core_DeterministicParameter):
    def __init__(self, times: List[float], values: List[float]):
        self._times = times
        self._values = values
        mx.core_DeterministicParameter.__init__(self, times, values)

    @staticmethod
    def fromDict(d: dict, mrk=mx.MarketData()):
        if isinstance(d, numbers.Number):
            return DeterministicParameter(['1Y', '100Y'], [d, d])

        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, DeterministicParameter.__name__)

        times = d['times']
        values = d['values']

        return DeterministicParameter(times, values)

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__
        res['times'] = self._times
        res['values'] = self._values

        return res

    def clone(self, **kwargs):
        args = []

        for arg in ['times', 'values']:
            args.append(kwargs.get(arg, getattr(self, '_{0}'.format(arg))))

        return DeterministicParameter(*args)

# models ----------------------------

class GBMConst(mx.core_GBMConstModel):
    # compounded rate is required
    def __init__(self, name: str, x0: float, rf: float, div: float, vol: float):
        self._x0 = x0
        self._rf = rf
        self._div = div
        self._vol = vol

        mx.core_GBMConstModel.__init__(self, name, x0, rf, div, vol)

    def clone(self, **kwargs):
        name = kwargs.get('name', self.name)
        args = []

        for arg in ['x0', 'rf', 'div', 'vol']:
            args.append(kwargs.get(arg, getattr(self, '_{0}'.format(arg))))

        return GBMConst(name, *args)


class GBM(mx.core_GBMModel):
    def __init__(self, name: str, x0, rfCurve: mx.YieldTermStructure, divCurve: mx.YieldTermStructure, volTs: mx.BlackVolTermStructure):

        self._x0 = x0
        self._rfCurve = rfCurve
        self._divCurve = divCurve
        self._volTs = volTs

        mx.core_GBMModel.__init__(self, name, x0, rfCurve, divCurve, volTs)

    def clone(self, **kwargs):
        name = kwargs.get('name', self.name)
        args = []

        for arg in ['x0', 'rfCurve', 'divCurve', 'volTs']:
            args.append(kwargs.get(arg, getattr(self, '_{0}'.format(arg))))

        return GBM(name, *args)


class Heston(mx.core_HestonModel):
    def __init__(self, name: str, x0: float, rfCurve: mx.YieldTermStructure, divCurve: mx.YieldTermStructure, 
                 v0: float, volRevertingSpeed: float, longTermVol: float, volOfVol: float, rho: float):

        self._x0 = x0
        self._rfCurve = rfCurve
        self._divCurve = divCurve
        self._v0 = v0
        self._volRevertingSpeed = volRevertingSpeed
        self._longTermVol = longTermVol
        self._volOfVol = volOfVol
        self._rho = rho

        mx.core_HestonModel.__init__(self, name, x0, rfCurve, divCurve, v0, volRevertingSpeed, longTermVol, volOfVol, rho)

    def clone(self, **kwargs):
        name = kwargs.get('name', self.name)
        args = []

        for arg in ['x0', 'rfCurve', 'divCurve', 'v0', 'volRevertingSpeed', 'longTermVol', 'volOfVol', 'rho']:
            args.append(kwargs.get(arg, getattr(self, '_{0}'.format(arg))))

        return Heston(name, *args)


class CIR1F(mx.core_CIR1FModel):
    def __init__(self, name: str, r0: float, alpha: float, longterm: float, sigma: float):
        self._r0 = r0
        self._alpha = alpha
        self._longterm = longterm
        self._sigma = sigma

        self.fixParameters = [False] * 4 # this for calibration

        mx.core_CIR1FModel.__init__(self, name, r0, alpha, longterm, sigma)

    def clone(self, **kwargs):
        name = kwargs.get('name', self.name)
        r0 = kwargs.get('r0', self._r0)
        alpha = kwargs.get('alpha', self._alpha)
        longterm = kwargs.get('longterm', self._longterm)
        sigma = kwargs.get('sigma', self._sigma) 
        fixParameters = kwargs.get('fixParameters', self.fixParameters)

        if 'calibrated_parameters' in kwargs:
            calibrated_parameters = kwargs['calibrated_parameters']

            r0 = calibrated_parameters[0]
            alpha = calibrated_parameters[1]
            longterm = calibrated_parameters[2]
            sigma = calibrated_parameters[3]
        
        model = CIR1F(name, r0, alpha, longterm, sigma)
        model.fixParameters = fixParameters

        return model


class Vasicek1F(mx.core_Vasicek1FModel):
    def __init__(self, name: str, r0: float, alpha: float, longterm: float, sigma: float):

        self._r0 = r0
        self._alpha = alpha
        self._longterm = longterm
        self._sigma = sigma

        self.fixParameters = [False] * 4 # this for calibration

        mx.core_Vasicek1FModel.__init__(self, name, r0, alpha, longterm, sigma)

    def clone(self, **kwargs):
        name = kwargs.get('name', self.name)
        r0 = kwargs.get('r0', self._r0)
        alpha = kwargs.get('alpha', self._alpha)
        longterm = kwargs.get('longterm', self._longterm)
        sigma = kwargs.get('sigma', self._sigma) 
        fixParameters = kwargs.get('fixParameters', self.fixParameters)

        if 'calibrated_parameters' in kwargs:
            calibrated_parameters = kwargs['calibrated_parameters']
            r0 = calibrated_parameters[0]
            alpha = calibrated_parameters[1]
            longterm = calibrated_parameters[2]
            sigma = calibrated_parameters[3]
            
        model = Vasicek1F(name, r0, alpha, longterm, sigma)
        model.fixParameters = fixParameters
        
        return model


class HullWhite1F(mx.core_HullWhite1FModel):
    def __init__(self, name: str, fittingCurve: mx.YieldTermStructure, alphaPara: DeterministicParameter, sigmaPara: DeterministicParameter):

        self._fittingCurve = fittingCurve
        self._alphaPara = alphaPara
        self._sigmaPara = sigmaPara
        
        self.fixParameters = [False] * (len(alphaPara._values) + len(sigmaPara._values)) # this for calibration

        mx.core_HullWhite1FModel.__init__(self, name, fittingCurve, alphaPara, sigmaPara)

    def clone(self, **kwargs):
        name = kwargs.get('name', self.name)
        fittingCurve = kwargs.get('fittingCurve', self._fittingCurve)
        alphaPara = kwargs.get('alphaPara', self._alphaPara)
        sigmaPara = kwargs.get('sigmaPara', self._sigmaPara)
        fixParameters = kwargs.get('fixParameters', self.fixParameters)

        if 'calibrated_parameters' in kwargs:
            calibrated_parameters = kwargs['calibrated_parameters']
            alphaPara = DeterministicParameter(self._alphaPara._times, calibrated_parameters[:len(self._alphaPara._values)])
            sigmaPara = DeterministicParameter(self._sigmaPara._times, calibrated_parameters[len(self._alphaPara._values):])
            
        model = HullWhite1F(name, fittingCurve, alphaPara, sigmaPara)
        model.fixParameters = fixParameters
        
        return model


class BK1F(mx.core_BK1FModel):
    def __init__(self, name: str, fittingCurve: mx.YieldTermStructure, alphaPara: DeterministicParameter, sigmaPara: DeterministicParameter):

        self._fittingCurve = fittingCurve
        self._alphaPara = alphaPara
        self._sigmaPara = sigmaPara

        self.fixParameters = [False] * (len(alphaPara._values) + len(sigmaPara._values)) # this for calibration

        mx.core_BK1FModel.__init__(self, name, fittingCurve, alphaPara, sigmaPara)

    def clone(self, **kwargs):
        name = kwargs.get('name', self.name)
        fittingCurve = kwargs.get('fittingCurve', self._fittingCurve)
        alphaPara = kwargs.get('alphaPara', self._alphaPara)
        sigmaPara = kwargs.get('sigmaPara', self._sigmaPara)
        fixParameters = kwargs.get('fixParameters', self.fixParameters)

        if 'calibrated_parameters' in kwargs:
            calibrated_parameters = kwargs['calibrated_parameters']
            alphaPara = DeterministicParameter(self._alphaPara._times, calibrated_parameters[:len(self._alphaPara._values)])
            sigmaPara = DeterministicParameter(self._sigmaPara._times, calibrated_parameters[len(self._alphaPara._values):])

        model = BK1F(name, fittingCurve, alphaPara, sigmaPara)
        model.fixParameters = fixParameters
        
        return model            


class G2Ext(mx.core_GTwoExtModel):
    def __init__(self, name: str, fittingCurve: mx.YieldTermStructure, 
                 alpha1: float, sigma1: float, alpha2: float, sigma2: float, corr: float):

        self._fittingCurve = fittingCurve
        self._alpha1 = alpha1
        self._sigma1 = sigma1
        self._alpha2 = alpha2
        self._sigma2 = sigma2
        self._corr = corr

        self.fixParameters = [False] * 5 # this for calibration

        mx.core_GTwoExtModel.__init__(self, name, fittingCurve, alpha1, sigma1, alpha2, sigma2, corr)

    def clone(self, **kwargs):
        name = kwargs.get('name', self.name)
        fittingCurve = kwargs.get('fittingCurve', self._fittingCurve)
        alpha1 = kwargs.get('alpha1', self._alpha1)
        sigma1 = kwargs.get('sigma1', self._sigma1)
        alpha2 = kwargs.get('alpha2', self._alpha2)
        sigma2 = kwargs.get('sigma2', self._sigma2)
        corr = kwargs.get('corr', self._corr)
        fixParameters = kwargs.get('fixParameters', self.fixParameters)
        
        if 'calibrated_parameters' in kwargs:
            calibrated_parameters = kwargs['calibrated_parameters']
            alpha1 = calibrated_parameters[0]
            sigma1 = calibrated_parameters[1]
            alpha2 = calibrated_parameters[2]
            sigma2 = calibrated_parameters[3]
            corr = calibrated_parameters[4]

        model = G2Ext(name, fittingCurve, alpha1, sigma1, alpha2, sigma2, corr)
        model.fixParameters = fixParameters
        
        return model                 


# operators -----------------------------
class PlusOper(mx.core_PlusOperCalc):
    def __init__(self, pc: mx.core_ProcessValue):
        self._pc = pc
        mx.core_PlusOperCalc.__init__(self, pc)


class MinusOper(mx.core_MinusOperCalc):
    def __init__(self, pc: mx.core_ProcessValue):
        self._pc = pc
        mx.core_MinusOperCalc.__init__(self, pc)


class AdditionOper(mx.core_AdditionOperCalc):
    def __init__(self, pc1: mx.core_ProcessValue, pc2: mx.core_ProcessValue):
        self._pc1 = pc1
        self._pc2 = pc2
        mx.core_AdditionOperCalc.__init__(self, pc1, pc2)


class SubtractionOper(mx.core_SubtractionOperCalc):
    def __init__(self, pc1: mx.core_ProcessValue, pc2: mx.core_ProcessValue):
        self._pc1 = pc1
        self._pc2 = pc2
        mx.core_SubtractionOperCalc.__init__(self, pc1, pc2)


class MultiplicationOper(mx.core_MultiplicationOperCalc):
    def __init__(self, pc1: mx.core_ProcessValue, pc2: mx.core_ProcessValue):
        self._pc1 = pc1
        self._pc2 = pc2
        mx.core_MultiplicationOperCalc.__init__(self, pc1, pc2)


class DivisionOper(mx.core_DivisionOperCalc):
    def __init__(self, pc1: mx.core_ProcessValue, pc2: mx.core_ProcessValue):
        self._pc1 = pc1
        self._pc2 = pc2
        mx.core_DivisionOperCalc.__init__(self, pc1, pc2)


# calcs -----------------------------

class Identity(mx.core_IdentityWrapperCalc):
    def __init__(self, name: str, pc: mx.core_ProcessValue):
        self._pc = pc

        mx.core_IdentityWrapperCalc.__init__(self, name, pc)

    def toDict(self):
        return self._pc.toDict()


class YieldCurve(mx.core_YieldCurveValueCalc):
    def __init__(self, name: str, yieldCurve: mx.YieldTermStructure, output_type='spot', compounding=mx.Compounded):

        self._yieldCurve = yieldCurve
        self._output_type = output_type
        self._compounding = compounding

        mx.core_YieldCurveValueCalc.__init__(self, name, yieldCurve, output_type, compounding)


class FixedRateBond(mx.core_FixedRateCMBondPositionCalc):
    def __init__(self, name: str, ir_pc: mx.core_ProcessValue,
                 notional=10000,
                 fixedRate=0.0,
                 couponTenor=mx.Period(3, mx.Months),
                 maturityTenor=mx.Period(3, mx.Years),
                 discountCurve=None):
        if discountCurve is None:
            raise Exception('discount curve is required')

        self._ir_pc = ir_pc
        self._notional = notional
        self._fixedRate = fixedRate
        self._couponTenor = couponTenor
        self._maturityTenor = maturityTenor
        self._discountCurve = discountCurve

        mx.core_FixedRateCMBondPositionCalc.__init__(self, name, ir_pc, notional, fixedRate, couponTenor, maturityTenor, discountCurve)



class Returns(mx.core_ReturnWrapperCalc):
    def __init__(self, name: str, pc: mx.core_ProcessValue, return_type='return'):
        self._pc = pc
        self._return_type = return_type

        mx.core_ReturnWrapperCalc.__init__(self, name, pc, return_type)


class Shift(mx.core_ShiftWrapperCalc):
    def __init__(self, name: str, pc: mx.core_ProcessValue, 
                 shift: int, fill_value=0.0):
        self._pc = pc
        self._shift = shift
        self._fill_value = fill_value

        mx.core_ShiftWrapperCalc.__init__(self, name, pc, shift, fill_value)


class ConstantValue(mx.core_ConstantValueCalc):
    def __init__(self, name: str, v: float):
        self._v = v
        mx.core_ConstantValueCalc.__init__(self, name, v)


class ConstantArray(mx.core_ConstantArrayCalc):
    def __init__(self, name: str, arr: List[float]):
        self._arr = arr
        mx.core_ConstantArrayCalc.__init__(self, name, arr)


class LinearOper(mx.core_LinearOperWrapperCalc):
    def __init__(self, name: str, pc: mx.core_ProcessValue, multiple=1.0, spread=0.0):
        self._pc = pc
        self._multiple = multiple
        self._spread = spread
        mx.core_LinearOperWrapperCalc.__init__(self, name, pc, multiple, spread)


class UnaryFunction(mx.core_UnaryFunctionWrapperCalc):
    def __init__(self, name: str, pc: mx.core_ProcessValue, func_type: str):
        self._pc = pc
        self._func_type = func_type
        mx.core_UnaryFunctionWrapperCalc.__init__(self, name, pc, func_type)


class BinaryFunction(mx.core_BinaryFunctionWrapperCalc):
    def __init__(self, name: str, pc1: mx.core_ProcessValue, pc2: mx.core_ProcessValue, func_type: str):
        self._pc1 = pc1
        self._pc2 = pc2
        self._func_type = func_type
        mx.core_BinaryFunctionWrapperCalc.__init__(self, name, pc1, pc2, func_type)


class MultaryFunction(mx.core_MultaryFunctionWrapperCalc):
    def __init__(self, name: str, pc_list: List[mx.core_ProcessValue], func_type: str):
        self._pc_list = pc_list
        self._func_type = func_type
        mx.core_MultaryFunctionWrapperCalc.__init__(self, name, pc_list, func_type)


class Overwrite(mx.core_OverwriteWrapperCalc):
    def __init__(self, name: str, pc: mx.core_ProcessValue, start_pos: int, arr: List[float]):
        self._pc = pc
        self._arr = arr
        mx.core_OverwriteWrapperCalc.__init__(self, name, pc, start_pos, arr)


class Fund(mx.core_FundWrapperCalc):
    def __init__(self, name: str, weights: float, pc_list: List[mx.core_ProcessValue]):
        self._weights = weights
        self._pc_list = pc_list
        mx.core_FundWrapperCalc.__init__(self, name, weights, pc_list)

# model
class SpotRate(mx.core_SpotRateCalc):
    def __init__(self, name: str, ir_pc: mx.core_ProcessValue, 
                 maturityTenor: mx.Period, compounding=mx.Compounded):
        self._ir_pc = ir_pc
        self._maturityTenor = maturityTenor
        self._compounding = utils.toCompounding(compounding)
        mx.core_SpotRateCalc.__init__(self, name, ir_pc, maturityTenor, compounding)


class ForwardRate(mx.core_ForwardRateCalc):
    def __init__(self, name: str, ir_pc: mx.core_ProcessValue, 
                 startTenor: mx.Period, maturityTenor: mx.Period, compounding=mx.Compounded):
        self._ir_pc = ir_pc
        self._startTenor = startTenor
        self._maturityTenor = maturityTenor
        self._compounding = utils.toCompounding(compounding)
        mx.core_ForwardRateCalc.__init__(self, name, ir_pc, startTenor, maturityTenor, compounding)


class DiscountFactor(mx.core_DiscountFactorCalc):
    def __init__(self, name: str, ir_pc: mx.core_ProcessValue):
        self._ir_pc = ir_pc
        mx.core_DiscountFactorCalc.__init__(self, name, ir_pc)


class DiscountBond(mx.core_DiscountBondCalc):
    def __init__(self, name: str, ir_pc: mx.core_ProcessValue, maturityTenor: mx.Period):
        self._ir_pc = ir_pc
        self._maturityTenor = maturityTenor
        mx.core_DiscountBondCalc.__init__(self, name, ir_pc, maturityTenor)


# Bond Price Dynamics
class DiscountBondReturn(mx.core_DiscountBondReturnCalc):
    def __init__(self, name: str, ir_pc: mx.core_ProcessValue, 
                 maturityTenor: mx.Period, isConstantMaturity=True):
        self._ir_pc = ir_pc
        self._maturityTenor = maturityTenor
        self._isConstantMaturity = isConstantMaturity
        
        mx.core_DiscountBondReturnCalc.__init__(self, name, ir_pc, maturityTenor, isConstantMaturity)


class Libor(mx.core_LiborCalc):
    def __init__(self, name: str, ir_pc: mx.core_ProcessValue, iborIndex: mx.core_IborIndex, fixing=None):
        self._ir_pc = ir_pc
        self._iborIndex = iborIndex
        self._fixing = fixing

        fixing_conv = mx.nullDouble() if fixing is None else fixing

        mx.core_LiborCalc.__init__(self, name, ir_pc, iborIndex, fixing_conv)


class SwapRate(mx.core_SwapRateCalc):
    def __init__(self, name: str, ir_pc: mx.core_ProcessValue, swapIndex: mx.core_SwapIndex, fixing=None):
        self._ir_pc = ir_pc
        self._swapIndex = swapIndex
        self._fixing = fixing

        fixing_conv = mx.nullDouble() if fixing is None else fixing

        mx.core_SwapRateCalc.__init__(self, name, ir_pc, swapIndex, fixing_conv)


# math functions ---------------------

def min(pv_list: List[mx.core_ProcessValue], name=None):
    if name is None:
        name = '_'.join([pv.name() for pv in pv_list]) + 'min'
    return mx.core_MultaryFunctionWrapperCalc(name, pv_list, 'min')


def max(pv_list: List[mx.core_ProcessValue], name=None):
    if name is None:
        name = '_'.join([pv.name() for pv in pv_list]) + 'max'
    return mx.core_MultaryFunctionWrapperCalc(name, pv_list, 'max')



