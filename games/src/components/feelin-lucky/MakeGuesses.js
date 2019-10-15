import React, { Component } from "react";

class MakeGuesses extends Component {
  state = {
    message: "",
    index: 0,
    authors: [],
    screenNames: {},
    searchQueries: [],
    currentAuthor: "",
    currentSearchQuery: ""
  };

  componentDidMount() {
    this.setState({
      authors: this.props.submissions.map(sub => sub.author),
      searchQueries: this.props.submissions.map(sub => sub.search_query)
    });

    fetch("feelin_lucky/guess?gameInstance=" + this.props.gameInstance)
    .then(response => {
      if (response.status !== 200) {
        return this.setState({ message: "Network error" });
      }
      return response.json();
    }).then(guesses => {
      this.props.submissions.map((sub) => {
        if (guesses.some((guess) => (guess.guesser == this.props.username) && (guess.submission = sub.id))) {
          this.setState({
            index: index+1
          });
        }
      });
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



  render() {
    var sub = this.props.submissions[this.state.index];

    return <div className="row">
      <div className = "col-3"/>
      <div className = "col-6">
        <p>{this.state.message}</p>
        <img src={"/static/img/feelin_lucky_downloads/" + sub.filename} className="candidate" />
      </div>
      <div className = "col-3"/>

      <div className = "col-6">
        {this.state.authors.map((author) =>
          <div key={author}>
            <input type="radio" name="author" value={author}/>
            <p>{this.state.screenNames[author]}</p>
          </div>
        )}
      </div>

      <div className = "col-6">
        {this.state.searchQueries.map((searchQuery) =>
          <div key={searchQuery}>
            <input type="radio" name="search_query" value={searchQuery}/>
            <p>{searchQuery}</p>
          </div>
        )}
      </div>
    </div>;
  }
}

export default MakeGuesses;