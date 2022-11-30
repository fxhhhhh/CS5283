// automatically generated by the FlatBuffers compiler, do not modify

package NamespaceA;

import java.nio.*;
import java.lang.*;
import java.util.*;
import com.google.flatbuffers.*;

@SuppressWarnings("unused")
public final class TableInFirstNS extends Table {
  public static void ValidateVersion() { Constants.FLATBUFFERS_2_0_8(); }
  public static TableInFirstNS getRootAsTableInFirstNS(ByteBuffer _bb) { return getRootAsTableInFirstNS(_bb, new TableInFirstNS()); }
  public static TableInFirstNS getRootAsTableInFirstNS(ByteBuffer _bb, TableInFirstNS obj) { _bb.order(ByteOrder.LITTLE_ENDIAN); return (obj.__assign(_bb.getInt(_bb.position()) + _bb.position(), _bb)); }
  public void __init(int _i, ByteBuffer _bb) { __reset(_i, _bb); }
  public TableInFirstNS __assign(int _i, ByteBuffer _bb) { __init(_i, _bb); return this; }

  public NamespaceA.NamespaceB.TableInNestedNS fooTable() { return fooTable(new NamespaceA.NamespaceB.TableInNestedNS()); }
  public NamespaceA.NamespaceB.TableInNestedNS fooTable(NamespaceA.NamespaceB.TableInNestedNS obj) { int o = __offset(4); return o != 0 ? obj.__assign(__indirect(o + bb_pos), bb) : null; }
  public byte fooEnum() { int o = __offset(6); return o != 0 ? bb.get(o + bb_pos) : 0; }
  public boolean mutateFooEnum(byte foo_enum) { int o = __offset(6); if (o != 0) { bb.put(o + bb_pos, foo_enum); return true; } else { return false; } }
  public byte fooUnionType() { int o = __offset(8); return o != 0 ? bb.get(o + bb_pos) : 0; }
  public Table fooUnion(Table obj) { int o = __offset(10); return o != 0 ? __union(obj, o + bb_pos) : null; }
  public NamespaceA.NamespaceB.StructInNestedNS fooStruct() { return fooStruct(new NamespaceA.NamespaceB.StructInNestedNS()); }
  public NamespaceA.NamespaceB.StructInNestedNS fooStruct(NamespaceA.NamespaceB.StructInNestedNS obj) { int o = __offset(12); return o != 0 ? obj.__assign(o + bb_pos, bb) : null; }

  public static void startTableInFirstNS(FlatBufferBuilder builder) { builder.startTable(5); }
  public static void addFooTable(FlatBufferBuilder builder, int fooTableOffset) { builder.addOffset(0, fooTableOffset, 0); }
  public static void addFooEnum(FlatBufferBuilder builder, byte fooEnum) { builder.addByte(1, fooEnum, 0); }
  public static void addFooUnionType(FlatBufferBuilder builder, byte fooUnionType) { builder.addByte(2, fooUnionType, 0); }
  public static void addFooUnion(FlatBufferBuilder builder, int fooUnionOffset) { builder.addOffset(3, fooUnionOffset, 0); }
  public static void addFooStruct(FlatBufferBuilder builder, int fooStructOffset) { builder.addStruct(4, fooStructOffset, 0); }
  public static int endTableInFirstNS(FlatBufferBuilder builder) {
    int o = builder.endTable();
    return o;
  }

  public static final class Vector extends BaseVector {
    public Vector __assign(int _vector, int _element_size, ByteBuffer _bb) { __reset(_vector, _element_size, _bb); return this; }

    public TableInFirstNS get(int j) { return get(new TableInFirstNS(), j); }
    public TableInFirstNS get(TableInFirstNS obj, int j) {  return obj.__assign(__indirect(__element(j), bb), bb); }
  }
  public TableInFirstNST unpack() {
    TableInFirstNST _o = new TableInFirstNST();
    unpackTo(_o);
    return _o;
  }
  public void unpackTo(TableInFirstNST _o) {
    if (fooTable() != null) _o.setFooTable(fooTable().unpack());
    else _o.setFooTable(null);
    byte _oFooEnum = fooEnum();
    _o.setFooEnum(_oFooEnum);
    NamespaceA.NamespaceB.UnionInNestedNSUnion _oFooUnion = new NamespaceA.NamespaceB.UnionInNestedNSUnion();
    byte _oFooUnionType = fooUnionType();
    _oFooUnion.setType(_oFooUnionType);
    Table _oFooUnionValue;
    switch (_oFooUnionType) {
      case NamespaceA.NamespaceB.UnionInNestedNS.TableInNestedNS:
        _oFooUnionValue = fooUnion(new NamespaceA.NamespaceB.TableInNestedNS());
        _oFooUnion.setValue(_oFooUnionValue != null ? ((NamespaceA.NamespaceB.TableInNestedNS) _oFooUnionValue).unpack() : null);
        break;
      default: break;
    }
    _o.setFooUnion(_oFooUnion);
    if (fooStruct() != null) fooStruct().unpackTo(_o.getFooStruct());
    else _o.setFooStruct(null);
  }
  public static int pack(FlatBufferBuilder builder, TableInFirstNST _o) {
    if (_o == null) return 0;
    int _foo_table = _o.getFooTable() == null ? 0 : NamespaceA.NamespaceB.TableInNestedNS.pack(builder, _o.getFooTable());
    byte _fooUnionType = _o.getFooUnion() == null ? NamespaceA.NamespaceB.UnionInNestedNS.NONE : _o.getFooUnion().getType();
    int _fooUnion = _o.getFooUnion() == null ? 0 : NamespaceA.NamespaceB.UnionInNestedNSUnion.pack(builder, _o.getFooUnion());
    startTableInFirstNS(builder);
    addFooTable(builder, _foo_table);
    addFooEnum(builder, _o.getFooEnum());
    addFooUnionType(builder, _fooUnionType);
    addFooUnion(builder, _fooUnion);
    addFooStruct(builder, NamespaceA.NamespaceB.StructInNestedNS.pack(builder, _o.getFooStruct()));
    return endTableInFirstNS(builder);
  }
}
