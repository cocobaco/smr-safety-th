"use strict";
const assert=require("node:assert/strict");
const path=require("node:path");
const measurement=require(path.resolve(process.argv[2]));
const key=[1,2,0];
assert.equal(measurement.score(key,[1,2,0]).percent,100);
assert.equal(measurement.score(key,[0,0,1]).percent,0);
assert.ok(Math.abs(measurement.score(key,[1,2,1]).percent-66.66666666666667)<1e-10);
assert.equal(measurement.score(key,[0,0,0]).correct,1);
assert.equal(Number(measurement.changePercentagePoints({percent:100/3},{percent:100}).toFixed(1)),66.7);
assert.equal(measurement.changePercentagePoints({percent:100},{percent:0}),-100);
assert.equal(measurement.changePercentagePoints(null,{percent:100}),null);
assert.throws(()=>measurement.score([],[]));
assert.throws(()=>measurement.score(key,[1]));
assert.throws(()=>measurement.score(key,[1,2,NaN]));
assert.throws(()=>measurement.score(key,[1,2,3]));
assert.throws(()=>measurement.changePercentagePoints({percent:101},{percent:0}));
console.log(JSON.stringify({result:"Pass",checks:12,scope:"Actual shared scoring module; valid, missing, zero, boundary and percentage-point cases; no reader impact data"}));

