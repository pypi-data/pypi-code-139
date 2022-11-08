from typing import List
import mxdevtool as mx
import mxdevtool.marketconvension as mx_mc
import mxdevtool.utils as utils


# condition -----------------------------
class ANDCondition(mx.core_ANDConditionMC):
    def __init__(self, conditions):
        self._conditions = conditions
        mx.core_ANDConditionMC.__init__(self, conditions)


class ORCondition(mx.core_ORConditionMC):
    def __init__(self, conditions):
        self._conditions = conditions
        mx.core_ORConditionMC.__init__(self, conditions)


class XORCondition(mx.core_XORConditionMC):
    def __init__(self, condition1, condition2):
        self._condition1 = condition1
        self._condition2 = condition2
        mx.core_XORConditionMC.__init__(self, condition1, condition2)


class NOTCondition(mx.core_NOTConditionMC):
    def __init__(self, condition):
        self._condition = condition
        mx.core_NOTConditionMC.__init__(self, condition)


class RangeCondition(mx.core_RangeConditionMC):
    def __init__(self, po, a, b):
        self._po = po
        self._a = a
        self._b = b
        mx.core_RangeConditionMC.__init__(self, po, a, b)


class ANDDatesCondition(mx.core_DatesConditionMC):
    def __init__(self, po, dates):
        self._po = po
        self._dates = dates
        mx.core_DatesConditionMC.__init__(self, po, dates, 'and')


class ORDatesCondition(mx.core_DatesConditionMC):
    def __init__(self, po, dates):
        self._po = po
        self._dates = dates
        mx.core_DatesConditionMC.__init__(self, po, dates, 'or')


# class ANDBetweenDatesCondition(mx.core_BetweenDatesConditionMC):
#     def __init__(self, po, dates):
#         self._po = po
#         self._dates = dates
#         mx.core_BetweenDatesConditionMC.__init__(self, po, dates, 'and')


# class ORBetweenDatesCondition(mx.core_BetweenDatesConditionMC):
#     def __init__(self, po, dates):
#         self._po = po
#         self._dates = dates
#         mx.core_BetweenDatesConditionMC.__init__(self, po, dates, 'or')


class RelationalCondition(mx.core_RelationalConditionMC):
    def __init__(self, po1, operand, po2):
        self._po1 = po1
        self._operand = operand
        self._po2 = po2
        mx.core_RelationalConditionMC.__init__(self, po1, operand, po2)



# operators -----------------------------
class PlusPayoff(mx.core_PlusPayoffMC):
    def __init__(self, po):
        self._po = po
        mx.core_PlusPayoffMC.__init__(self, po)


class MinusPayoff(mx.core_MinusPayoffMC):
    def __init__(self, po):
        self._po = po
        mx.core_MinusPayoffMC.__init__(self, po)


class AdditionPayoff(mx.core_AdditionPayoffMC):
    def __init__(self, po1, po2):
        self._po1 = po1
        self._po2 = po2
        mx.core_AdditionPayoffMC.__init__(self, po1, po2)


class SubtractionPayoff(mx.core_SubtractionPayoffMC):
    def __init__(self, po1, po2):
        self._po1 = po1
        self._po2 = po2
        mx.core_SubtractionPayoffMC.__init__(self, po1, po2)


class MultiplicationPayoff(mx.core_MultiplicationPayoffMC):
    def __init__(self, po1, po2):
        self._po1 = po1
        self._po2 = po2
        mx.core_MultiplicationPayoffMC.__init__(self, po1, po2)


class DivisionPayoff(mx.core_DivisionPayoffMC):
    def __init__(self, po1, po2):
        self._po1 = po1
        self._po2 = po2
        mx.core_DivisionPayoffMC.__init__(self, po1, po2)


class IdentityPayoff(mx.core_IdentityPayoffMC):
    def __init__(self, po):
        self._po = po
        mx.core_IdentityPayoffMC.__init__(self, po)


class LinearPayoff(mx.core_LinearPayoffMC):
    def __init__(self, po, multiple, spread):
        self._po = po
        self._multiple = multiple
        self._spread = spread
        mx.core_LinearPayoffMC.__init__(self, po, multiple, spread)


class ConstantPayoff(mx.core_ConstantPayoffMC):
    def __init__(self, v):
        self._v = v
        mx.core_ConstantPayoffMC.__init__(self, v)


class ConditionPayoff(mx.core_ConditionPayoffMC):
    def __init__(self, condi, po_true, po_false):
        self._condi = condi
        self._po_true = po_true
        self._po_false = po_false
        mx.core_ConditionPayoffMC.__init__(self, condi, po_true, po_false)


class IndexPayoff(mx.core_IndexPayoffMC):
    def __init__(self, name):
        self._name = name
        mx.core_IndexPayoffMC.__init__(self, name)

    def index(self) -> mx.Index:
        return self._index()

    # parsing ex) krwirs10y
    # def as_iborIndex(self) -> mx_mc.IborIndex:
    #     mx_mc.get_iborIndex(self._name)

    def as_swapIndex(self) -> mx_mc.SwapIndex:
        mx_mc.get_swapIndex(self._name)

    @staticmethod
    def fromDict(d: dict):
        return utils.parseClassFromDict(d, globals())

    def toDict(self):
        return utils.serializeToDict(self)


class MinPayoff(mx.core_BinaryFunctionPayoffMC):
    def __init__(self, po1, po2):
        self._po1 = po1
        self._po2 = po2
        mx.core_BinaryFunctionPayoffMC.__init__(self, po1, po2, 'min')


class MaxPayoff(mx.core_BinaryFunctionPayoffMC):
    def __init__(self, po1, po2):
        self._po1 = po1
        self._po2 = po2
        mx.core_BinaryFunctionPayoffMC.__init__(self, po1, po2, 'max')



class MinimumBetweenDatesPayoff(mx.core_BetweenDatesFunctionPayoffMC):
    def __init__(self, po, startDate, endDate):
        self._po = po
        self._startDate = startDate
        self._endDate = endDate
        mx.core_BetweenDatesFunctionPayoffMC.__init__(self, po, startDate, endDate, 'minimum')


class MaximumBetweenDatesPayoff(mx.core_BetweenDatesFunctionPayoffMC):
    def __init__(self, po, startDate, endDate):
        self._po = po
        self._startDate = startDate
        self._endDate = endDate
        mx.core_BetweenDatesFunctionPayoffMC.__init__(self, po, startDate, endDate, 'maximum')


class AverageBetweenDatesPayoff(mx.core_BetweenDatesFunctionPayoffMC):
    def __init__(self, po, startDate, endDate):
        self._po = po
        self._startDate = startDate
        self._endDate = endDate
        mx.core_BetweenDatesFunctionPayoffMC.__init__(self, po, startDate, endDate, 'average')


class MinimumDatesPayoff(mx.core_DatesFunctionPayoffMC):
    def __init__(self, po, dates):
        self._po = po
        self._dates = dates
        mx.core_DatesFunctionPayoffMC.__init__(self, po, dates, 'minimum')


class MaximumDatesPayoff(mx.core_DatesFunctionPayoffMC):
    def __init__(self, po, dates):
        self._po = po
        self._dates = dates
        mx.core_DatesFunctionPayoffMC.__init__(self, po, dates, 'maximum')


class AverageDatesPayoff(mx.core_DatesFunctionPayoffMC):
    def __init__(self, po, dates):
        self._po = po
        self._dates = dates
        mx.core_DatesFunctionPayoffMC.__init__(self, po, dates, 'average')


# coupons -----------------------------

class RateAccrualCouponMC(mx.core_RateAccrualCouponMC):
    def __init__(self, paymentDate, nominal, payoffMC,
                 accrualStartDate, accrualEndDate, calendar, dayCounter, accruedAmount):

        args = utils.set_init_self_args(self, paymentDate, nominal, payoffMC,
                accrualStartDate, accrualEndDate, calendar, dayCounter, accruedAmount)

        super().__init__(*args)

    @staticmethod
    def makeLeg(schedule, payoffMC, notional=10000,
                calendar=mx.SouthKorea(), dayCounter=mx.Actual365Fixed()):

        cpns = []

        for i, d in enumerate(schedule):
            if i == 0: continue

            cpn = RateAccrualCouponMC(
                schedule[i],
                notional,
                payoffMC,
                schedule[i-1],
                schedule[i],
                calendar,
                dayCounter)

            cpns.append(cpn)

        return cpns


class FloatingRateCouponMC(mx.core_FloatingRateCouponMC):
    def __init__(self, paymentDate, nominal,
                accrualStartDate, accrualEndDate, fixingDays, indexPayoffMC, calendar,
                dayCounter, gearing=1.0, spread=0.0):

        args = utils.set_init_self_args(self, paymentDate, nominal,
                    accrualStartDate, accrualEndDate, fixingDays, indexPayoffMC, calendar,
                    dayCounter, gearing, spread)

        super().__init__(*args)

    @staticmethod
    def makeLeg(schedule, indexPayoffMC, notional=10000, fixingDays=1,
                calendar=mx.SouthKorea(), dayCounter=mx.Actual365Fixed(), gearing=1.0, spread=0.0):

        cpns = []

        for i, d in enumerate(schedule):
            if i == 0: continue

            cpn = FloatingRateCouponMC(
                schedule[i],
                notional,
                schedule[i-1],
                schedule[i],
                fixingDays,
                indexPayoffMC,
                calendar,
                dayCounter,
                gearing,
                spread)

            cpns.append(cpn)

        return cpns



# class VanillaCouponMC(mx.core_VanillaCouponMC):
#     pass


class StructuredLegExerciseOption(mx.core_StructuredLegExerciseOption):
    def __init__(self, dates, settlementDates, amounts):
        args = utils.set_init_self_args(self, dates, settlementDates, amounts)

        super().__init__(*args)


class VanillaLegInfo(mx.core_VanillaLegInfo):
    def __init__(self, coupons, currency=mx.currencyParse('krw')):
        args = utils.set_init_self_args(self, coupons, currency)

        super().__init__(*args)


class StructuredLegInfo(mx.core_StructuredLegInfo):
    def __init__(self, coupons, currency=mx.currencyParse('krw'), option=None):
        args = utils.set_init_self_args(self, coupons, currency, option)

        super().__init__(*args)


class StructuredSwap(mx.core_StructuredSwap):
    def __init__(self, payLegInfo, recLegInfo):
        self._payLegInfo = payLegInfo
        self._recLegInfo = recLegInfo

        mx.core_StructuredSwap.__init__(self, payLegInfo, recLegInfo)

    def payCpns(self) -> List[mx.core_CouponMC]:
        return self._payLegInfo._coupons

    def recCpns(self) -> List[mx.core_CouponMC]:
        return self._recLegInfo._coupons

    def setPricingParams_Scen(self, pay_discount: str, rec_discount: str, reg_index_names: str, scen_filename: str):
        self._setPricingParams_Scen(pay_discount, rec_discount, reg_index_names, scen_filename)
        return self
