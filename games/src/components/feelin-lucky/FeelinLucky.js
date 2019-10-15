import React, { Component } from "react";
import PropTypes from 'prop-types';

import ImageSearch from "./ImageSearch";
import ImageSelect from "./ImageSelect";
import Awaiting from "./Awaiting";
import MakeGuesses from "./MakeGuesses";
import Scoreboard from "./Scoreboard";

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
      this.setState({
        searchQueries: data.submissions.map(sub => sub.search_query)
      });
    });

    fetch("participants?gameInstance=" + this.props.gameInstance)
    .then(response => {
      if (response.status !== 200) {
        return this.setState({ message: "Network error" });
      }
      return response.json();
    }).then(data => {
      this.setState({
        authors: data.participants
      });
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
        gameElem = <Awaiting update={this.fetchSubmissions.bind(this)} authors={this.state.authors}
                     submitted={this.state.authors.filter(author => this.state.submissions.some(sub => (sub.author == author) && (sub.filename != "")))}
                     screenNames={this.state.screenNames} />;
      }
    } else {
      if ((this.state.submissions.length != this.state.authors.length) || (this.state.submissions.length != this.state.searchQueries.length)) {
        gameElem = <p>An error was encountered.</p>;
      } else if (this.state.guesses.length != Math.pow(this.state.submissions.length, 2)) {
        gameElem = <MakeGuesses username={this.props.username} gameInstance={this.props.gameInstance}
                     submissions={this.state.submissions} fetchGuesses={this.fetchGuesses.bind(this)}
                     authors={this.state.authors} screenNames={this.state.screenNames}
                     searchQueries={this.state.searchQueries} guesses={this.state.guesses} />;

      } else {
        gameElem = <Scoreboard submissions={this.state.submissions} guesses={this.state.guesses}
                     screenNames={this.state.screenNames} />;
      }
    }

    return gameElem;
  }
}

export default FeelinLucky;