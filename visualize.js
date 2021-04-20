class Node {
  fixedSize = 7.5;
  constructor({id, parent_id, depth, children}) {
    this.id = id;
    this.parent_id = parent_id;
    this.depth = depth;
    this.children = children;
    this.radius = this.fixedSize + (this.fixedSize * this.children.length)/5;
    this.x;
    this.y;
  }
  *[Symbol.iterator]() {
    for (let child of this.children) {
      yield child;
    }
  }
  drawNode(x, y) {
    this.x = x;
    this.y = y;
    ctx.beginPath();
    ctx.fillStyle = '#021225';
    ctx.arc(this.x, this.y, this.radius, 0, 2 * Math.PI, false);
    ctx.font = 'bold 20pt Calibri';
    ctx.fill()
    ctx.beginPath();
    ctx.fillStyle = "white";
    ctx.fillText(this.id, 40, 100);
    ctx.fill()
    ctx.stroke();
    ctx.closePath();
  }

  drawEdge(toX, toY) {   
    const moveToX = this.x;
    const moveToY = this.y + this.radius;
    const lineToX = toX;
    const lineToY = toY - this.radius;
    ctx.beginPath();
    ctx.moveTo(moveToX, moveToY);
    ctx.lineTo(lineToX, lineToY);
    ctx.stroke(); 
    ctx.closePath();
  };
}

let canvas;
let ctx;
export default function visualize(JSONRoot) {
  canvas = document.getElementById('canvas');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  ctx = canvas.getContext('2d');
  const root = new Node(JSONRoot);
  mapJSON(root);
  let nodes = flattenJSON(root);
  drawTree(root, nodes);
  
}

function drawTree(root, nodes) {
  const rootX = canvas.width/2
  const rootY = 100
  root.drawNode(rootX, rootY, ctx);
  const max = maxDepth(nodes)
 
  for (let i = 2; i <= max; i++) {
    let nodesAtDepth = nodes.filter(node => node.depth === i); 

    const half = Math.ceil(nodesAtDepth.length / 2);
    const firstHalf = nodesAtDepth.splice(0, half);
    const secondHalf = nodesAtDepth.splice(-half);

    firstHalf.map((node, j) => {
      const parent = findParentNode(nodes, node);
      const childX = parent.x - 40*j < 0 ? 0 : parent.x - 40*j; 
      node.drawNode(childX,  parent.y + 60 + node.radius);
      node.drawEdge(parent.x, parent.y);
    });
    secondHalf.map((node, j) => {
      const parent = findParentNode(nodes, node);
      const childX = parent.x + 20*(j+1) < 0 ? 0 : parent.x + 20*(j+1);
      node.drawNode(childX, parent.y + 60 + node.radius);
      node.drawEdge(parent.x, parent.y);
      console.log(parent);
    })
    
  }
}

window.addEventListener('resize', () => resizeCanvas()) 

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}

function mapJSON(root) {
  if (root.children.length === 0) {
    return;
  }
  const children = []
  for (let child of root) {
    child = new Node(child)
    children.push(child)
    mapJSON(child)
  }
  root.children = children;
}

function drawEdges(root) {
  if (root.children.length === 0) {
    return;
  }
  for (let childNode of root) {
    childNode.drawEdge(root.x, root.y);
    drawEdges(childNode)
  }
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