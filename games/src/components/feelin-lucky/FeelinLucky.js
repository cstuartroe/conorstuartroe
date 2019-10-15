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
    authors: [],
    screenNames: {},
    searchQueries: [],
    all_submissions: false,
    submissions: [],
    guesses: []
  };

  fetchSubmissions() {
    fetch('feelin_lucky/submissions?gameInstance=' + this.props.gameInstance)
    .then(response => {
      if (response.status !== 200) {
        return { all_submissions: false, submissions: []};
      }
      return response.json();
    }).then(data => {
      var had_all_submissions = this.state.all_submissions;
      this.setState(data);
      if (data.all_submissions && !had_all_submissions) {
        this.settleSubmisions();
      }
    });
  }

  settleSubmisions() {
    this.setState({
      authors: this.state.submissions.map(sub => sub.author),
      searchQueries: this.state.submissions.map(sub => sub.search_query)
    });

    fetch("users")
    .then(response => {
      if (response.status !== 200) {
        return this.setState({ message: "Network error" });
      }
      return response.json();
    }).then(users => {
      var screenNames = {};
      users.map((user) => {
        screenNames[user.username] = user.screen_name;
      });
      this.setState({
        screenNames: screenNames
      })
    });
  }

  fetchGuesses(guesses) {
    fetch("feelin_lucky/guess?gameInstance=" + this.props.gameInstance)
    .then(response => {
      if (response.status !== 200) {
        return this.setState({ message: "Network error" });
      }
      return response.json();
    })
    .then(guesses => this.setState({guesses: guesses}));
  }

  componentDidMount() {
    this.fetchSubmissions();
    this.fetchGuesses();
  }

  render() {
    var gameElem;

    if (!this.state.all_submissions) {
      if (!this.state.submissions.some(sub => (sub.author == this.props.username))) {
        gameElem = <ImageSearch username={this.props.username} gameInstance={this.props.gameInstance}
                     fetchSubmissions={this.fetchSubmissions.bind(this)} />;
      } else if (!this.state.submissions.some(sub => (sub.author == this.props.username && sub.filename != ""))) {
        gameElem = <ImageSelect username={this.props.username} gameInstance={this.props.gameInstance}
                     submissions={this.state.submissions} fetchSubmissions={this.fetchSubmissions.bind(this)} />;
      } else {
        gameElem = <Awaiting fetchSubmissions={this.fetchSubmissions.bind(this)} />;
      }
    } else {
      gameElem = <MakeGuesses username={this.props.username} gameInstance={this.props.gameInstance}
                   submissions={this.state.submissions} fetchSubmissions={this.fetchSubmissions.bind(this)}
                   authors={this.state.authors} screenNames={this.state.screenNames}
                   searchQueries={this.state.searchQueries} guesses={this.state.guesses} />;
    }

    return gameElem;
  }
}

export default FeelinLucky;