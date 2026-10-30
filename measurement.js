"use strict";
const SMRMeasurement=Object.freeze({
version:"SMR-SCORE-v01",
score(correctAnswers,answers){
if(!Array.isArray(correctAnswers)||!Array.isArray(answers)||correctAnswers.length===0||correctAnswers.length!==answers.length)throw new Error("Complete paired answer arrays required");
if([...correctAnswers,...answers].some(n=>!Number.isInteger(n)||n<0||n>2))throw new Error("Each response must be a valid index for this three-option instrument");
const correct=answers.reduce((count,answer,i)=>count+Number(answer===correctAnswers[i]),0);
return {answers:[...answers],correct,total:correctAnswers.length,percent:100*correct/correctAnswers.length};
},
changePercentagePoints(pre,post){
if(!pre||!post)return null;
if(![pre.percent,post.percent].every(n=>Number.isFinite(n)&&n>=0&&n<=100))throw new Error("Valid 0–100 percentages required");
return post.percent-pre.percent;
}
});
if(typeof module!=="undefined"&&module.exports)module.exports=SMRMeasurement;

