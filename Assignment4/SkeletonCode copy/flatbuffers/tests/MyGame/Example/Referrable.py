# automatically generated by the FlatBuffers compiler, do not modify

# namespace: Example

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class Referrable(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Referrable()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsReferrable(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    @classmethod
    def ReferrableBufferHasIdentifier(cls, buf, offset, size_prefixed=False):
        return flatbuffers.util.BufferHasIdentifier(buf, offset, b"\x4D\x4F\x4E\x53", size_prefixed=size_prefixed)

    # Referrable
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Referrable
    def Id(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

def ReferrableStart(builder): builder.StartObject(1)
def Start(builder):
    return ReferrableStart(builder)
def ReferrableAddId(builder, id): builder.PrependUint64Slot(0, id, 0)
def AddId(builder, id):
    return ReferrableAddId(builder, id)
def ReferrableEnd(builder): return builder.EndObject()
def End(builder):
    return ReferrableEnd(builder)

class ReferrableT(object):

    # ReferrableT
    def __init__(self):
        self.id = 0  # type: int

    @classmethod
    def InitFromBuf(cls, buf, pos):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, 0)
        referrable = Referrable()
        referrable.Init(buf, pos+n)
        return cls.InitFromObj(referrable)

    @classmethod
    def InitFromObj(cls, referrable):
        x = ReferrableT()
        x._UnPack(referrable)
        return x

    # ReferrableT
    def _UnPack(self, referrable):
        if referrable is None:
            return
        self.id = referrable.Id()

    # ReferrableT
    def Pack(self, builder):
        ReferrableStart(builder)
        ReferrableAddId(builder, self.id)
        referrable = ReferrableEnd(builder)
        return referrable
