(function () {
  "use strict";

  var app = {
    bundle: null,
    playing: false,
    timer: null,
    zoom: "fit"
  };

  var el = {};

  window.addEventListener("DOMContentLoaded", function () {
    el.fileInput = document.getElementById("fileInput");
    el.viewMode = document.getElementById("viewMode");
    el.timeSlider = document.getElementById("timeSlider");
    el.timeValue = document.getElementById("timeValue");
    el.prevButton = document.getElementById("prevButton");
    el.playButton = document.getElementById("playButton");
    el.nextButton = document.getElementById("nextButton");
    el.sliceControl = document.getElementById("sliceControl");
    el.sliceAxis = document.getElementById("sliceAxis");
    el.projectionMode = document.getElementById("projectionMode");
    el.sliceSlider = document.getElementById("sliceSlider");
    el.sliceValue = document.getElementById("sliceValue");
    el.zoomSelect = document.getElementById("zoomSelect");
    el.canvas = document.getElementById("viewCanvas");
    el.meta = document.getElementById("meta");
    app.ctx = el.canvas.getContext("2d", { alpha: false });
    app.ctx.imageSmoothingEnabled = false;

    el.fileInput.addEventListener("change", onFileChange);
    el.viewMode.addEventListener("change", render);
    el.timeSlider.addEventListener("input", function () {
      el.timeValue.textContent = el.timeSlider.value;
      render();
    });
    el.sliceAxis.addEventListener("change", configureSlice);
    el.projectionMode.addEventListener("change", function () {
      configureSlice();
      render();
    });
    el.sliceSlider.addEventListener("input", function () {
      el.sliceValue.textContent = el.sliceSlider.value;
      render();
    });
    el.zoomSelect.addEventListener("change", function () {
      app.zoom = el.zoomSelect.value;
      render();
    });
    el.prevButton.addEventListener("click", function () { stepTime(-1); });
    el.nextButton.addEventListener("click", function () { stepTime(1); });
    el.playButton.addEventListener("click", togglePlay);
    el.canvas.addEventListener("mousemove", inspectCanvas);
    el.canvas.addEventListener("mouseleave", function () {
      app.inspectText = "";
      updateMeta();
    });
    window.addEventListener("resize", render);
    setMeta("No bundle loaded");
    loadBundleFromQuery();
  });

  function onFileChange(event) {
    var file = event.target.files && event.target.files[0];
    if (!file) {
      return;
    }
    file.arrayBuffer().then(function (buffer) {
      app.bundle = window.ANKOSViz.parseBundle(buffer);
      configureControls();
      render();
    }).catch(function (err) {
      stopPlayback();
      app.bundle = null;
      setMeta(err.message);
      clearCanvas();
    });
  }

  function loadBundleFromQuery() {
    var params = new URLSearchParams(window.location.search);
    var bundleUrl = params.get("bundle");
    if (!bundleUrl) {
      return;
    }
    fetch(bundleUrl).then(function (response) {
      if (!response.ok) {
        throw new Error("Bundle request failed with HTTP " + response.status);
      }
      return response.arrayBuffer();
    }).then(function (buffer) {
      app.bundle = window.ANKOSViz.parseBundle(buffer);
      configureControls();
      render();
    }).catch(function (err) {
      setMeta(err.message);
      clearCanvas();
    });
  }

  function configureControls() {
    var bundle = app.bundle;
    var header = bundle.header;
    var modes = window.ANKOSViz.viewModesForDomain(header.domain);
    el.viewMode.textContent = "";
    modes.forEach(function (mode) {
      var option = document.createElement("option");
      option.value = mode[0];
      option.textContent = mode[1];
      el.viewMode.appendChild(option);
    });

    el.timeSlider.min = "0";
    el.timeSlider.max = String(Math.max(0, header.steps - 1));
    el.timeSlider.value = "0";
    el.timeValue.textContent = "0";

    el.sliceControl.classList.toggle("hidden", header.domain !== "t+3d");
    configureSlice();
    updateMeta();
  }

  function configureSlice() {
    if (!app.bundle || app.bundle.header.domain !== "t+3d") {
      return;
    }
    var shape = app.bundle.header.shape;
    var axis = el.sliceAxis.value;
    var maxIndex = axis === "xy" ? shape[2] - 1 : (axis === "xz" ? shape[1] - 1 : shape[0] - 1);
    var isProjection = el.projectionMode.value !== "slice";
    el.sliceSlider.disabled = isProjection;
    el.sliceSlider.min = "0";
    el.sliceSlider.max = String(Math.max(0, maxIndex));
    el.sliceSlider.value = String(window.ANKOSViz.clamp(Number(el.sliceSlider.value), 0, maxIndex));
    el.sliceValue.textContent = el.sliceSlider.value;
    render();
  }

  function render() {
    if (!app.bundle) {
      clearCanvas();
      return;
    }
    var mode = el.viewMode.value;
    var image;
    if (mode === "strip") {
      image = renderStrip(app.bundle);
    } else if (mode === "spacetime") {
      image = renderSpacetime(app.bundle);
    } else if (mode === "frame") {
      image = renderFrame(app.bundle);
    } else if (mode === "slice") {
      image = el.projectionMode.value === "slice" ? renderSlice(app.bundle) : renderProjection(app.bundle);
    } else {
      image = renderRaw(app.bundle);
    }
    drawImage(image);
    updateMeta();
  }

  function renderStrip(bundle) {
    var shape = bundle.header.states.shape;
    var width = shape[0];
    var image = new ImageData(width, 1);
    for (var t = 0; t < width; t += 1) {
      writeColor(bundle, image.data, t, bundle.states[t]);
    }
    return image;
  }

  function renderSpacetime(bundle) {
    var shape = bundle.header.states.shape;
    var steps = shape[0];
    var xSize = shape[1];
    var image = new ImageData(xSize, steps);
    var out = 0;
    for (var t = 0; t < steps; t += 1) {
      for (var x = 0; x < xSize; x += 1) {
        writeColor(bundle, image.data, out, bundle.states[t * xSize + x]);
        out += 1;
      }
    }
    return image;
  }

  function renderProjection(bundle) {
    var shape = bundle.header.states.shape;
    var t = Number(el.timeSlider.value);
    var axis = el.sliceAxis.value;
    var mode = el.projectionMode.value;
    var xSize = shape[1];
    var ySize = shape[2];
    var zSize = shape[3];
    var imageWidth = axis === "yz" ? ySize : xSize;
    var imageHeight = axis === "xy" ? ySize : zSize;
    var image = new ImageData(imageWidth, imageHeight);
    var frameOffset = t * xSize * ySize * zSize;
    var maxSum = axis === "xy" ? zSize : (axis === "xz" ? ySize : xSize);
    var out = 0;
    for (var row = 0; row < imageHeight; row += 1) {
      for (var col = 0; col < imageWidth; col += 1) {
        var projected = projectCell(bundle, frameOffset, axis, mode, col, row, xSize, ySize, zSize);
        if (mode === "sum") {
          writeGray(image.data, out, projected, maxSum);
        } else {
          writeColor(bundle, image.data, out, projected);
        }
        out += 1;
      }
    }
    return image;
  }

  function projectCell(bundle, frameOffset, axis, mode, col, row, xSize, ySize, zSize) {
    var limit = axis === "xy" ? zSize : (axis === "xz" ? ySize : xSize);
    var aggregate = mode === "first-active" ? 0 : 0;
    for (var i = 0; i < limit; i += 1) {
      var x;
      var y;
      var z;
      if (axis === "xy") {
        x = col;
        y = row;
        z = i;
      } else if (axis === "xz") {
        x = col;
        y = i;
        z = row;
      } else {
        x = i;
        y = col;
        z = row;
      }
      var code = bundle.states[frameOffset + ((x * ySize + y) * zSize + z)];
      if (mode === "sum") {
        aggregate += code;
      } else if (mode === "max") {
        aggregate = Math.max(aggregate, code);
      } else if (mode === "first-active" && code !== 0) {
        return code;
      }
    }
    return aggregate;
  }

  function renderFrame(bundle) {
    var shape = bundle.header.states.shape;
    var t = Number(el.timeSlider.value);
    var xSize = shape[1];
    var ySize = shape[2];
    var frameOffset = t * xSize * ySize;
    var image = new ImageData(xSize, ySize);
    var out = 0;
    for (var y = 0; y < ySize; y += 1) {
      for (var x = 0; x < xSize; x += 1) {
        writeColor(bundle, image.data, out, bundle.states[frameOffset + x * ySize + y]);
        out += 1;
      }
    }
    return image;
  }

  function renderSlice(bundle) {
    var shape = bundle.header.states.shape;
    var t = Number(el.timeSlider.value);
    var axis = el.sliceAxis.value;
    var slice = Number(el.sliceSlider.value);
    var xSize = shape[1];
    var ySize = shape[2];
    var zSize = shape[3];
    var imageWidth = axis === "yz" ? ySize : xSize;
    var imageHeight = axis === "xy" ? ySize : zSize;
    var image = new ImageData(imageWidth, imageHeight);
    var frameOffset = t * xSize * ySize * zSize;
    var out = 0;
    for (var row = 0; row < imageHeight; row += 1) {
      for (var col = 0; col < imageWidth; col += 1) {
        var x;
        var y;
        var z;
        if (axis === "xy") {
          x = col;
          y = row;
          z = slice;
        } else if (axis === "xz") {
          x = col;
          y = slice;
          z = row;
        } else {
          x = slice;
          y = col;
          z = row;
        }
        var offset = frameOffset + ((x * ySize + y) * zSize + z);
        writeColor(bundle, image.data, out, bundle.states[offset]);
        out += 1;
      }
    }
    return image;
  }

  function renderRaw(bundle) {
    var shape = bundle.header.states.shape;
    var width = shape[shape.length - 1] || 1;
    var height = Math.ceil(bundle.states.length / width);
    var image = new ImageData(width, height);
    for (var i = 0; i < bundle.states.length; i += 1) {
      writeColor(bundle, image.data, i, bundle.states[i]);
    }
    return image;
  }

  function writeColor(bundle, rgba, index, code) {
    var colors = bundle.header.palette.colors;
    var color = colors[code % colors.length];
    var offset = index * 4;
    rgba[offset] = color[0];
    rgba[offset + 1] = color[1];
    rgba[offset + 2] = color[2];
    rgba[offset + 3] = color[3];
  }

  function writeGray(rgba, index, value, maxValue) {
    var level = maxValue <= 0 ? 0 : Math.round(255 * Math.min(1, value / maxValue));
    var offset = index * 4;
    rgba[offset] = level;
    rgba[offset + 1] = level;
    rgba[offset + 2] = level;
    rgba[offset + 3] = 255;
  }

  function drawImage(image) {
    var ctx = app.ctx;
    var canvas = el.canvas;
    var rect = canvas.parentElement.getBoundingClientRect();
    var zoom = app.zoom;
    var targetWidth;
    var targetHeight;
    if (zoom === "fit") {
      var fitScale = Math.min(rect.width / image.width, rect.height / image.height);
      var scale = fitScale >= 1 ? Math.max(1, Math.floor(fitScale)) : fitScale;
      targetWidth = image.width * scale;
      targetHeight = image.height * scale;
    } else {
      var scaleFixed = Number(zoom);
      targetWidth = image.width * scaleFixed;
      targetHeight = image.height * scaleFixed;
    }
    canvas.width = Math.max(1, Math.floor(rect.width));
    canvas.height = Math.max(1, Math.floor(rect.height));
    ctx.imageSmoothingEnabled = false;
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    var tmp = getScratchCanvas(image.width, image.height);
    tmp.ctx.putImageData(image, 0, 0);
    var left = Math.floor((canvas.width - targetWidth) / 2);
    var top = Math.floor((canvas.height - targetHeight) / 2);
    ctx.drawImage(tmp.canvas, left, top, targetWidth, targetHeight);
    app.drawInfo = {
      left: left,
      top: top,
      width: targetWidth,
      height: targetHeight,
      imageWidth: image.width,
      imageHeight: image.height,
      mode: el.viewMode.value,
      time: Number(el.timeSlider.value),
      sliceAxis: el.sliceAxis.value,
      slice: Number(el.sliceSlider.value),
      projection: el.projectionMode.value
    };
  }

  function getScratchCanvas(width, height) {
    if (!app.scratch) {
      app.scratch = {
        canvas: document.createElement("canvas"),
        ctx: null
      };
      app.scratch.ctx = app.scratch.canvas.getContext("2d", { alpha: false });
    }
    app.scratch.canvas.width = width;
    app.scratch.canvas.height = height;
    app.scratch.ctx.imageSmoothingEnabled = false;
    return app.scratch;
  }

  function clearCanvas() {
    if (!app.ctx) {
      return;
    }
    var rect = el.canvas.parentElement.getBoundingClientRect();
    el.canvas.width = Math.max(1, Math.floor(rect.width));
    el.canvas.height = Math.max(1, Math.floor(rect.height));
    app.ctx.fillStyle = "#ffffff";
    app.ctx.fillRect(0, 0, el.canvas.width, el.canvas.height);
  }

  function stepTime(delta) {
    if (!app.bundle) {
      return;
    }
    var maxValue = Number(el.timeSlider.max);
    var next = Number(el.timeSlider.value) + delta;
    if (next > maxValue) {
      next = 0;
    }
    if (next < 0) {
      next = maxValue;
    }
    el.timeSlider.value = String(next);
    el.timeValue.textContent = el.timeSlider.value;
    render();
  }

  function togglePlay() {
    if (app.playing) {
      stopPlayback();
      return;
    }
    app.playing = true;
    el.playButton.textContent = "Pause";
    app.timer = window.setInterval(function () {
      stepTime(1);
    }, 120);
  }

  function stopPlayback() {
    app.playing = false;
    el.playButton.textContent = "Play";
    if (app.timer) {
      window.clearInterval(app.timer);
      app.timer = null;
    }
  }

  function updateMeta() {
    if (!app.bundle) {
      return;
    }
    var h = app.bundle.header;
    var items = [
      "domain " + h.domain,
      "shape " + window.ANKOSViz.formatShape(h.shape),
      "steps " + h.steps,
      "rule " + h.rule_id,
      "layout " + h.states.layout,
      h.states.storage_mode + " " + h.states.storage_dtype
    ];
    if (app.inspectText) {
      items.push(app.inspectText);
    }
    setMeta(items);
  }

  function inspectCanvas(event) {
    if (!app.bundle || !app.drawInfo) {
      return;
    }
    var rect = el.canvas.getBoundingClientRect();
    var x = event.clientX - rect.left;
    var y = event.clientY - rect.top;
    var info = app.drawInfo;
    var col = Math.floor(((x - info.left) / info.width) * info.imageWidth);
    var row = Math.floor(((y - info.top) / info.height) * info.imageHeight);
    if (col < 0 || row < 0 || col >= info.imageWidth || row >= info.imageHeight) {
      app.inspectText = "";
      updateMeta();
      return;
    }
    app.inspectText = inspectionText(col, row);
    updateMeta();
  }

  function inspectionText(col, row) {
    var bundle = app.bundle;
    var h = bundle.header;
    var mode = app.drawInfo.mode;
    if (mode === "strip") {
      return stateText([col], [col, 0, 0, 0]);
    }
    if (mode === "spacetime") {
      return stateText([row, col], [row, centeredCoord(col, h.shape[0]), 0, 0]);
    }
    if (mode === "frame") {
      return stateText([app.drawInfo.time, col, row], [
        app.drawInfo.time,
        centeredCoord(col, h.shape[0]),
        centeredCoord(row, h.shape[1]),
        0
      ]);
    }
    if (mode === "slice" && app.drawInfo.projection === "slice") {
      return sliceInspectionText(col, row);
    }
    if (mode === "slice") {
      return "projection " + app.drawInfo.sliceAxis + " [" + col + ", " + row + "]";
    }
    return "[" + col + ", " + row + "]";
  }

  function sliceInspectionText(col, row) {
    var h = app.bundle.header;
    var axis = app.drawInfo.sliceAxis;
    var x;
    var y;
    var z;
    if (axis === "xy") {
      x = col;
      y = row;
      z = app.drawInfo.slice;
    } else if (axis === "xz") {
      x = col;
      y = app.drawInfo.slice;
      z = row;
    } else {
      x = app.drawInfo.slice;
      y = col;
      z = row;
    }
    return stateText([app.drawInfo.time, x, y, z], [
      app.drawInfo.time,
      centeredCoord(x, h.shape[0]),
      centeredCoord(y, h.shape[1]),
      centeredCoord(z, h.shape[2])
    ]);
  }

  function stateText(indices, coord) {
    var code = window.ANKOSViz.stateAt(app.bundle, indices);
    var value = window.ANKOSViz.rawValue(app.bundle, code);
    return "cell [" + coord.join(", ") + "] = " + value;
  }

  function centeredCoord(index, size) {
    var half = Math.floor(size / 2);
    if (size % 2) {
      return index - half;
    }
    return index - half + 1;
  }

  function setMeta(items) {
    if (!Array.isArray(items)) {
      items = [items];
    }
    el.meta.textContent = "";
    items.forEach(function (item) {
      var span = document.createElement("span");
      span.textContent = item;
      el.meta.appendChild(span);
    });
  }
}());
