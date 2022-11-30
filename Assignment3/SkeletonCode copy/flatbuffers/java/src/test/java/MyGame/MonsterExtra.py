# automatically generated by the FlatBuffers compiler, do not modify

# namespace: MyGame

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class MonsterExtra(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = MonsterExtra()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsMonsterExtra(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    @classmethod
    def MonsterExtraBufferHasIdentifier(cls, buf, offset, size_prefixed=False):
        return flatbuffers.util.BufferHasIdentifier(buf, offset, b"\x4D\x4F\x4E\x45", size_prefixed=size_prefixed)

    # MonsterExtra
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # MonsterExtra
    def D0(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float64Flags, o + self._tab.Pos)
        return float('nan')

    # MonsterExtra
    def D1(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float64Flags, o + self._tab.Pos)
        return float('nan')

    # MonsterExtra
    def D2(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float64Flags, o + self._tab.Pos)
        return float('inf')

    # MonsterExtra
    def D3(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float64Flags, o + self._tab.Pos)
        return float('-inf')

    # MonsterExtra
    def F0(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return float('nan')

    # MonsterExtra
    def F1(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return float('nan')

    # MonsterExtra
    def F2(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return float('inf')

    # MonsterExtra
    def F3(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return float('-inf')

    # MonsterExtra
    def Dvec(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(20))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Float64Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 8))
        return 0

    # MonsterExtra
    def DvecAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(20))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Float64Flags, o)
        return 0

    # MonsterExtra
    def DvecLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(20))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # MonsterExtra
    def DvecIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(20))
        return o == 0

    # MonsterExtra
    def Fvec(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(22))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Float32Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return 0

    # MonsterExtra
    def FvecAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(22))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Float32Flags, o)
        return 0

    # MonsterExtra
    def FvecLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(22))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # MonsterExtra
    def FvecIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(22))
        return o == 0

def MonsterExtraStart(builder): builder.StartObject(11)
def Start(builder):
    return MonsterExtraStart(builder)
def MonsterExtraAddD0(builder, d0): builder.PrependFloat64Slot(0, d0, float('nan'))
def AddD0(builder, d0):
    return MonsterExtraAddD0(builder, d0)
def MonsterExtraAddD1(builder, d1): builder.PrependFloat64Slot(1, d1, float('nan'))
def AddD1(builder, d1):
    return MonsterExtraAddD1(builder, d1)
def MonsterExtraAddD2(builder, d2): builder.PrependFloat64Slot(2, d2, float('inf'))
def AddD2(builder, d2):
    return MonsterExtraAddD2(builder, d2)
def MonsterExtraAddD3(builder, d3): builder.PrependFloat64Slot(3, d3, float('-inf'))
def AddD3(builder, d3):
    return MonsterExtraAddD3(builder, d3)
def MonsterExtraAddF0(builder, f0): builder.PrependFloat32Slot(4, f0, float('nan'))
def AddF0(builder, f0):
    return MonsterExtraAddF0(builder, f0)
def MonsterExtraAddF1(builder, f1): builder.PrependFloat32Slot(5, f1, float('nan'))
def AddF1(builder, f1):
    return MonsterExtraAddF1(builder, f1)
def MonsterExtraAddF2(builder, f2): builder.PrependFloat32Slot(6, f2, float('inf'))
def AddF2(builder, f2):
    return MonsterExtraAddF2(builder, f2)
def MonsterExtraAddF3(builder, f3): builder.PrependFloat32Slot(7, f3, float('-inf'))
def AddF3(builder, f3):
    return MonsterExtraAddF3(builder, f3)
def MonsterExtraAddDvec(builder, dvec): builder.PrependUOffsetTRelativeSlot(8, flatbuffers.number_types.UOffsetTFlags.py_type(dvec), 0)
def AddDvec(builder, dvec):
    return MonsterExtraAddDvec(builder, dvec)
def MonsterExtraStartDvecVector(builder, numElems): return builder.StartVector(8, numElems, 8)
def StartDvecVector(builder, numElems):
    return MonsterExtraStartDvecVector(builder, numElems)
def MonsterExtraAddFvec(builder, fvec): builder.PrependUOffsetTRelativeSlot(9, flatbuffers.number_types.UOffsetTFlags.py_type(fvec), 0)
def AddFvec(builder, fvec):
    return MonsterExtraAddFvec(builder, fvec)
def MonsterExtraStartFvecVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def StartFvecVector(builder, numElems):
    return MonsterExtraStartFvecVector(builder, numElems)
def MonsterExtraEnd(builder): return builder.EndObject()
def End(builder):
    return MonsterExtraEnd(builder)
try:
    from typing import List
except:
    pass

class MonsterExtraT(object):

    # MonsterExtraT
    def __init__(self):
        self.d0 = float('nan')  # type: float
        self.d1 = float('nan')  # type: float
        self.d2 = float('inf')  # type: float
        self.d3 = float('-inf')  # type: float
        self.f0 = float('nan')  # type: float
        self.f1 = float('nan')  # type: float
        self.f2 = float('inf')  # type: float
        self.f3 = float('-inf')  # type: float
        self.dvec = None  # type: List[float]
        self.fvec = None  # type: List[float]

    @classmethod
    def InitFromBuf(cls, buf, pos):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, 0)
        monsterExtra = MonsterExtra()
        monsterExtra.Init(buf, pos+n)
        return cls.InitFromObj(monsterExtra)

    @classmethod
    def InitFromObj(cls, monsterExtra):
        x = MonsterExtraT()
        x._UnPack(monsterExtra)
        return x

    # MonsterExtraT
    def _UnPack(self, monsterExtra):
        if monsterExtra is None:
            return
        self.d0 = monsterExtra.D0()
        self.d1 = monsterExtra.D1()
        self.d2 = monsterExtra.D2()
        self.d3 = monsterExtra.D3()
        self.f0 = monsterExtra.F0()
        self.f1 = monsterExtra.F1()
        self.f2 = monsterExtra.F2()
        self.f3 = monsterExtra.F3()
        if not monsterExtra.DvecIsNone():
            if np is None:
                self.dvec = []
                for i in range(monsterExtra.DvecLength()):
                    self.dvec.append(monsterExtra.Dvec(i))
            else:
                self.dvec = monsterExtra.DvecAsNumpy()
        if not monsterExtra.FvecIsNone():
            if np is None:
                self.fvec = []
                for i in range(monsterExtra.FvecLength()):
                    self.fvec.append(monsterExtra.Fvec(i))
            else:
                self.fvec = monsterExtra.FvecAsNumpy()

    # MonsterExtraT
    def Pack(self, builder):
        if self.dvec is not None:
            if np is not None and type(self.dvec) is np.ndarray:
                dvec = builder.CreateNumpyVector(self.dvec)
            else:
                MonsterExtraStartDvecVector(builder, len(self.dvec))
                for i in reversed(range(len(self.dvec))):
                    builder.PrependFloat64(self.dvec[i])
                dvec = builder.EndVector()
        if self.fvec is not None:
            if np is not None and type(self.fvec) is np.ndarray:
                fvec = builder.CreateNumpyVector(self.fvec)
            else:
                MonsterExtraStartFvecVector(builder, len(self.fvec))
                for i in reversed(range(len(self.fvec))):
                    builder.PrependFloat32(self.fvec[i])
                fvec = builder.EndVector()
        MonsterExtraStart(builder)
        MonsterExtraAddD0(builder, self.d0)
        MonsterExtraAddD1(builder, self.d1)
        MonsterExtraAddD2(builder, self.d2)
        MonsterExtraAddD3(builder, self.d3)
        MonsterExtraAddF0(builder, self.f0)
        MonsterExtraAddF1(builder, self.f1)
        MonsterExtraAddF2(builder, self.f2)
        MonsterExtraAddF3(builder, self.f3)
        if self.dvec is not None:
            MonsterExtraAddDvec(builder, dvec)
        if self.fvec is not None:
            MonsterExtraAddFvec(builder, fvec)
        monsterExtra = MonsterExtraEnd(builder)
        return monsterExtra
