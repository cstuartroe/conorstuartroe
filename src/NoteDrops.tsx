import React, { Component } from "react";

const vh = window.innerHeight;
const vw = window.innerWidth;

type RawMidiMessage = {
  data: [number, number, number],
  timeStamp: number,
}

type MidiInputDevice = {
  onmidimessage: (m: RawMidiMessage) => void
};

type MidiConnection = {
  inputs: MidiInputDevice[],
  onstatechange: () => void,
}

function randInt(n: number): number {
  return Math.floor(Math.random()*n);
}

type Props = {};

type Dot = {
  x: number,
  y: number,
  color: number,
}

type State = {
  dots: Dot[],
  inputs: any[],
  canvas: any,
};

export default class NoteDrops extends Component<Props, State> {
  constructor(props: Props) {
    super(props);

    this.state = {
      dots: [],
      inputs: [],
      canvas: undefined,
    }
  }

  componentDidMount() {
    const canvas = document.getElementById('drops');

    if (canvas !== null) {
      //@ts-ignore
      navigator.requestMIDIAccess()
        .then((a: MidiConnection) => {
          a.onstatechange = () => {
            this.setState({inputs: a.inputs});
            a.inputs.forEach(input => {
              input.onmidimessage = this.onMidiMessage.bind(this);
            });
          }
          a.onstatechange();
        })
        // .catch((_: any) => this.setState({connectionError: true}));
    }

    this.setState({canvas});

    setInterval(() => {
      this.clearCanvas();
      this.moveParticles();
      this.drawDots();
    }, 10);
  }

  clearCanvas() {
    const ctx = this.state.canvas.getContext('2d');

    ctx.fillStyle = '#757f8a';

    ctx.fillRect(
      0,
      0,
      vw,
      vh,
    );
  }

  moveParticles() {
    const dots = this.state.dots.map((dot) => ({
      ...dot,
      y: dot.y + 1,
    })).filter(dot => dot.y < vh);

    this.setState({dots});
  }

  drawDots() {
    this.state.dots.forEach(dot => {
      this.drawParticle(dot);
    });
  }

  onMidiMessage(message: any) {
    console.log(message);
    if (message.data[0] === 144) {
      this.setState({
        dots: this.state.dots.concat([{
          x: randInt(vw),
          y: 0,
          color: randInt(255),
        }])
      });
    }
  }

  render() {
    return <div style={{position: 'absolute', top: 0, left: 0, width: '100vw', height: '100vh', overflow: 'hidden'}}>
      <canvas
        id={'drops'}
        width={vw}
        height={vh}
      />
    </div>;
  }

  drawParticle = (dot: Dot) => {
    const ctx = this.state.canvas.getContext('2d');

    const swell = Math.round(Math.sin(dot.y/15) * 10);
    const lightness = swell + 65;
    const radius = 8 + (swell/10);

    ctx.fillStyle = `hsl(${dot.color}, 100%, ${lightness}%)`;

    ctx.beginPath()
    ctx.arc(
      dot.x,
      dot.y,
      radius,
      0,
      Math.PI*2,
    )
    ctx.fill();
  }
}