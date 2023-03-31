# common.capnp
@0xfc7047536f2cc43c;

struct Package {
    objType @0 :Text;
    objVersion @1 :UInt64;
    source @2 :Text;
    destination @3 :Text;
    payload @4 :AnyPointer;
}

struct Object {
    id @0 :Text;
    timestamp @1 :UInt64;
}

struct Request {
    obj @0 :Object;
}

struct Response {
    obj @0 :Object;
    status @1 :UInt64;
    detail @2 :Text;
}
