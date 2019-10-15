import React, { Component } from "react";
const qs = require('querystring');

class GamePicker extends Component {
  state = {
    message: "",
    currentInstanceId: ""
  };

  setGameInstance() {
    if (this.state.currentInstanceId == "") {
      fetch('new_game', {
        method: "POST",
        body: qs.stringify({username: this.props.username, game: this.props.game}),
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
      }).then(response => {
        if (response.status !== 200) {
          return this.setState({ message: "Network error" });
        }
        return response.json();
      }).then(data => this.props.setGameInstance(data.gameInstance));

    } else {
      fetch('join_game', {
        method: "POST",
        body: qs.stringify({username: this.props.username, game: this.props.game, gameInstance: this.state.currentInstanceId}),
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
      }).then(response => {
        if (response.status !== 200) {
          return this.setState({ message: "Network error" });
        }
        return response.json();
      }).then(data => {
        if (data.accepted) {
          this.props.setGameInstance(this.state.currentInstanceId.toUpperCase());
        } else {
          this.setState({ message: data.message });
        }
      });
    }
  }

  render() {
    return (
      <div className="row" id="game-picker">
        <div className="col-12">
          <h1>Enter your game room, or create a new one:</h1>
          <input type="text" style={{fontSize: "5vh", width: "20vh", fontVariant: "all-small-caps"}}
            onChange={event => {this.setState({currentInstanceId: event.target.value})}}></input>
          <p>{this.state.message}</p>
        </div>

        <div className="col-12">
          <button className="big-select" onClick={() => this.setGameInstance()}>
            {this.state.currentInstanceId == "" ? "Create a new game" : "Join"}
          </button>
        </div>
      </div>
    );
  }
}

export default GamePicker;