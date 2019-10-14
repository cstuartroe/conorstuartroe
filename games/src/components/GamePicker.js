import React, { Component } from "react";

class GamePicker extends Component {
  state = {};

  games = [{
    id: "feelin-lucky",
    name: "Feelin' Lucky?"
  }];

  render() {
    return (
      <div className="row" id="game-picker">
        <div className="col-12">
          <h2>Pick a Game</h2>
        </div>

        {this.games.map((game) =>
          <div className="col-6 col-md-4 goto-game" onClick={() => this.props.setGame(game.id)}>
            <h2>{game.name}</h2>
          </div>
        )}
      </div>
    );
  }
}

export default GamePicker;