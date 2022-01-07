from decimal import Decimal
from typing import Iterable, Optional, Type, TypeVar
from stock_indicators._cslib import CsIndicator
from stock_indicators._cstypes import List as CsList
from stock_indicators._cstypes import Decimal as CsDecimal
from stock_indicators._cstypes import to_pydecimal
from stock_indicators.indicators.common.results import IndicatorResults, ResultBase
from stock_indicators.indicators.common.quote import Quote

def get_chandelier(quotes: Iterable[Quote], lookback_periods: int = 22, multiplier: float = 3):
    results = CsIndicator.GetChandelier[Quote](CsList(Quote, quotes), lookback_periods, multiplier)
    return ChandelierResults(results, ChandelierResult)

class ChandelierResult(ResultBase):
    """
    A wrapper class for a single unit of Chandelier Exit results.
    """

    @property
    def chandelier_exit(self) -> Optional[Decimal]:
        return to_pydecimal(self._csdata.ChandelierExit)

    @chandelier_exit.setter
    def chandelier_exit(self, value):
        self._csdata.ChandelierExit = CsDecimal(value)
        
T = TypeVar("T", bound=ChandelierResult)
class ChandelierResults(IndicatorResults[T]):
    """
    A wrapper class for the list of Chandelier Exit results.
    It is exactly same with built-in `list` except for that it provides
    some useful helper methods written in C# implementation.
    """

    def __init__(self, data: Iterable, wrapper_class: Type[T]):
        super().__init__(data, wrapper_class)

    @IndicatorResults._verify_data
    def remove_warmup_periods(self, remove_periods: Optional[int] = None):
        if remove_periods is not None:
            return super().remove_warmup_periods(remove_periods)

        removed_results = CsIndicator.RemoveWarmupPeriods(CsList(type(self._csdata[0]), self._csdata))

        return self.__class__(removed_results, self._wrapper_class)