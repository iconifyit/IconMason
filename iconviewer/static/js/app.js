
Uint8Array.prototype.fromString = function(str) {
    uint=new Uint8Array(str.length);
    for(var i=0, j=str.length; i<j; ++i){
      uint[i]=str.charCodeAt(i);
    }
    return uint;
}

function svg2blob(data) {
  return new Blob(
    [Uint8Array.fromString(data)],{
        type: "image/svg+xml;charset=utf-8"
    });
}

function downloadIcon(iconData) {
    saveAs(iconData.svg, iconData.file);
}
