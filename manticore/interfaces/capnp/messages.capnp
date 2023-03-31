# messages.capnp
@0x92fc066f6f6be06d;

using import "common.capnp".Object;


struct MockV1 {
    obj @0 :Object;
    data @1 :Text;
}

struct MockV2 {
    obj @0 :Object;
    data @1 :Text;
    data2 @2 :Text;
}
