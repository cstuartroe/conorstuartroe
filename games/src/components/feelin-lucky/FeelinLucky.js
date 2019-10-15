import React, { Component } from "react";
import PropTypes from 'prop-types';

import ImageSearch from "./ImageSearch";
import ImageSelect from "./ImageSelect";
import Awaiting from "./Awaiting";
import MakeGuesses from "./MakeGuesses";
import Scoreboard from "../Scoreboard";

class FeelinLucky extends Component {
  static propTypes = {
    username: PropTypes.string.isRequired,
    gameInstance: PropTypes.string.isRequired
  }

  state = {
    candidateImages: [],
    selected: false,
    all_submissions: false,
    submissions: []
  };

  setCandidates(candidates) {
    this.setState({
      candidateImages: candidates
    });
  }

  finishSelecting() {
    this.setState({
      selected: true
    });
  }

  fetchSubmissions() {
    fetch('feelin_lucky/submissions?gameInstance=' + this.props.gameInstance)
    .then(response => {
      if (response.status !== 200) {
        return { all_submissions: false, submissions: []};
      }
      return response.json();
    }).then(data => {
      this.setState(data);
    });
  }

  componentDidMount() {
    this.fetchSubmissions();
  }

  render() {
    var gameElem;

    if (!this.state.all_submissions) {
      if (this.state.submissions.some(sub => (sub.author == this.props.username))) {
        gameElem = <Awaiting fetchSubmissions={this.fetchSubmissions.bind(this)} />;
      } else if (this.state.candidateImages.length == 0) {
        gameElem = <ImageSearch username={this.props.username} gameInstance={this.props.gameInstance}
                     setCandidates={this.setCandidates.bind(this)} />;
      } else if (!this.state.selected) {
        gameElem = <ImageSelect username={this.props.username} gameInstance={this.props.gameInstance}
                     candidateImages={this.state.candidateImages} finishSelecting={this.finishSelecting.bind(this)} />;
      } else {
        gameElem = <Awaiting fetchSubmissions={this.fetchSubmissions.bind(this)} />;
      }
    } else {
      gameElem = <MakeGuesses gameInstance={this.props.gameInstance} submissions={this.state.submissions} />;
    }

    return gameElem;
  }
}

export default FeelinLucky;