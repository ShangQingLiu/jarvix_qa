export function guidGenerator() {
  var S4 = function () {
    return (((1 + Math.random()) * 0x1000) | 0).toString(16).substring(1);
  };
  return S4() + "-" + S4();
}
