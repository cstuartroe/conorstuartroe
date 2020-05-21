import React, { Component } from "react";
import ReactDOM from "react-dom";

const ionian_intervals = [2, 2, 1, 2, 2, 2, 1];
const harmonic_minor_intervals = [2, 1, 2, 2, 1, 3, 1];
const key_names = ["C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B"];
const major_modes = ["Ionian (Major)", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian (Minor)", "Locrian"];
const guitar_strings = [4, 9, 2, 7, 11, 4];
const scale_position_colors = ["#ff0000", "#0000ff", "#ff00ff", "#007700", "#ff7700", "#777700", "#7700ff"];

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
    var included_notes = [this.state.key];
    if (major_modes.includes(this.state.mode)) {
      var rot = major_modes.indexOf(this.state.mode);
      var rotated_intervals = ionian_intervals.slice(rot).concat(ionian_intervals.slice(0, rot));
      for (var interval of rotated_intervals) {
        included_notes.push((included_notes[included_notes.length - 1] + interval) % 12);
      }
    }

    var s = "";
    for (var i of included_notes) {
      s += key_names[i] + " ";
    }

    var positions = [];
    for (var string_index in guitar_strings) {
      for (var fret of [...Array(13).keys()]) {
        positions.push({string_index: string_index, fret: fret});
      }
    }

    var fretboard = <div style={{backgroundColor: "#9c7714", width: "100%", height: "100vh", position: "absolute"}}>
      {guitar_strings.map((note, index) =>
        <div className="string" key={index}
          style={{backgroundColor: "#000000", width: "4px", height: "100%", left: (16.7*index + 8.3) + "%", top: "0", position: "absolute"}}/>
      )}

      {[...Array(13).keys()].map((fret) =>
        <div className="fret" key={fret}
          style={{backgroundColor: "#000000", width: "100%", height: "6px", left: "0", top: (201 - Math.pow(.946, fret)*200) + "vh", position: "absolute"}}/>
      )}

      <div id="five-dot"
        style={{backgroundColor: "#000000", width: "2vw", "height": "2vw", left: "48.5%", top: "44vh", position: "absolute", borderRadius: "1vw"}}/>
      <div id="seven-dot"
        style={{backgroundColor: "#000000", width: "2vw", "height": "2vw", left: "48.5%", top: "61vh", position: "absolute", borderRadius: "1vw"}}/>
      <div id="left-octave-dot"
        style={{backgroundColor: "#000000", width: "2vw", "height": "2vw", left: "44.5%", top: "95vh", position: "absolute", borderRadius: "1vw"}}/>
      <div id="right-octave-dot"
        style={{backgroundColor: "#000000", width: "2vw", "height": "2vw", left: "52.5%", top: "95vh", position: "absolute", borderRadius: "1vw"}}/>


      {positions.map((pos, index) => {
        var note = guitar_strings[pos.string_index];
        if (included_notes.includes((note + pos.fret) % 12)) {
            var scale_position = included_notes.indexOf((note + pos.fret) % 12);
            return <div className="finger-dot" key={pos.string_index*13 + pos.fret}
                        style={{backgroundColor: "#ffffff", border: "4px solid " + scale_position_colors[scale_position],
                        color: scale_position_colors[scale_position], fontWeight: 900,
                        width: "3vh", "height": "3vh", left: (16.7*pos.string_index + 4.3) + "%",
                        top: (200 - Math.pow(.946, pos.fret)*200) + "vh",
                        position: "absolute", borderRadius: "1vh"}}>{scale_position+1}</div>;
        } else { return null; }
      })}

    </div>;

    return (
      <div className="container"><div className="row">
        <div className="col-3">
          <select name="key" id="keyselect" onChange={this.keychange.bind(this)}>
          {key_names.map((name, number) =>
            <option value={number} key={number}>{name}</option>
          )}
          </select>
        </div>

        <div className="col-6">
          {fretboard}
        </div>

        <div className="col-3">
          <select name="mode" id="modeselect" onChange={this.modechange.bind(this)}>
          {major_modes.map((mode) =>
            <option value={mode} key={mode}>{mode}</option>
          )}
          </select>
        </div>
      </div></div>
    );
  }
}

export default Guitar;