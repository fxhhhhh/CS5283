# automatically generated by the FlatBuffers1 compiler, do not modify

# namespace: Grocery

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class veggie1(object):
    __slots__ = ['_tab']

    @classmethod
    def SizeOf(cls):
        return 20

    # veggie1
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # veggie1
    def Cucumber(self): return self._tab.Get(flatbuffers.number_types.Float32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(0))
    # veggie1
    def Tomato(self): return self._tab.Get(flatbuffers.number_types.Float32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(4))
    # veggie1
    def Potato(self): return self._tab.Get(flatbuffers.number_types.Float32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(8))
    # veggie1
    def Carrot(self): return self._tab.Get(flatbuffers.number_types.Float32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(12))
    # veggie1
    def Eggplant(self): return self._tab.Get(flatbuffers.number_types.Float32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(16))

def Createveggie1(builder, cucumber, tomato, potato, carrot, eggplant):
    builder.Prep(4, 20)
    builder.PrependFloat32(eggplant)
    builder.PrependFloat32(carrot)
    builder.PrependFloat32(potato)
    builder.PrependFloat32(tomato)
    builder.PrependFloat32(cucumber)
    return builder.Offset()