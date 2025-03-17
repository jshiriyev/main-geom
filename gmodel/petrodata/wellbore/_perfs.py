from dataclasses import dataclass, fields

from datetime import date

@dataclass
class Perf:
    """It is a dictionary for a perforation in a well."""
    date        : date = None

    layer       : str = None
    interval    : str = None
    guntype     : str = None

    @staticmethod
    def fields() -> list:
        """Returns the list of field names in the Perf dataclass."""
        return [f.name for f in fields(Perf)]

    @staticmethod
    def interval_to_list(interval:str,delimiter:str="-",decsep:str=".") -> list:
        """Converts a string interval into a list of floats.

        Parameters:
        ----------
        interval  : The interval string (e.g., "1005-1092").
        delimiter : The delimiter separating depths in the interval. Defaults to "-".
        decsep    : The decimal separator in the depth of the interval. Defaults to ".".
        
        Returns:
        -------
        List: A list containing one or two float values. If only one value
            is provided, the second element will be None.
        """
        try:
            depths = [float(depth.replace(decsep,'.')) for depth in interval.split(delimiter)]
            if len(depths)==1:
                depths.append(None)
            elif len(depths) > 2:
                raise ValueError(f"Unexpected format: '{interval}'. Expected format 'depth_1{delimiter}depth_2'.")
            return depths
        except ValueError as e:
            raise ValueError(f"Invalid interval format: {interval}. Error: {e}")

class Perfs():
    """A collection of 'Perf' objects with list-like access."""

    def __init__(self,*args:Perf):

        self._list = list(args)

    def __getitem__(self,key):
        """Retrieves a 'Perf' object by index."""
        return self._list[key]

    def __iter__(self) -> Iterator[Perf]:
        """Allows iteration over the 'Perf' objects."""
        return iter(self._list)

    def __len__(self) -> int:
        """Returns the number of 'Perf' objects."""
        return len(self._list)

    def append(self,perf:Perf) -> None:
        """Adds a new 'Perf' object to the collection."""
        if not isinstance(perf, Perf):
            raise TypeError("Only Perf objects can be added.")
        self._list.append(perf)

    def __getattr__(self,key):
        """Forwards attribute access to the internal list object."""
        return getattr(self._list,key)
    