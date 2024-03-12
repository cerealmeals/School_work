import { Framebuffer } from './framebuffer.js';
import { Rasterizer } from './rasterizer.js';
// DO NOT CHANGE ANYTHING ABOVE HERE

////////////////////////////////////////////////////////////////////////////////
// TODO: Implement functions drawLine(v1, v2) and drawTriangle(v1, v2, v3) below.
////////////////////////////////////////////////////////////////////////////////

// take two vertices defining line and rasterize to framebuffer
Rasterizer.prototype.drawLine = function(v1, v2) {
  const [x1, y1, [r1, g1, b1]] = v1;
  const [x2, y2, [r2, g2, b2]] = v2;
  // TODO/HINT: use this.setPixel(x, y, color) in this function to draw line
  let m = 0
  let flag = 0;
  if((x2-x1) != 0){
    m = (y2 - y1)/(x2-x1);
    this.setPixel(1, 0, [0.0, 0.0,1.0])
  }
  if(((x2-x1) == 0 || m < -1 || m > 1) && ((y2-y1) != 0)){
    m = (x2-x1)/(y2-y1);
    flag = 1;
    this.setPixel(0, 1, [1.0, 0.0,0.0])
  }
  this.setPixel(0, 0, [1.0, 1.0,1.0])
  
    if((flag == 0) && (m <= 0)){
      this.setPixel(2, 2, [0.0,0.0,0.0])
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
        this.setPixel(Math.floor(x), Math.floor(y), [r1, g1, b1])
        y += m;
      }
    }
    else if((flag == 1) && (m <= 0)){
      this.setPixel(60, 1, [0.0,0.0,0.0])
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
        this.setPixel(Math.floor(x), Math.floor(y), [r1, g1, b1])
        x += m;
      }
    }
      
    else if((flag == 1) && (m > 0)){
      this.setPixel(1, 60, [0.0,0.0,0.0])
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
        this.setPixel(Math.floor(x), Math.floor(y), [r1, g1, b1])
        x += m;
      }
    }
    
    else if((flag == 0) && (m > 0)){
      this.setPixel(60, 60, [0.0,0.0,0.0])
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
        this.setPixel(Math.floor(x), Math.floor(y), [r1, g1, b1])
        y += m;
      }
    }
    else{
      this.setPixel(2, 1, [1.0,0,0])
    }
 
  // this.setPixel(Math.floor(x1), Math.floor(y1), [r1, g1, b1]);
  // this.setPixel(Math.floor(x2), Math.floor(y2), [r2, g2, b2]);
}

// take 3 vertices defining a solid triangle and rasterize to framebuffer
function CorrectSideOfLine(v0,v1,p){
  let m = 0;

  let a = v1[1] - v0[1];
  let b = v0[0] - v1[0];
  let c = v0[0]*v1[1] - v1[0]*v0[1];

  m = a*p[0] + b*p[1] + c;

  if(m >= 0){
    return true;
  }
  else{
    return false;
  }
}
function pointIsInsideTriangle(v1,v2,v3,p){
  
  if(CorrectSideOfLine(v1,v2,p)&&CorrectSideOfLine(v2,v3,p)&&CorrectSideOfLine(v3,v1,p)){
    return true;
  }
  else return false;
}

Rasterizer.prototype.drawTriangle = function(v1, v2, v3) {
  const [x1, y1, [r1, g1, b1]] = v1;
  const [x2, y2, [r2, g2, b2]] = v2;
  const [x3, y3, [r3, g3, b3]] = v3;
  // TODO/HINT: use this.setPixel(x, y, color) in this function to draw triangle
  this.setPixel(Math.floor(x1), Math.floor(y1), [r1, g1, b1]);
  this.setPixel(Math.floor(x2), Math.floor(y2), [r2, g2, b2]);
  this.setPixel(Math.floor(x3), Math.floor(y3), [r3, g3, b3]);
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
  "v,10,10,1.0,0.0,0.0;",
  "v,50,10,0.0,1.0,0.0;",
  "v,10,50,1.0,0.0,1.0;",
  "v,50,50,0.0,0.0,1.0;",
  "v,25,10,0.0,0.0,1.0;",
  "v,25,50,0.0,0.0,1.0;",
  "l,3,0;",
  "l,0,4;"
].join("\n");


// DO NOT CHANGE ANYTHING BELOW HERE
export { Rasterizer, Framebuffer, DEF_INPUT };

