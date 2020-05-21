import React, { Component } from "react";
import ReactDOM from "react-dom";

const key_names = ["C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B"];
const guitar_strings = [4, 9, 2, 7, 11, 4];

const ionian_intervals = [2, 2, 1, 2, 2, 2, 1];
const major_modes = ["Ionian (Major)", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian (Minor)", "Locrian"];

var scales = {
  "Harmonic Minor": {"0": "1", "2": "2", "3": "3", "5": "4", "7": "5", "8": "6", "11": "7"},
  "Pentatonic Major": {"0": "1", "2": "2", "4": "3", "7": "5", "9": "6"},
  "Pentatonic Minor": {"0": "1", "3": "3", "5": "4", "7": "5", "10": "7"},
  "Blues": {"0": "1", "3": "3", "5": "4", "6": "#", "7": "5", "10": "7"}
};

const scale_list = major_modes.concat([...Object.keys(scales)]);

for (var i in major_modes) {
  var scale = {"0": "1"};
  var current_note = 0;
  for (var j in ionian_intervals) {
    var interval = ionian_intervals[(i + j) % 7];
    current_note += interval;
    scale[current_note] = parseInt(j) + 2;
  }

  scales[major_modes[i]] = scale;
}

const scale_position_colors = [null, "#ff0000", "#0000ff", "#ff00ff", "#007700", "#ff7700", "#9900ff", "#bb7700"];
scale_position_colors["#"] = "#777777";

var positions = [];
for (var string_index in guitar_strings) {
  for (var fret of [...Array(13).keys()]) {
    positions.push({string_index: string_index, fret: fret});
  }
}

class Guitar extends Component {
  state = {
    key: 0,
    mode: major_modes[0]
  }

  keychange(event) {
    this.setState({key: parseInt(event.target.value)});
  }

  modechange(event) {
    this.setState({mode: event.target.value});
  }

  render() {
    return (
      <div>
        <div>
          <select name="key" id="keyselect" onChange={this.keychange.bind(this)}>
          {key_names.map((name, number) =>
            <option value={number} key={number}>{name}</option>
          )}
          </select>
        </div>

        <div>
          <select name="mode" id="modeselect" onChange={this.modechange.bind(this)}>
          {scale_list.map((mode) =>
            <option value={mode} key={mode}>{mode}</option>
          )}
          </select>
        </div>

        <div style={{backgroundColor: "#9c7714", width: "36vh", height: "120vh", position: "absolute", left: "calc(50vw - 18vh)"}}>
          {[...Array(13).keys()].map((fret) =>
            <div className="fret" key={fret}
              style={{backgroundColor: "#999999", width: "100%", height: "1vh", left: "0", top: (241 - Math.pow(.946, fret)*240) + "vh", position: "absolute"}}/>
          )}

          {guitar_strings.map((note, index) =>
            <div className="string" key={index}
              style={{backgroundColor: "#b5a642", width: ".5vh", height: "120vh", left: (6*index + 2.75) + "vh", top: "0", position: "absolute"}}/>
          )}


          {[3, 5, 7, 9].map((fret) =>
            <div className="guidedot" key={fret}
              style={{backgroundColor: "#000000", width: "2vh", "height": "2vh", left: "17vh",
                      top: (241 - Math.pow(.946, (fret - .55))*240) + "vh", position: "absolute", borderRadius: "1vh"}}/>
          )}
          <div id="left-octave-dot"
            style={{backgroundColor: "#000000", width: "2vh", "height": "2vh", left: "15.5vh",
                    top: (241 - Math.pow(.946, 11.45)*240) + "vh", position: "absolute", borderRadius: "1vh"}}/>
          <div id="right-octave-dot"
            style={{backgroundColor: "#000000", width: "2vh", "height": "2vh", left: "18.5vh",
                    top: (241 - Math.pow(.946, 11.45)*240) + "vh", position: "absolute", borderRadius: "1vh"}}/>


          {positions.map((pos, index) => {
            var note = (12 + guitar_strings[pos.string_index]+ pos.fret - this.state.key) % 12;
            if (note in scales[this.state.mode]) {
                var scale_position = scales[this.state.mode][note];
                return <div className="finger-dot" key={index}
                            style={{backgroundColor: scale_position_colors[scale_position],
                            color: "#ffffff", fontWeight: 900, textAlign: "center", fontFamily: "Arial",
                            width: "3vh", "height": "3vh", left: (6*pos.string_index + 1.5) + "vh",
                            top: (240 - Math.pow(.946, pos.fret)*240) + "vh", fontSize: "2vh",
                            position: "absolute", borderRadius: "1.5vh"}}>{scale_position}</div>;
            } else { return null; }
          })}

        </div>
      </div>
    );
  }
}

export default Guitar;
