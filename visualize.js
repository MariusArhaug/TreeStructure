class Node {
  fixedSize = 7.5;
  ctx = ctx;
  constructor({id, parent_id, depth, children}) {
    this.id = id;
    this.parent_id = parent_id;
    this.depth = depth;
    this.children = children;

    this.radius = this.fixedSize + (this.fixedSize * this.children.length)/4;
    this.x = canvas.width/2;
    this.y = 100;
  }
  *[Symbol.iterator]() {
    for (let child of this.children) {
      yield child;
    }
  }
  updateCoordinates(x, y) {
    this.x = x;
    this.y = y;
  }

  changeCanvas(ctx) {
    this.ctx = ctx;
  }

  drawNode() {
    ctx.beginPath();
    ctx.fillStyle = '#021225';
    ctx.arc(this.x, this.y, this.radius, 0, 2 * Math.PI, false);
    ctx.fill()
    ctx.stroke();
    ctx.closePath();
  }

  drawEdge(toX, toY) {   
    ctx.beginPath();
    ctx.fillStyle = 'gray';
    ctx.moveTo(this.x, this.y);
    ctx.lineTo(toX, toY);
    ctx.stroke(); 
    ctx.closePath();
  };

  drawID() {
    ctx.beginPath();
    ctx.font = 'bold 10pt Calibri';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fill()
    ctx.beginPath();
    ctx.fillStyle = "white";
    ctx.fillText(this.id, this.x, this.y);
  }
}

let canvas;
let ctx;
/**
 * Visualize a nested jsonObj into a tree with drawTree function
 * @param {*} jsonObj nested jsonObj read from json file/API. 
 */
export default function visualize(jsonObj) {
  canvas = document.getElementById('canvas');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  ctx = canvas.getContext('2d');
  let root = new Node(jsonObj)
  root.drawNode();
  drawTree(root);
  root.drawID();
}

/**
 * Draw a tree on canvas from a given root Node
 * Split opp root's children in two halfes,
 * so that they can be drawn from center then +/- depending on left and right.
 * @param {*} root Root of the tree
 * @returns undefined. 
 */
function drawTree(root) {
  if (root.children.length === 0) {
    return;
  }
  let children = root.children;
  const half = Math.ceil(children.length / 2);
  let firstHalf = children.splice(0, half);
  let secondHalf = children.splice(-half);
  
  firstHalf = drawNodeAndEdge(root, firstHalf, true);
  secondHalf = drawNodeAndEdge(root, secondHalf, false);
  children = [...[...firstHalf, ...secondHalf]];
  for (let childNode of children) {
    drawTree(childNode);
    childNode.drawID();
  }
}
/**
 * Draw nodes in nodeArray aswell as edge from drawn node to root node. 
 * @param {*} root Root/parent of the nodeArray
 * @param {*} nodeArray array of children nodes of root
 * @param {*} left decide to draw nodes either to the left or right. 
 * @returns 
 */
const drawNodeAndEdge = (root, nodeArray, left) => {
  return nodeArray.map((node, i) => {
    node = new Node(node);
    const x = root.x + (left ? -1 : 1 ) * (20 + node.radius*2)*(i + (left ? 0 : 1))*(1.5 * nodeArray.length * 0.5 * node.depth);
    const y = root.y + (50 + node.radius*2) * 0.2 * node.depth;
    node.updateCoordinates(x, y);
    node.drawNode();
    node.drawEdge(root.x , root.y);
    return node;
  })
}

function findParentNode(nodeList, node) {
  return nodeList.filter(o => o.id === node.parent_id)[0];
}

function maxDepth(nodeList) {
  return Math.max(...nodeList.map(node => node.depth))
}

function flattenJSON(root, nodes=[]) {
  nodes.push(root)
  if (root.children.length === 0) {
    return nodes
  }
  for (let child of root) {
    const node = new Node(child)
    flattenJSON(node, nodes)
  }
  return nodes;
}