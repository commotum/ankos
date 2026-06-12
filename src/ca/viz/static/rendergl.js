(function () {
  "use strict";

  window.ANKOSVizGL = {
    available: function (canvas) {
      return !!(canvas && canvas.getContext && canvas.getContext("webgl2"));
    }
  };
}());
