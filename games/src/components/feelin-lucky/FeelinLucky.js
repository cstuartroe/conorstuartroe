import React, { Component } from "react";
import PropTypes from 'prop-types';

import ImageSearch from "./ImageSearch";
import ImageSelect from "./ImageSelect";
import Scoreboard from "../Scoreboard";

class FeelinLucky extends Component {
  static propTypes = {
    username: PropTypes.string.isRequired,
    gameInstance: PropTypes.string.isRequired
  }

  state = {
    candidateImages: [],
    selected: false,
    submissions: {}
  };

  setCandidates(candidates) {
    this.setState({
      candidateImages: candidates
    });
  }

  finishSelecting() {
    this.setState({
      selected: true
    })
  }

  render() {
    var gameElem;

    if (this.state.candidateImages.length == 0) {
      gameElem = <ImageSearch setCandidates={this.setCandidates.bind(this)} />;
    } else if (!this.state.selected) {
      gameElem = <ImageSelect candidateImages={this.state.candidateImages} finishSelecting={this.finishSelecting.bind(this)} />;
    } else {
      gameElem = <Scoreboard/>;
    }

    return gameElem;
  }
}

export default FeelinLucky;