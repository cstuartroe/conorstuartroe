import React, {Component, CSSProperties} from "react";
import { range } from "./utils";

const key_names: {[edo: number]: string[]} = {
  12: ["E", "F", "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B", "C", "C#/Db", "D", "D#/Eb"],
  15: ["E", "F", "F#", "Gb", "G", "G#/Ab", "A", "A#", "Bb", "B", "C", "C#/Db", "D", "D#", "Eb"],
  22: range(22).map(n => n + ""),
};

const guitar_strings: {[edo: number]: number[]} = {
  12: [0, 5, 10, 3, 7, 0],
  15: [0, 6, 12, 3, 9, 0],
  22: [0, 9, 18, 5, 13, 0],
};

type Scale = {[degree: string]: string};

const scales: { [edo: number]: { [name: string]: Scale } } = {
  12: {
    "Harmonic Minor": {"0": "1", "2": "2", "3": "3", "5": "4", "7": "5", "8": "6", "11": "7"},
    "Pentatonic Major": {"0": "1", "2": "2", "4": "3", "7": "5", "9": "6"},
    "Pentatonic Minor": {"0": "1", "3": "3", "5": "4", "7": "5", "10": "7"},
    "Blues": {"0": "1", "3": "3", "5": "4", "6": "#", "7": "5", "10": "7"},
  },
  15: {
    "Half-Mixolydian": {"0": "1", "2": "2", "5": "3", "6": "4", "9": "5", "11": "6", "13": "7"},
  },
  22: {
    "Major Bent": {"0": "1", "4": "2", "7": "3", "9": "4", "13": "5", "16": "6", "20": "7"},
    "Minor Bent": {"0": "1", "3": "2", "7": "3", "9": "4", "13": "5", "16": "6", "20": "7"},
    "Neutral Bent": {"0": "1", "3": "2", "7": "3", "9": "4", "13": "5", "16": "6", "19": "7"},
    "Major Septimal": {"0": "1", "4": "2", "7": "3", "9": "4", "13": "5", "17": "6", "20": "7"},
    "Minor Septimal": {"0": "1", "3": "2", "7": "3", "9": "4", "12": "5", "16": "6", "20": "7"},
    "Balanced Septimal": {"0": "1", "4": "2", "7": "3", "9": "4", "13": "5", "17": "6", "19": "7"},
  }
};

const ionian_intervals: {[edo: number]: number[]} = {
  12: [2, 2, 1, 2, 2, 2, 1],
  15: [3, 2, 1, 3, 2, 3, 1],
  22: [4, 4, 1, 4, 4, 4, 1],
}

const diatonic_modes = ["Ionian (Major)", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian (Minor)", "Locrian"];

for (let i = 0; i < 7; i++) {
  for (const edo of Object.keys(scales)) {
    const scale: Scale = {"0": "1"};
    let current_note = 0;

    for (let j = 0; j < 7; j++) {
      current_note += ionian_intervals[parseInt(edo)][(i + j) % 7];
      scale[current_note] = String(j + 2);
    }

    scales[parseInt(edo)][diatonic_modes[i]] = scale;
  }
}

const scale_position_colors : {[degree: string]: string} = {
  1: "#ff0000",
  2: "#0000ff",
  3: "#ff00ff",
  4: "#007700",
  5: "#ff7700",
  6: "#9900ff",
  7: "#bb7700",
  '#': "#777777",
};

type Position = {string_index: number, fret: number};

type Props = {
  edo: number;
}

type State = {
  key: number,
  scale_name: string,
}

class Guitar extends Component<Props, State> {
  private positions: Position[];
  private readonly frets: number[];

  constructor(props: Props) {
    super(props);

    this.state = {
      key: 0,
      scale_name: diatonic_modes[0]
    }

    this.frets = range(Math.floor(props.edo * 1.4));
    this.positions = [];

    for (const string_index of range(guitar_strings[props.edo].length)) {
      for (const fret of this.frets) {
       this.positions.push({string_index: string_index, fret: fret});
      }
    }
  }

  keychange(event: React.ChangeEvent<HTMLSelectElement>) {
    this.setState({key: parseInt(event.target.value)});
  }

  modechange(event: React.ChangeEvent<HTMLSelectElement>) {
    this.setState({scale_name: event.target.value});
  }

  render() {
    const { edo } = this.props;

    const neckHeight = 160

    const getHeight = (steps: number, extra: number = 0) => {
      return (neckHeight + 1 - Math.pow(2, -steps/edo)*neckHeight + extra) + "vh"
    }

    const dotStyle: CSSProperties = {
      backgroundColor: "#000000",
      width: "2vh",
      height: "2vh",
      position: "absolute",
      borderRadius: "1vh",
    };

    return (
      <div>
        <div>
          <select name="key" id="keyselect" onChange={this.keychange.bind(this)}>
          {key_names[edo].map((name, number) =>
            <option value={number} key={number}>{name}</option>
          )}
          </select>
        </div>

        <div>
          <select name="mode" id="modeselect" value={this.state.scale_name} onChange={this.modechange.bind(this)}>
          {Object.keys(scales[edo]).map((mode) =>
            <option value={mode} key={mode}>{mode}</option>
          )}
          </select>
        </div>

        <div style={{
          backgroundColor: "#9c7714",
          width: "36vh",
          height: neckHeight*.62 + "vh",
          position: "absolute",
          left: "calc(50vw - 18vh)",
        }}>

          {this.frets.map((fret) =>
            <div className="fret" key={fret}
              style={{
                backgroundColor: "#999999",
                width: "100%",
                height: "1vh",
                left: "0",
                top: getHeight(fret),
                position: "absolute",
              }}/>
          )}

          {guitar_strings[edo].map((note, index) =>
            <div className="string" key={index}
              style={{
                backgroundColor: "#b5a642",
                width: ".5vh",
                height: neckHeight*.62 + "vh",
                left: (6*index + 2.75) + "vh",
                top: "0",
                position: "absolute",
              }}/>
          )}


          {[3, 5, 7, 9].map((fret) =>
            <div className="guidedot" key={fret}
              style={{
                ...dotStyle,
                left: "17vh",
                top: getHeight(fret - .5, -1),
              }}/>
          )}

          <div id="left-octave-dot"
            style={{
              ...dotStyle,
              left: "15.5vh",
              top: getHeight(edo - .5, -1),
            }}/>

          <div id="right-octave-dot"
            style={{
              ...dotStyle,
              left: "18.5vh",
              top: getHeight(edo - .5, -1),
            }}/>


          {this.positions.map((pos, index) => {
            const note = (edo + guitar_strings[edo][pos.string_index] + pos.fret - this.state.key) % edo;

            if (note in scales[edo][this.state.scale_name]) {
              const scale_position = scales[edo][this.state.scale_name][note];

              return <div
                className="finger-dot" key={index}
                style={{
                  backgroundColor: scale_position_colors[scale_position],
                  color: "#ffffff",
                  fontWeight: 900,
                  textAlign: "center",
                  fontFamily: "Arial",
                  width: "3vh",
                  height: "3vh",
                  left: (6*pos.string_index + 1.5) + "vh",
                  top: getHeight(pos.fret, -1),
                  fontSize: "2vh",
                  position: "absolute",
                  borderRadius: "1.5vh",
                }}>
                {scale_position}
              </div>;
            } else {
              return null;
            }
          })}

        </div>
      </div>
    );
  }
}

export default Guitar;
