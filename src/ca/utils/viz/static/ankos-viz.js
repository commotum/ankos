(function () {
  "use strict";

  var MAGIC = "ANKOSV1\u0000";
  var HEADER_PREFIX_LENGTH = 12;

  function parseBundle(buffer) {
    var bytes = new Uint8Array(buffer);
    if (bytes.length < HEADER_PREFIX_LENGTH) {
      throw new Error("Bundle is shorter than the header prefix");
    }
    var magic = "";
    for (var i = 0; i < 8; i += 1) {
      magic += String.fromCharCode(bytes[i]);
    }
    if (magic !== MAGIC) {
      throw new Error("Bundle magic does not match ANKOSV1");
    }
    var view = new DataView(buffer);
    var headerLength = view.getUint32(8, true);
    var payloadBase = HEADER_PREFIX_LENGTH + headerLength;
    if (bytes.length < payloadBase) {
      throw new Error("Bundle is shorter than its declared header");
    }
    var headerText = new TextDecoder("utf-8").decode(bytes.slice(HEADER_PREFIX_LENGTH, payloadBase));
    var header = JSON.parse(headerText);
    var states = typedPayload(buffer, payloadBase, header.states);
    var coords = header.coords ? typedPayload(buffer, payloadBase, header.coords) : null;
    return {
      header: header,
      payloadBase: payloadBase,
      states: states,
      coords: coords
    };
  }

  function typedPayload(buffer, payloadBase, entry) {
    var ctor = dtypeCtor(entry.storage_dtype);
    var offset = payloadBase + entry.byte_offset;
    var length = entry.byte_length / ctor.BYTES_PER_ELEMENT;
    if (offset % ctor.BYTES_PER_ELEMENT !== 0) {
      throw new Error(entry.storage_dtype + " payload is not aligned");
    }
    if (length !== Math.floor(length)) {
      throw new Error(entry.storage_dtype + " payload byte length is invalid");
    }
    return new ctor(buffer, offset, length);
  }

  function dtypeCtor(dtype) {
    if (dtype === "uint8") {
      return Uint8Array;
    }
    if (dtype === "uint16") {
      return Uint16Array;
    }
    if (dtype === "int32") {
      return Int32Array;
    }
    throw new Error("Unsupported payload dtype " + dtype);
  }

  function shapeProduct(shape) {
    var out = 1;
    for (var i = 0; i < shape.length; i += 1) {
      out *= shape[i];
    }
    return out;
  }

  function rawValue(bundle, code) {
    if (bundle.header.value_map) {
      return bundle.header.value_map.values[code];
    }
    return code;
  }

  function stateAt(bundle, indices) {
    var shape = bundle.header.states.shape;
    var offset = 0;
    var stride = 1;
    for (var axis = shape.length - 1; axis >= 0; axis -= 1) {
      offset += indices[axis] * stride;
      stride *= shape[axis];
    }
    return bundle.states[offset];
  }

  function clamp(value, low, high) {
    return Math.max(low, Math.min(high, value));
  }

  function viewModesForDomain(domain) {
    if (domain === "t+0d") {
      return [["strip", "strip"]];
    }
    if (domain === "t+1d") {
      return [["spacetime", "spacetime"]];
    }
    if (domain === "t+2d") {
      return [["frame", "frame"]];
    }
    if (domain === "t+3d") {
      return [["slice", "slice"]];
    }
    return [["raw", "raw"]];
  }

  function formatShape(shape) {
    return "(" + shape.join(", ") + ")";
  }

  window.ANKOSViz = {
    parseBundle: parseBundle,
    shapeProduct: shapeProduct,
    rawValue: rawValue,
    stateAt: stateAt,
    clamp: clamp,
    viewModesForDomain: viewModesForDomain,
    formatShape: formatShape
  };
}());
