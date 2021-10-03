import React, { Component } from "react";

const vh = window.innerHeight;
const vw = window.innerWidth;

const pipe_width = 10;
const pipe_border = 2;
const pipe_color = '#757f8a';
const section_length = Math.floor((vh + vw)/100)*2 + 10;
const grid_height = Math.floor(vh / section_length) + 1;
const grid_width = Math.floor(vw / section_length) + 1;

const node_frequency = .13;
const margin = Math.floor(section_length/2);
const node_radius = 10;
const particle_radius = 5;
const frame_interval = 25;

const pixels_x = (grid_x: number) => grid_x * section_length + margin;
const pixels_y = (grid_y: number) => grid_y * section_length + margin;

type Direction = "up" | "down" | "left" | "right";
const directions: Direction[] = ["up", "down", "left", "right"];


type Vector = {x: number, y: number};

const directionVectors: {[key in Direction]: Vector} = {
  "up": {x: 0, y: -1},
  "down": {x: 0, y: 1},
  "left": {x: -1, y: 0},
  "right": {x: 1, y: 0},
}

const magnitude = (v: Vector): number => Math.sqrt(v.x ** 2 + v.y ** 2);

const unitize = (v: Vector): Vector => {
  const mag = magnitude(v);
  return {x: v.x/mag, y: v.y/mag};
}

const evaluateDirection = (v: Vector): (Direction | undefined) => {
  const u = unitize(v);
  for (const d of directions) {
    if (u.x === directionVectors[d].x && u.y === directionVectors[d].y) {
      return d;
    }
  }
}

const opposites: {[key in Direction]: Direction} = {
  "up": "down",
  "left": "right",
  "down": "up",
  "right": "left",
}

type Node = {
  x: number,
  y: number,
  pipes: {[key in Direction]?: Pipe}
}

function pipelist(n: Node) {
  return [n.pipes.up, n.pipes.down, n.pipes.left, n.pipes.right].filter(p => p !== undefined);
}

function pastEdge({x, y}: Vector): boolean {
  return x < 0 || y < 0 || x >= grid_width || y >= grid_height;
}

type Particle = {
  position: number,
  direction: Direction,
  hue: number,
  ticks_since_spawn: number,
  speed: number,
}

function putParticle(node: Node, direction: Direction, par: Particle) {
  const nextPipe = node.pipes[direction];

  if (nextPipe === undefined) {
    throw "Undefined pipe";
  }

  nextPipe.particles.push({
    position: ['up', 'left'].includes(direction) ? nextPipe.length() : 0,
    direction: direction,
    hue: par.hue,
    ticks_since_spawn: par.ticks_since_spawn,
    speed: par.speed,
  })
}

function closestNode(pipe: Pipe, par: Particle) {
  const dist0 = par.position;
  const dist1 = pipe.length() - par.position;

  if (dist0 < dist1) {
    return {node: pipe.nodes[0], distance: dist0};
  } else {
      return {node: pipe.nodes[1], distance: dist1};
  }
}

class Pipe {
  public nodes: Node[];
  public particles: Particle[];

  constructor(nodes: Node[]) {
    if (nodes.length !== 2) {
      throw "Incorrect number of end nodes for pipe";
    }

    const same_row = nodes[0].x === nodes[1].x;
    const same_column = nodes[0].y === nodes[1].y;

    if (same_row && same_column) {
      throw "Nodes are in the same place";
    } else if ((!same_row) && (!same_column)) {
      throw "Nodes are at a diagonal";
    }

    this.nodes = nodes;
    this.particles = [];
  }

  numSections = () => (Math.abs(this.nodes[1].x - this.nodes[0].x) + Math.abs(this.nodes[1].y - this.nodes[0].y));

  length = () => this.numSections() * section_length;

  moveParticles = (): number => {
    let keptParticles: Particle[] = [];
    let droppedParticles: number = 0;

    for (const p of this.particles) {
      const dv = directionVectors[p.direction];
      p.position += (dv.x + dv.y)*p.speed;
      p.ticks_since_spawn++;

      let {node: passingNode, distance} = closestNode(this, p);

      if (distance > 0) {
        keptParticles.push(p);
        continue;
      }

      if (pastEdge(passingNode)) {
        droppedParticles++;
        continue;
      }

      const possibleNextDirections = directions.filter(dir => (
        passingNode.pipes[dir] !== undefined &&
          dir !== opposites[p.direction]
      ));

      const nextDirection = possibleNextDirections[randint(possibleNextDirections.length)];
      putParticle(passingNode, nextDirection, p);
    }

    this.particles = keptParticles;
    return droppedParticles;
  }
}

function connectNodes(node1: Node, node2: Node) {
  const pipe = new Pipe([node1, node2].sort((a, b) => a.x + a.y - b.x - b.y));
  const dir = evaluateDirection({x: node2.x - node1.x, y: node2.y - node1.y});

  if (dir == undefined) {
    throw "Cannot connect pipes at a diagonal";
  }

  node1.pipes[dir] = pipe;
  node2.pipes[opposites[dir]] = pipe;

  return pipe;
}

const randint = (n: number) => Math.floor(Math.random() * n);

const pipePixels = (pipe: Pipe) => ({
  x1: pixels_x(pipe.nodes[0].x),
  y1: pixels_y(pipe.nodes[0].y),
  x2: pixels_x(pipe.nodes[1].x),
  y2: pixels_y(pipe.nodes[1].y),
})

class PipesManager {
  private canvas: any;
  private nodes: Node[];
  private edgeNodes: Node[];
  private pipes: Pipe[];
  private numParticles: number;
  private ticks: number;
  private last_particle_spawn: number;

  constructor(canvas: HTMLElement) {
    this.canvas = canvas;
    this.nodes = this.generateNodes();
    this.edgeNodes = [];
    this.pipes = this.generatePipes();
    this.numParticles = 0;
    this.ticks = 0;
    this.last_particle_spawn = -1000;

    setInterval(() => {
      this.spawnParticles();
      this.pipes.forEach(p => {
        this.numParticles -= p.moveParticles();
      });
      this.drawPipes();
      this.ticks++;
    }, frame_interval);
  }

  generateNodes = (): Node[] => {
    const nodes: Node[] = [];

    while (nodes.length < (grid_width*grid_height) * node_frequency) {
      const x = randint(grid_width), y = randint(grid_height);

      if (!nodes.some(n => n.x === x && n.y === y)) {
        nodes.push({x, y, pipes: {}});
      }
    }

    return nodes;
  }

  generatePipes = (): Pipe[] => {
    const pipes: Pipe[] = [];

    for (const node of this.nodes) {
      for (const dir of directions) {
        if (node.pipes[dir] === undefined) {
          let {x, y} = node;

          while (!pastEdge({x, y})) {
            x += directionVectors[dir].x;
            y += directionVectors[dir].y;

            const matching_node: Node | undefined = this.nodes.find(n => n.x == x && n.y == y);

            if (matching_node !== undefined) {
              if (matching_node.pipes[opposites[dir]] !== undefined) {
                throw "Mismatched pipe";
              }

              const pipe = connectNodes(node, matching_node);
              pipes.push(pipe);
              break;
            }
          }
        }
      }

      while (pipelist(node).length < 2) {
        const dir = directions[randint(directions.length)];

        if (node.pipes[dir] === undefined) {
          const dv = directionVectors[dir];

          let {x, y} = node;
          while (!pastEdge({x, y})) {
            x += dv.x;
            y += dv.y;
          }

          const edgeNode: Node = {
            x,
            y,
            pipes: {},
          };

          this.edgeNodes.push(edgeNode);

          const pipe = connectNodes(node, edgeNode);
          pipes.push(pipe);
        }
      }
    }

    return pipes;
  }

  spawnParticles = () => {
    if (this.ticks - this.last_particle_spawn < (section_length/2)) {
      return;
    }

    this.edgeNodes.forEach(node => {
      if (Math.random() < (2/(this.numParticles**.5 + 1))) {
        const par: Particle = {
          hue: 140 + randint(220), // green, blue, purple, pink, red; skip oranges and yellows
          ticks_since_spawn: 0,
          direction: "up",
          position: 0,
          speed: 1 + Math.random()*2,
        }

        putParticle(node, directions.filter(d => node.pipes[d] !== undefined)[0], par);
        this.numParticles++;
        this.last_particle_spawn = this.ticks;
      }
    });
  }

  drawNodes = () => {
    const { canvas, nodes } = this;

    if (canvas.getContext) {
      const ctx = canvas.getContext('2d');
      for (const node of nodes) {
        ctx.beginPath();
        ctx.arc(pixels_x(node.x), pixels_y(node.y), node_radius, 0, Math.PI*2);
        ctx.fill();
      }
    }
  }

  drawPipes = () => {
    const { canvas, pipes, nodes } = this;

    if (canvas.getContext) {
      const ctx = canvas.getContext('2d');

      const cornerParticles: [Pipe, Particle][] = [];

      for (const pipe of pipes) {
        const {x1, y1, x2, y2} = pipePixels(pipe);

        ctx.fillStyle = pipe_color;

        ctx.fillRect(
          x1 - pipe_width / 2 - pipe_border,
          y1 - pipe_width / 2 - pipe_border,
          (x2 - x1) + pipe_width + pipe_border * 2,
          (y2 - y1) + pipe_width + pipe_border * 2,
        );

        ctx.clearRect(
          x1 - pipe_width/2,
          y1 - pipe_width/2,
          (x2 - x1) + pipe_width,
          (y2 - y1) + pipe_width,
        );

        for (const par of pipe.particles) {
          let { distance } = closestNode(pipe, par);
          if (distance > section_length/2) {
            this.drawParticle(ctx, pipe, par);
          } else {
            cornerParticles.push([pipe, par]);
          }
        }
      }

      for (const node of nodes) {
        for (const dir of directions) {
          if (node.pipes[dir] !== undefined) {
            const dv = directionVectors[dir];

            ctx.clearRect(
              pixels_x(node.x) - pipe_width/2 + dv.x*pipe_border*2,
              pixels_y(node.y) - pipe_width/2 + dv.y*pipe_border*2,
              pipe_width + dv.x*pipe_border*2,
              pipe_width + dv.y*pipe_border*2,
            )
          }
        }
      }

      for (const [pipe, par] of cornerParticles) {
        this.drawParticle(ctx, pipe, par);
      }
    }
  }

  drawParticle = (ctx: any, pipe: Pipe, par: Particle) => {
    const {x1, y1} = pipePixels(pipe);

    const dv = directionVectors[par.direction];

    const lightness = Math.round(Math.sin(par.ticks_since_spawn/15)*10) + 65;

    ctx.fillStyle = `hsl(${par.hue}, 100%, ${lightness}%)`;

    ctx.beginPath()
    ctx.arc(
      x1 + par.position*Math.abs(dv.x),
      y1 + par.position*Math.abs(dv.y),
      particle_radius,
      0,
      Math.PI*2,
    )
    ctx.fill();
  }
}


type Props = {};

type State = {
  manager?: PipesManager,
};


export default class Pipes extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
  }

  componentDidMount() {
    const canvas = document.getElementById('pipes');

    if (canvas !== null) {
      this.setState({
        manager: new PipesManager(canvas),
      });
    }
  }

  render() {
    return <div style={{position: 'absolute', top: 0, left: 0, width: '100vw', height: '100vh', overflow: 'hidden'}}>
      <canvas
        id={'pipes'}
        width={section_length*(grid_width-1) + (margin*2)}
        height={section_length*(grid_height-1) + (margin*2)}
      />
    </div>;
  }
}