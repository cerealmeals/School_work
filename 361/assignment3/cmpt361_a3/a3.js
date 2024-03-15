import { Framebuffer } from './framebuffer.js';
import { Rasterizer } from './rasterizer.js';
// DO NOT CHANGE ANYTHING ABOVE HERE

////////////////////////////////////////////////////////////////////////////////
// TODO: Implement functions drawLine(v1, v2) and drawTriangle(v1, v2, v3) below.
////////////////////////////////////////////////////////////////////////////////

// take two vertices defining line and rasterize to framebuffer
function LinearInterperpolation(v1, v2, x, y){
  const [x1, y1, [r1, g1, b1]] = v1;
  const [x2, y2, [r2, g2, b2]] = v2;

  let t = 0;
  let numerator = Math.hypot(x - x1, y - y1);
  let denomerator = Math.hypot(x2 - x1, y2 - y1);
  if(denomerator != 0){
    t = numerator/denomerator;
  }

  let r = (1-t)*r1 + t*r2;
  let g = (1-t)*g1 + t*g2;
  let b = (1-t)*b1 + t*b2;
  let c = [r, g, b];
  return c;
}

Rasterizer.prototype.drawLine = function(v1, v2) {
  const [x1, y1, [r1, g1, b1]] = v1;
  const [x2, y2, [r2, g2, b2]] = v2;
  // TODO/HINT: use this.setPixel(x, y, color) in this function to draw line
  let slope = 0;
  let flag = 0;
  let c;
  if((x2-x1) != 0){
    slope = (y2 - y1)/(x2-x1);
    // this.setPixel(1, 0, [0.0, 0.0,1.0])
  }
  if(((x2-x1) == 0 || slope < -1 || slope > 1) && ((y2-y1) != 0)){
    slope = (x2-x1)/(y2-y1);
    flag = 1;
    // this.setPixel(0, 1, [1.0, 0.0,0.0]);
  }
  // this.setPixel(0, 0, [1.0, 1.0,1.0]);
  
    if((flag == 0) && (slope <= 0)){
      // this.setPixel(2, 2, [0.0,0.0,0.0]);
      let larger = 0, x = 0, y = 0;
      if(x1 < x2){
        x = x1;
        y = y1;
        larger = x2;
      }
      else{
        x = x2;
        y = y2;
        larger = x1;
      }
      for(; x <= larger; x++){
        c = LinearInterperpolation(v1, v2, x, y);
        let [cr, cg, cb] = c;
        this.setPixel(Math.floor(x), Math.floor(y), [cr, cg, cb]);
        y += slope;
      }
    }
    else if((flag == 1) && (slope <= 0)){
      // this.setPixel(60, 1, [0.0,0.0,0.0]);
      let larger = 0, x = 0, y = 0;
      if(y1 < y2){
        y = y1;
        x = x1;
        larger = y2;
      }
      else{
        y = y2;
        x = x2;
        larger = y1;
      }
      for(; y <= larger; y++){
        c = LinearInterperpolation(v1, v2, x, y);
        let [cr, cg, cb] = c;
        this.setPixel(Math.floor(x), Math.floor(y), [cr, cg, cb]);
        x += slope;
      }
    }
      
    else if((flag == 1) && (slope > 0)){
      // this.setPixel(1, 60, [0.0,0.0,0.0]);
      let larger = 0, x = 0, y = 0;
      
      if(y1 < y2){
        y = y1;
        x= x1;
        larger = y2;
      }
      else{
        y = y2;
        x = x2;
        larger = y1;
      }
      for(; y <= larger; y++){
        c = LinearInterperpolation(v1, v2, x, y);
        let [cr, cg, cb] = c;
        this.setPixel(Math.floor(x), Math.floor(y), [cr, cg, cb]);
        x += slope;
      }
    }
    
    else if((flag == 0) && (slope > 0)){
      // this.setPixel(60, 60, [0.0,0.0,0.0]);
      let larger = 0, x = 0, y = 0;
      if(x1 < x2){
        x = x1;
        y = y1;
        larger = x2;
      }
      else{
        x = x2;
        y = x2;
        larger = x1;
      }
      for(; x <= larger; x++){
        c = LinearInterperpolation(v1, v2, x, y);
        let [cr, cg, cb] = c;
        this.setPixel(Math.floor(x), Math.floor(y), [cr, cg, cb]);
        y += slope;
      }
    }
    else{
      this.setPixel(2, 1, [1.0,0,0]);
    }
 
  // this.setPixel(Math.floor(x1), Math.floor(y1), [r1, g1, b1]);
  // this.setPixel(Math.floor(x2), Math.floor(y2), [r2, g2, b2]);
}

// take 3 vertices defining a solid triangle and rasterize to framebuffer
function CorrectSideOfLineAndNotLine(v0,v1,p){
  let m = 0;

  let a = v1[1] - v0[1];
  let b = v0[0] - v1[0];
  let c = v1[0]*v0[1] - v0[0]*v1[1];

  m = a*p[0] + b*p[1] + c;

  if(m > 0){
    return true;
  }
  else{
    return false;
  }
}

function CorrectSideOfLineAndOnLine(v0,v1,p){
  let m = 0;

  let a = v1[1] - v0[1];
  let b = v0[0] - v1[0];
  let c = v1[0]*v0[1] - v0[0]*v1[1];

  m = a*p[0] + b*p[1] + c;

  if(m >= 0){
    return true;
  }
  else{
    return false;
  }
}

function EdgeCaseChecker(v1, v2, v3, p){
  if(v1[1] > v2[1]){
    return CorrectSideOfLineAndOnLine(v1, v2, p);
  }
  else if (v1[1] == v2[1] && v3[1] < v1[1]){
    return CorrectSideOfLineAndOnLine(v1, v2, p);
  }
  else{
    return CorrectSideOfLineAndNotLine(v1, v2, p);
  }
}
function pointIsInsideTriangle(v1,v2,v3,p){
  // egde case need to find top edge and left edge(s)
  let flag_for_side_1 = 0, flag_for_side_2 = 0, flag_for_side_3 = 0;
  
  flag_for_side_1 = EdgeCaseChecker(v1, v2, v3, p);
  flag_for_side_2 = EdgeCaseChecker(v2, v3, v1, p);
  flag_for_side_3 = EdgeCaseChecker(v3, v1, v2, p);
  
  if(flag_for_side_1&&flag_for_side_2&&flag_for_side_3){
    return true;
  }
  else{
    return false;
  }
}

function barycentricCoordinates(v1, v2, v3, p, area_of_main_triangle){
  const [x1, y1, [r1, g1, b1]] = v1;
  const [x2, y2, [r2, g2, b2]] = v2;
  const [x3, y3, [r3, g3, b3]] = v3;
  const [xp, yp] = p;
  let area1 = Math.abs((x2-xp)*(y3-yp)-(y2-yp)*(x3-xp))/2;
  let area2 = Math.abs((xp-x1)*(y3-y1)-(yp-y1)*(x3-x1))/2;
  let area3 = Math.abs((x2-x1)*(yp-y1)-(y2-y1)*(xp-x1))/2;
  let u = area1 / area_of_main_triangle;
  let v = area2 / area_of_main_triangle;
  let w = area3 / area_of_main_triangle;
  let r = u*r1 + v*r2 + w*r3;
  let g = u*g1 + v*g2 + w*g3;
  let b = u*b1 + v*b2 + w*b3;
  let c = [r, g, b];
  return c;
}

Rasterizer.prototype.drawTriangle = function(v1, v2, v3) {
  const [x1, y1, [r1, g1, b1]] = v1;
  const [x2, y2, [r2, g2, b2]] = v2;
  const [x3, y3, [r3, g3, b3]] = v3;
  
  let xmin = Math.min(x1, x2, x3);
  let xmax = Math.max(x1, x2, x3);
  let ymin = Math.min(y1, y2, y3);
  let ymax = Math.max(y1, y2, y3);
  let area_of_main_triangle = Math.abs(((x2-x1)*(y3-y1))-((y2-y1)*(x3-x1)))/2;
  

  for(let i = ymin; i < ymax+1; i++){
    for(let j = xmin; j < xmax+1; j++){
      //this.setPixel(j, i, [0,0,1.0]);
      let p = [j, i];
      if(pointIsInsideTriangle(v1, v2, v3, p)){
        
        let c = barycentricCoordinates(v1, v2, v3, p, area_of_main_triangle);
        let [cr, cg, cb] = c;
        this.setPixel(j, i, [cr, cg, cb]);
        //this.setPixel(j, i, [1.0,0,1.0]);
      }
    }
  }

  // TODO/HINT: use this.setPixel(x, y, color) in this function to draw triangle
  // this.setPixel(Math.floor(x1), Math.floor(y1), [r1, g1, b1]);
  // this.setPixel(Math.floor(x2), Math.floor(y2), [r2, g2, b2]);
  // this.setPixel(Math.floor(x3), Math.floor(y3), [r3, g3, b3]);
}


////////////////////////////////////////////////////////////////////////////////
// EXTRA CREDIT: change DEF_INPUT to create something interesting!
////////////////////////////////////////////////////////////////////////////////
const DEF_INPUT = [
  // "v,10,10,1.0,0.0,0.0;",
  // "v,52,52,0.0,1.0,0.0;",
  // "v,52,10,0.0,0.0,1.0;",
  // "v,10,52,1.0,1.0,1.0;",
  // "t,0,1,2;",
  // "t,0,3,1;",
  // "v,10,10,1.0,1.0,1.0;",
  // "v,10,52,0.0,0.0,0.0;",
  // "v,52,52,1.0,1.0,1.0;",
  // "v,52,10,0.0,0.0,0.0;",
  // "l,4,5;",
  // "l,5,6;",
  // "l,6,7;",
  // "l,7,4;"
  // "v,0,0,1.0,0.0,0.0;",
  // "v,5,5,0.0,1.0,0.0;",
  // "v,5,0,1.0,0.0,1.0;",
  // "v,50,50,0.0,0.0,1.0;",
  // "v,25,10,0.0,0.0,1.0;",
  // "v,25,50,0.0,0.0,1.0;",
  // "t,0,1,2;"
  "v,16,31,0,1.0,0;",
  "v,46,31,0,1.0,0;",
  "v,31,15,0,0,1.0;",
  "t,0,1,2;",
  "v,20,31,0,1.0,0;",
  "v,42,31,0,1.0,0;",
  "v,20,51,0.5,0.5,0.5;",
  "v,42,51,0.5,0.5,0.5;",
  "t,4,3,5;",
  "t,5,6,3;",
  "t,5,6,4;",
  "v,16,31,0.294,0.529,0.809;",
  "v,46,31,0.294,0.529,0.809;",
  "v,31,15,0.294,0.529,0.809;",
  "v,0,31,0.294,0.529,0.809;",
  "v,62,31,0.294,0.529,0.809;",
  "v,0,0,1.0,0.647,0;",
  "v,62,0,1.0,0.647,0;",
  "t,7,9,12;",
  "t,10,7,12;",
  "t,12,9,13;",
  "t,13,9,8;",
  "t,8,11,13;",
  "v,0,62,0,1.0,0;",
  "v,62,62,0,1.0,0;",
  "v,20,51,0,0.7,0;",
  "v,42,51,0,0.7,0;",
  "v,20,31,0.294,0.529,0.809;",
  "v,42,31,0.294,0.529,0.809;",
  "v,32,62,0,1.0,0;", 
  "t,11,19,15;",
  "t,17,15,19;",
  "t,17,20,15;",
  "t,17,16,20;",
  "t,16,14,20;",
  "t,16,18,14;",
  "t,14,18,10;",
  "v,0,0,0,0,0;",
  "v,0,63,0,0,0;",
  "v,63,63,0,0,0;",
  "v,63,0,0,0,0;",
  "l,21,22;",
  "l,22,23;",
  "l,23,24;",
  "l,24,21;"

].join("\n");


// DO NOT CHANGE ANYTHING BELOW HERE
export { Rasterizer, Framebuffer, DEF_INPUT };

