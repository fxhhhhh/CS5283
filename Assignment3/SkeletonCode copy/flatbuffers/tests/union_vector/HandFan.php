<?php
// automatically generated by the FlatBuffers compiler, do not modify

use \Google\FlatBuffers\Struct;
use \Google\FlatBuffers\Table;
use \Google\FlatBuffers\ByteBuffer;
use \Google\FlatBuffers\FlatBufferBuilder;

class HandFan extends Table
{
    /**
     * @param ByteBuffer $bb
     * @return HandFan
     */
    public static function getRootAsHandFan(ByteBuffer $bb)
    {
        $obj = new HandFan();
        return ($obj->init($bb->getInt($bb->getPosition()) + $bb->getPosition(), $bb));
    }

    public static function HandFanIdentifier()
    {
        return "MOVI";
    }

    public static function HandFanBufferHasIdentifier(ByteBuffer $buf)
    {
        return self::__has_identifier($buf, self::HandFanIdentifier());
    }

    /**
     * @param int $_i offset
     * @param ByteBuffer $_bb
     * @return HandFan
     **/
    public function init($_i, ByteBuffer $_bb)
    {
        $this->bb_pos = $_i;
        $this->bb = $_bb;
        return $this;
    }

    /**
     * @return int
     */
    public function getLength()
    {
        $o = $this->__offset(4);
        return $o != 0 ? $this->bb->getInt($o + $this->bb_pos) : 0;
    }

    /**
     * @param FlatBufferBuilder $builder
     * @return void
     */
    public static function startHandFan(FlatBufferBuilder $builder)
    {
        $builder->StartObject(1);
    }

    /**
     * @param FlatBufferBuilder $builder
     * @return HandFan
     */
    public static function createHandFan(FlatBufferBuilder $builder, $length)
    {
        $builder->startObject(1);
        self::addLength($builder, $length);
        $o = $builder->endObject();
        return $o;
    }

    /**
     * @param FlatBufferBuilder $builder
     * @param int
     * @return void
     */
    public static function addLength(FlatBufferBuilder $builder, $length)
    {
        $builder->addIntX(0, $length, 0);
    }

    /**
     * @param FlatBufferBuilder $builder
     * @return int table offset
     */
    public static function endHandFan(FlatBufferBuilder $builder)
    {
        $o = $builder->endObject();
        return $o;
    }
}
