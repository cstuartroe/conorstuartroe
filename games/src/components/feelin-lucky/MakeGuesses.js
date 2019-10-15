import React, { Component } from "react";
const qs = require('querystring');

class MakeGuesses extends Component {
  state = {
    message: "",
    index: 0,
    currentAuthor: "",
    currentSearchQuery: ""
  };

  componentDidMount() {
    this.props.guesses.map((guess) => {
      if (this.props.submissions.some((sub) => (guess.guesser == this.props.username) && (guess.submission = sub.id))) {
        this.setState({
          index: this.state.index+1
        });
      }
    });
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
        return this.setState({ message: "Network error" });
      }
      return this.setState({index: this.state.index+1});
    });
  }

  render() {
    var sub = this.props.submissions[this.state.index];

    return <div className="row">
      <div className = "col-3"/>
      <div className = "col-6">
        <img src={"/static/img/feelin_lucky_downloads/" + sub.filename} className="candidate" />
        <p>{this.state.message}</p>
      </div>
      <div className = "col-3"/>

      <div className = "col-6">
        {this.props.authors.map((author) =>
          <div key={author}>
            <input type="radio" name="author" onClick={() => this.setStateAndSubmit({currentAuthor: author})} />
            <p>{this.props.screenNames[author]}</p>
          </div>
        )}
      </div>

      <div className = "col-6">
        {this.props.searchQueries.map((searchQuery) =>
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