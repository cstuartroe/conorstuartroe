import React, { Component } from "react";
import ReactDOM from "react-dom";

import TopMenu from "./components/TopMenu"
import GamePicker from "./components/GamePicker"

class App extends Component {
  state = {
    game: null
  };

  setGame(gameId) {
    this.setState({
      game: gameId
    })
  }

  componentDidMount() {
    //fetch(this.props.endpoint)
    //  .then(response => {
    //    if (response.status !== 200) {
    //      return this.setState({ placeholder: "Something went wrong" });
    //    }
    //    return response.json();
    //  })
    //  .then(data => this.setState({ data: data, loaded: true }));
  }

  render() {
    const { game } = this.state;

    var bodyElem;
    switch (game) {
      case null: bodyElem = <GamePicker setGame = {this.setGame.bind(this)} />; break;
      default: bodyElem = <p>Unknown game.</p>; break;
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