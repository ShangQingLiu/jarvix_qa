
// function shuffle(o) {
//   for(var j, x, i = o.length; i; j = parseInt(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
//   return o;
// };
// const numbers = [...Array(1000).keys()]

// export function guidGenerator() {
//   var random = shuffle(numbers);
//   console.log(random);
//   return random;
// }
export const guidGenerator = () => parseInt(Date.now() * Math.random());
