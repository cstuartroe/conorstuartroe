import React, { Component } from "react";

class GamePicker extends Component {
  state = {
    games: [{"slug": "feelin-lucky", "title": "Feelin' Lucky?"}],
    message: ""
  };

  render() {
    return (
      <div className="row" id="game-picker">
        <div className="col-12">
          <h1>Select a Game:</h1>
          <p>{this.state.message}</p>
        </div>

        {this.state.games.map((game) =>
          <div className="col-6 col-md-4" key={game.slug}>
            <button className="big-select" onClick={() => this.props.setGame(game.slug, game.title)}>{game.title}</button>
          </div>
        )}
      </div>
    );
  }
}

export default GamePicker;