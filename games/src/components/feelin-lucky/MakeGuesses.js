import React, { Component } from "react";
const qs = require('querystring');

import Awaiting from "./Awaiting";

class MakeGuesses extends Component {
  state = {
    message: "",
    index: 0,
    currentAuthor: "",
    currentSearchQuery: ""
  };

  static getDerivedStateFromProps(props, state) {
    var index = 0;
    props.guesses.map((guess) => {
      if (guess.guesser == props.username) {
        index ++;
      }
    });

    state.index = index;
    return state;
  }

  setStateAndSubmit(o) {
    this.setState(o, () => {
      if (this.state.currentAuthor != "" && this.state.currentSearchQuery != "") {
        this.submitGuess();
      }
    });
  }

  submitGuess() {
    var sub = this.props.submissions[this.state.index];
    var author = this.state.currentAuthor, searchQuery = this.state.currentSearchQuery;

    this.setState({
      currentAuthor: "",
      currentSearchQuery: ""
    });

    fetch("feelin_lucky/guess", {
      method: "POST",
      body: qs.stringify({
        guesser: this.props.username,
        submissionId: sub.id,
        author: author,
        searchQuery: searchQuery
      }),
      headers: { "Content-Type": "application/x-www-form-urlencoded" }
    }).then(response => {
      if (response.status !== 200) {
        this.setState({ message: "Network error" });
      }
      this.props.fetchGuesses();
    });
  }

  render() {
    if (this.props.submissions.length == 0) {
      return <p>Loading...</p>;
    }

    if (this.state.index > 0) {
      var prev_submission_id = this.props.submissions[this.state.index-1].id;
      var guesses_for_prev_submission = this.props.guesses.filter(guess => guess.submission == prev_submission_id);

      if (guesses_for_prev_submission.length != this.props.authors.length) {
        return <Awaiting update={this.props.fetchGuesses} authors={this.props.authors}
                 submitted={guesses_for_prev_submission.map(sub => sub.guesser)} screenNames={this.props.screenNames} />;
      }
    }

    var sub = this.props.submissions[this.state.index];

    var my_guesses = this.props.guesses.filter(guess => guess.guesser == this.props.username),
        authors_already_guessed = my_guesses.map(guess => guess.author),
        queries_already_guessed = my_guesses.map(guess => guess.search_query);

    return <div className="row">
      <div className = "col-0 col-sm-1 col-md-2 col-lg-3"/>
      <div className = "col-12 col-sm-10 col-md-8 col-lg-6">
        <img src={"/static/img/feelin_lucky_downloads/" + sub.filename} className="candidate"
          style={{margin: 0}}/>
        <p>{this.state.message}</p>
      </div>
      <div className = "col-0 col-sm-1 col-md-2 col-lg-3"/>

      <div className = "col-6">
        {this.props.authors.filter(author => !authors_already_guessed.includes(author)).sort().map((author) =>
          <div key={author}>
            <input type="radio" name="author" onClick={() => this.setStateAndSubmit({currentAuthor: author})} />
            <p>{this.props.screenNames[author]}</p>
          </div>
        )}
      </div>

      <div className = "col-6">
        {this.props.searchQueries.filter(query => !queries_already_guessed.includes(query)).sort().map((searchQuery) =>
          <div key={searchQuery}>
            <input type="radio" name="search_query"  onClick={() => this.setStateAndSubmit({currentSearchQuery: searchQuery})}/>
            <p>{searchQuery}</p>
          </div>
        )}
      </div>
    </div>;
  }
}

export default MakeGuesses;
