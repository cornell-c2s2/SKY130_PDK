import gdb
import re
import sys
sys.path.insert(0, '/grid/common/pkgs/gcc/latest/share/gcc-9.3.0/python/')
from libstdcxx.v6.printers import StdVectorPrinter



MemTypeSwitch = {
    "Cadence::oaDebugCDS::cIndex": "index",
    "Cadence::oaDebugCDS::cStringRef": "stringRef",
    "Cadence::oaDebugCDS::cName": "nameRef",
    "Cadence::oaDebugCDS::cBox": "box",
    "Cadence::oaDebugCDS::cDist": "dist",
    "Cadence::oaDebugCDS::cPointArray": "pointArray",
    "Cadence::oaDebugCDS::cByte": "byte",
    "Cadence::oaDebugCDS::cPoint": "point",
    "Cadence::oaDebugCDS::cDouble": "doubleVal",
    "Cadence::oaDebugCDS::cUInt4": "uint4Val",
    "Cadence::oaDebugCDS::cString": "string",
    "Cadence::oaDebugCDS::cFloat": "floatVal",
    "Cadence::oaDebugCDS::cUInt8": "uint8Val",
    "Cadence::oaDebugCDS::cByteArray": "byteArray",
    "Cadence::oaDebugCDS::cObjRef": "objRef",
    "Cadence::oaDebugCDS::cBoolean": "boolVal"
}

MemValueSwitch = {
    "4294967295": "oacNullIndex",
    "18446744073709551615": "oacNullLongIndex",
    "-2147483648": "INT_MIN",
    "2147483647": "INT_MAX"
}



class MemDataVectorPrinter(StdVectorPrinter):
    """Derive from StdVectorPrinter to keep the iterator functionality but customize the output.

    This also avoids the memData print from being overridden if a user is auto-loading the GCC libstc++ pretty-printers."""
    class _iterator(StdVectorPrinter._iterator):
        def __next__(self):
            s = super().__next__()
            return ("\n    " + s[0], s[1])



class ObjectPvtPrinter(object):
    """Print an ObjectPvt

    Prints the type or the subType if applicable, not both.
    The memData is counted as it's "children" so that it can be iterated over."""
    def __init__(self, val):
        self.val = val

    def to_string(self):
        type = str(self.val["subTypeTag"]) if str(self.val["subTypeTag"]) else str(self.val["typeTag"])
        output = "\n  type = " + type + \
                 "\n  db = " + str(self.val["database"]) + \
                 "\n  dtIndex = " + str(self.val["dtIndex"]) + \
                 "\n  index = " + str(self.val["index"]) + \
                 "\n  flags = " + str(self.val["flags"]) + \
                 "\n  memberData"
        return output

    def display_hint(self):
        return 'ObjectPvt'

    def children(self):
        return MemDataVectorPrinter("MemDataVector", self.val["memberData"]).children();



class MemDataPrinter(object):
    """Print a MemData

    Displays an error if the MemType doesn't correspond to any of the attributes that a MemData can hold."""
    def __init__(self, val):
        self.val = val

    def to_string(self):
        memType = MemTypeSwitch.get(str(self.val["type"]))
        if memType:
            
            memValue = str(self.val[memType])
            output = str(self.val["tag"]) + " " + \
                     (MemValueSwitch.get(memValue) if MemValueSwitch.get(memValue) else memValue)
        else:
            output = "Unsupported memType: " + str(self.val["type"])

        return output

    def display_hint(self):
        return 'MemData'



class ObjRefPrinter(object):
    """Print an ObjRef"""
    def __init__(self, val):
        self.val = val

    def to_string(self):
        rawDtIndex = str(self.val["dtIndex"])
        rawObjIndex = str(self.val["index"])
        return "{dtIndex = " + \
               (MemValueSwitch.get(rawDtIndex) if MemValueSwitch.get(rawDtIndex) else rawDtIndex) + \
               ", index = " + \
               (MemValueSwitch.get(rawObjIndex) if MemValueSwitch.get(rawObjIndex) else rawObjIndex) + \
               ", domain = " + str(self.val["domain"]) + "}"

    def display_hint(self):
        return 'ObjRef'



class StringRefPrinter(object):
    """Print an StringRef"""
    def __init__(self, val):
        self.val = val

    def to_string(self):
        rawIndex = str(self.val["index"])
        index = MemValueSwitch.get(rawIndex) if MemValueSwitch.get(rawIndex) else rawIndex

        output = "{stringRef = " + index

        if index != "oacNullLongIndex":
           output += ', value = "' + str(self.val["value"]) + '"'

        output += '}'

        return output

    def display_hint(self):
        return 'StringRef'



class oaBoxPrinter(object):
    """Print an oaBox"""

    def __init__(self, val):
        self.val = val

    def to_string(self):
        return str(self.val["lowerLeftVal"]) + " " + str(self.val["upperRightVal"])

    def display_hint(self):
        return 'oaBox'



class oaPointPrinter(object):
    """Print an oaPoint"""

    def __init__(self, val):
        self.val = val

    def to_string(self):
        return "(" + str(self.val["xVal"]) + ":" + str(self.val["yVal"]) + ")"

    def display_hint(self):
        return 'oaPoint'



class oaArrayPrinter(object):
    """Print an oaArray"""

    def __init__(self, val):
        self.val = val
        self.elements = self.val['elements']
        self.length = int(self.val["numElements"])

    def to_string(self):
        return str(self.length) + " elements"
    
    def next_element(self):
        for i in range(self.length):
            yield str(i), (self.elements + i).dereference()

    def children(self):
        return self.next_element()

    def display_hint(self):
        return 'oaArray'



class oaPointArrayPrinter(oaArrayPrinter):
    """Print an oaPointArray"""

    def to_string(self):
        return str(self.length) + " elements"

    def display_hint(self):
        return 'oaPointArray'



class oaByteArrayPrinter(oaArrayPrinter):
    """Print an oaByteArray"""

    def to_string(self):
        return str(self.length) + " elements"

    def display_hint(self):
        return 'oaByteArray'



class oaStringPrinter(object):
    """Print an oaString"""

    def __init__(self, val):
        self.val = val

    def to_string(self):
        return self.val["data"].string(encoding='utf-8', errors='ignore',length=self.val["size"])

    def display_hint(self):
        return 'oaString'



def build_pretty_printer():
    """Register the pretty printer as a global printer. If it already exists, overwrite it."""

    pp = gdb.printing.RegexpCollectionPrettyPrinter("oaDebugCDS")
    pp.add_printer('ObjectPvt', '^Cadence::oaDebugCDS::ObjectPvt$', ObjectPvtPrinter)
    pp.add_printer('MemData', '^Cadence::oaDebugCDS::MemData$', MemDataPrinter)
    pp.add_printer('ObjRef', '^Cadence::oaDebugCDS::ObjRef$', ObjRefPrinter)
    pp.add_printer('StringRef', '^Cadence::oaDebugCDS::StringRef', StringRefPrinter)
    pp.add_printer('oaBox', '^OpenAccess_4::oaBox$', oaBoxPrinter)
    pp.add_printer('oaArray', '^OpenAccess_4::oaArray<.*>$', oaArrayPrinter)
    pp.add_printer('oaPoint', '^OpenAccess_4::oaPoint$', oaPointPrinter)
    pp.add_printer('oaPointArray', '^OpenAccess_4::oaPointArray$', oaPointArrayPrinter)
    pp.add_printer('oaByteArray', '^OpenAccess_4::oaByteArray$', oaByteArrayPrinter)
    pp.add_printer('oaString', '^OpenAccess_4::oaString$', oaStringPrinter)
    gdb.printing.register_pretty_printer(None, pp, True)

build_pretty_printer()
