import { Mat4 } from './math.js';
import { Parser } from './parser.js';
import { Scene } from './scene.js';
import { Renderer } from './renderer.js';
import { TriangleMesh } from './trianglemesh.js';
// DO NOT CHANGE ANYTHING ABOVE HERE

////////////////////////////////////////////////////////////////////////////////
// TODO: Implement createCube, createSphere, computeTransformation, and shaders
////////////////////////////////////////////////////////////////////////////////

// Example two triangle quad
const quad = {
  positions: [-1, -1, -1,
              1, -1, -1, 
              1, 1, -1, 
              -1, -1, -1, 
              1,  1, -1, 
              -1,  1, -1],
  normals: [0, 0, 1,
            0, 0, 1, 
            0, 0, 1, 
            0, 0, 1, 
            0, 0, 1, 
            0, 0, 1],
  uvCoords: [0, 0, 
             1, 0, 
             1, 1, 
             0, 0, 
             1, 1, 
             0, 1]
}

const cube ={
  positions: [
              // front face
              1,1,1,    -1,1,1,   1,-1,1,
              -1,1,1,   -1,-1,1,  1,-1,1,
              //back face
              1,1,-1,   1,-1,-1,  -1,-1,-1,
              -1,1,-1,  1,1,-1,   -1,-1,-1,
              // right face
              1,1,1,    1,-1,1,   1,-1,-1,
              1,1,1,    1,-1,-1,  1,1,-1,
              // left face
              -1,1,-1,  -1,-1,-1, -1,-1,1,
              -1,1,-1,  -1,-1,1,  -1,1,1,
              //top face
              1,1,1,    1,1,-1,   -1,1,-1,
              1,1,1,    -1,1,-1,  -1,1,1,
              //bottom face
              1,-1,-1,  -1,-1,1,  -1,-1,-1,
              1,-1,-1,  1,-1,1,   -1,-1,1
            ],
  normals: [
            // front face
            0, 0, 1,    0, 0, 1,  0, 0, 1, 
            0, 0, 1,    0, 0, 1,  0, 0, 1,
            // back face
            0, 0, -1,    0, 0, -1,  0, 0, -1, 
            0, 0, -1,    0, 0, -1,  0, 0, -1,
            // right face
            1, 0, 0,    1, 0, 0,  1, 0, 0, 
            1, 0, 0,    1, 0, 0,  1, 0, 0,
            // left face
            -1, 0, 0,    -1, 0, 0,  -1, 0, 0, 
            -1, 0, 0,    -1, 0, 0,  -1, 0, 0,
            // top face
            0, 1, 0,    0, 1, 0,  0, 1, 0, 
            0, 1, 0,    0, 1, 0,  0, 1, 0,
            // buttom face
            0, -1, 0,    0, -1, 0,  0, -1, 0, 
            0, -1, 0,    0, -1, 0,  0, -1, 0
          ],
  uvCoords: [
             // front face
             0.5,1,     0,1,      0.5,(2/3),
             0,1,       0,(2/3),  0.5,(2/3),
             //back face
             0.5,(1/3), 0.5,0,    1,0,
             1,(1/3),   0.5,(1/3),1,0,
             // right face
             0,(2/3),   0,(1/3),  0.5,(1/3),
             0,(2/3),   0.5,(1/3),0.5,(2/3),
             // left face
             0.5,(2/3), 0.5,(1/3),1,(1/3),
             0.5,(2/3), 1,(1/3),  1,(2/3),
             //top face
             0.5,0,     0.5,(1/3),0,(1/3),
             0.5,0,     0,(1/3),  0,0,
             //bottom face
             0.5,1,     1,(2/3),  1,1,
             0.5,1,     0.5,(2/3),1,(2/3) 
          ],
  // indices: [(0,4,2), (4,6,2), (0,5,4), (1,5,0), (0,2,3), (0,3,1), (1,3,7), (1,7,5), (5,7,6), (5,6,4), (3,2,6), (3,6,7)]
}

TriangleMesh.prototype.createCube = function() {
  // TODO: populate unit cube vertex positions, normals, and uv coordinates
  this.positions = cube.positions;
  this.normals = cube.normals;
  this.uvCoords = cube.uvCoords;
  // this.indices = cube.indices
}

TriangleMesh.prototype.createSphere = function(numStacks, numSectors) {
  // TODO: populate unit sphere vertex positions, normals, uv coordinates, and indices
  

  // code taken from http://www.songho.ca/opengl/gl_sphere.html then was modified by myself

  var radius = 1.0;
  var x, y, z, xy;                              // vertex position
  var nx, ny, nz, lengthInv = 1.0 / radius;     // vertex normal
  var s, t;                                     // vertex texCoord

  var sectorStep = 2 * Math.PI / numSectors;
  var stackStep = Math.PI / numStacks;
  var sectorAngle, stackAngle;

  for(var i = 0; i <= numStacks; ++i)
  {
      stackAngle = ((-Math.PI) / 2) + i * stackStep;        // starting from -pi/2 to pi/2
      xy = radius * Math.cos(stackAngle);             // r * cos(u)
      z = radius * Math.sin(stackAngle);              // r * sin(u)

      // add (numSectors+1) vertices per stack
      // first and last vertices have same position and normal, but different tex coords
      for(var j = 0; j <= numSectors; ++j)
      {
          sectorAngle = j * sectorStep;           // starting from 0 to 2pi

          // vertex position (x, y, z)
          x = xy * Math.cos(sectorAngle);             // r * cos(u) * cos(v)
          y = xy * Math.sin(sectorAngle);             // r * cos(u) * sin(v)
          this.positions.push(x);
          this.positions.push(y);
          this.positions.push(z);

          // normalized vertex normal (nx, ny, nz)
          nx = x * lengthInv;
          ny = y * lengthInv;
          nz = z * lengthInv;
          this.normals.push(nx);
          this.normals.push(ny);
          this.normals.push(nz);

          // vertex tex coord (s, t) range between [0, 1]
          s = 1 -(j / numSectors);
          t = 1 -(i / numStacks);
          this.uvCoords.push(s);
          this.uvCoords.push(t);
      }
  }
  var k1, k2;
  for(var i = 0; i < numStacks; ++i)
  {
      k1 = i * (numSectors + 1);     // beginning of current stack
      k2 = k1 + numSectors + 1;      // beginning of next stack

      for(var j = 0; j < numSectors; ++j, ++k1, ++k2)
      {
          // 2 triangles per sector excluding first and last stacks
          // k1 => k2 => k1+1
          if(i != 0)
          {
              this.indices.push(k1);
              this.indices.push(k2);
              this.indices.push(k1 + 1);
          }

          // k1+1 => k2 => k2+1
          if(i != (numStacks-1))
          {
              this.indices.push(k1 + 1);
              this.indices.push(k2);
              this.indices.push(k2 + 1);
          }
      }
  }
}

Scene.prototype.computeTransformation = function(transformSequence) {
  // TODO: go through transform sequence and compose into overallTransform
  // console.log("transform Sequence " + transformSequence);
  let overallTransform = Mat4.create();  // identity matrix
  
  for(let i = 0; i < transformSequence.length; i++){
    // console.log("check "+transformSequence[i]);
    
    if(transformSequence[i][0] == "Rz"){
      let rotate_z_axis = Mat4.create();
      let radians = transformSequence[i][1] * Math.PI / 180;
      Mat4.set(rotate_z_axis, Math.cos(radians),Math.sin(radians),0,0,
                              -Math.sin(radians),Math.cos(radians),0,0,
                              0,0,1,0,
                              0,0,0,1);
      // console.log(rotate_z_axis);
      Mat4.multiply(overallTransform, rotate_z_axis, overallTransform);
    }
    if(transformSequence[i][0] == "Rx"){
      let rotate_x_axis = Mat4.create();
      let radians = transformSequence[i][1] * Math.PI / 180;
      Mat4.set(rotate_x_axis, 1,0,0,0,
                              0,Math.cos(radians),Math.sin(radians),0,
                              0,-Math.sin(radians),Math.cos(radians),0,
                              0,0,0,1);
      // console.log(rotate_x_axis);
      Mat4.multiply(overallTransform, rotate_x_axis, overallTransform);
    }
    if(transformSequence[i][0] == "Ry"){
      let rotate_y_axis = Mat4.create();
      let radians = transformSequence[i][1] * Math.PI / 180;
      Mat4.set(rotate_y_axis, Math.cos(radians),0,-Math.sin(radians),0, 
                              0, 1, 0, 0,
                              Math.sin(radians),0,Math.cos(radians),0,
                              0,0,0,1);
      // console.log(rotate_y_axis);
      Mat4.multiply(overallTransform, rotate_y_axis, overallTransform);
    }
    if(transformSequence[i][0] == "S"){
      let scale_matix = Mat4.create();
      Mat4.set(scale_matix, transformSequence[i][1],0,0,0
                            ,0,transformSequence[i][2],0,0
                            ,0,0,transformSequence[i][3],0
                            ,0,0,0,1);
      // console.log(scale_matix);
      Mat4.multiply(overallTransform, scale_matix, overallTransform);
    }
    if(transformSequence[i][0] == "T"){
      let translate_matrix = Mat4.create();
      Mat4.set(translate_matrix, 1,0,0,0
                            ,0,1,0,0
                            ,0,0,1,0
                            ,transformSequence[i][1],transformSequence[i][2],transformSequence[i][3],1);
      // console.log(translate_matrix);
      Mat4.multiply(overallTransform, translate_matrix, overallTransform);
    }
  }
  
  // console.log(overallTransform);
  
  return overallTransform;
}

Renderer.prototype.VERTEX_SHADER = `
precision mediump float;
attribute vec3 position, normal;
attribute vec2 uvCoord;
uniform vec3 lightPosition;
uniform mat4 projectionMatrix, viewMatrix, modelMatrix;
uniform mat3 normalMatrix;
varying vec2 vTexCoord;

// TODO: implement vertex shader logic below

varying vec3 fNormal;
varying vec3 fPosition;
varying vec3 light_dir;

void main()
{
  fNormal = normalize(normalMatrix * normal);
  vec4 pos = viewMatrix * modelMatrix * vec4(position, 1.0);
  fPosition = pos.xyz;
  light_dir = normalize(lightPosition - fPosition);
  vTexCoord = uvCoord;
  gl_Position = projectionMatrix * pos;
}
`;

Renderer.prototype.FRAGMENT_SHADER = `
precision mediump float;
uniform vec3 ka, kd, ks, lightIntensity;
uniform float shininess;
uniform sampler2D uTexture;
uniform bool hasTexture;
varying vec2 vTexCoord;

// TODO: implement fragment shader logic below

varying vec3 fPosition;
varying vec3 fNormal;
varying vec3 light_dir;

void main()
{
  // ambient
  vec3 col_ambient = ka * lightIntensity;

  // diffuse
  float n_dot_l = dot(-light_dir, fNormal);
  vec3 col_diffuse = kd * max(0.0, n_dot_l) * lightIntensity;

  // phong specular
  vec3 v = normalize(fPosition);
  vec3 H = normalize((light_dir + v));
  float H_dot_n = dot(H, fNormal);
  vec3 col_spec = ks * pow(max(0.0,H_dot_n), shininess) * lightIntensity;

  vec3 col = col_ambient + col_diffuse + col_spec;

  if(hasTexture){
    vec4 textureColor = texture2D(uTexture,vTexCoord);
    col = col * textureColor.rgb;
  }
  gl_FragColor = vec4(col, 1.0);
}
`;

////////////////////////////////////////////////////////////////////////////////
// EXTRA CREDIT: change DEF_INPUT to create something interesting!
////////////////////////////////////////////////////////////////////////////////
const DEF_INPUT = [
  
  "c,myCamera,perspective,5,5,5,0,0,0,0,1,0;",
  "l,myLight,point,0,5,0,2,2,2;",
  "p,unitCube,cube;",
  "p,unitSphere,sphere,20,20;",
  "m,bluDiceMat,0,0,0.3,0,0,0.7,1,1,1,15,dice.jpg;",
  "m,blackDiceMat,0,0,0,0,0,0.7,1,1,1,15,dice.jpg;",
  "m,globeMat,0.3,0.3,0.3,0.7,0.7,0.7,1,1,1,5,globe.jpg;",
  "o,rd,unitCube,bluDiceMat;",
  "o,ld,unitCube,bluDiceMat;",
  "o,hg,unitSphere,blackDiceMat;",
  "o,hd,unitCube,blackDiceMat;",
  "o,gh,unitSphere,globeMat;",
  "o,gb,unitSphere,globeMat;",
  "o,gf,unitSphere,globeMat;",
  "X,ld,Rz,90;X,ld,Rx,90;X,ld,S,0.1,0.1,0.9;X,ld,T,-2,-1,0;;",
  "X,rd,S,0.9,0.1,0.1;X,rd,Rx,90;X,rd,T,0,-1,-2.2;",
  "X,gh,S,0.5,0.5,0.5;X,gh,Rx,90;X,gh,Ry,-150;X,gh,T,0,1.5,0;",
  "X,gb,Ry,40;X,gb,Rx,-20;",
  "X,gf,S,1.5,1.5,1.5;X,gf,Rx,90;X,gf,Ry,-150;X,gf,T,0,-2,0;",
  "X,hg,S,0.8,0.1,0.1;X,hg,T,0,2,0;",
  "X,hd,Rx,-20;X,hd,S,0.3,0.4,0.3;X,hd,T,0.15,2.5,0;",

  // "c,myCamera,perspective,5,5,5,0,0,0,0,1,0;",
  // "l,myLight,point,0,5,0,2,2,2;",
  // "p,unitCube,cube;",
  // "p,unitSphere,sphere,20,20;",
  // "m,redDiceMat,0.3,0,0,0.7,0,0,1,1,1,15,dice.jpg;",
  // "m,grnDiceMat,0,0.3,0,0,0.7,0,1,1,1,15,dice.jpg;",
  // "m,bluDiceMat,0,0,0.3,0,0,0.7,1,1,1,15,dice.jpg;",
  // "m,globeMat,0.3,0.3,0.3,0.7,0.7,0.7,1,1,1,5,globe.jpg;",
  // "o,rd,unitCube,redDiceMat;",
  // "o,gd,unitCube,grnDiceMat;",
  // "o,bd,unitCube,bluDiceMat;",
  // "o,gl,unitSphere,globeMat;",
  // "X,rd,Rz,75;X,rd,Rx,90;X,rd,S,0.5,0.5,0.5;X,rd,T,-1,0,2;",
  // "X,gd,Ry,45;X,gd,S,0.5,0.5,0.5;X,gd,T,2,0,2;",
  // "X,bd,S,0.5,0.5,0.5;X,bd,Rx,90;X,bd,T,2,0,-1;",
  // "X,gl,S,1.5,1.5,1.5;X,gl,Rx,90;X,gl,Ry,-150;X,gl,T,0,1.5,0;",
].join("\n");

// DO NOT CHANGE ANYTHING BELOW HERE
export { Parser, Scene, Renderer, DEF_INPUT };
