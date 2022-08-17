var p = function (e) {
    for (c = [], s = 0; s < 256; ++s)
        c.push((s + 256).toString(16).substr(1));

    var t = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : 0
        ,
        n = (c[e[t + 0]] + c[e[t + 1]] + c[e[t + 2]] + c[e[t + 3]] + "-" + c[e[t + 4]] + c[e[t + 5]] + "-" + c[e[t + 6]] + c[e[t + 7]] + "-" + c[e[t + 8]] + c[e[t + 9]] + "-" + c[e[t + 10]] + c[e[t + 11]] + c[e[t + 12]] + c[e[t + 13]] + c[e[t + 14]] + c[e[t + 15]]).toLowerCase();

    return n
}

p(crypto.getRandomValues(new Uint8Array(16)))