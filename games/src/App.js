import React, { Component } from "react";
import ReactDOM from "react-dom";

import TopMenu from "./components/TopMenu";
import UserLogin from "./components/UserLogin";
import GamePicker from "./components/GamePicker";
import FeelinLucky from "./components/feelin-lucky/FeelinLucky"

class App extends Component {
  state = {
    user: null,
    game: null,
    gameInstance: null
  };

  setUser(username) {
    this.setState({
      user: username
    });
  }

  setGame(gameSlug) {
    this.setState({
      game: gameSlug
    });
  }

  setGameInstance(gameInstanceId) {
    this.setState({
      gameInstance: gameInstanceId
    });
  }

  render() {
    const { user, game, gameInstance } = this.state;

    var bodyElem;
    if (user == null) {
      bodyElem = <UserLogin setUser = {this.setUser.bind(this)} />;
    } else if (game == null) {
      bodyElem = <GamePicker setGame = {this.setGame.bind(this)} />;
    } else if (game == "feelin-lucky") {
      bodyElem = <FeelinLucky user={user} gameInstance={gameInstance}/>;
    } else {
      bodyElem = <p>Unknown game.</p>;
    }

    return (
      <div className="container">
        <TopMenu/>
        { bodyElem }
      </div>
    );
  }
}

const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render(<App />, wrapper) : null;