import React, { Component } from "react";

class Scoreboard extends Component {
  state = {
    scores: []
  };

  componentDidMount() {
    this.fetchScores();
  }

  fetchScores() {
    fetch("scores?gameInstance=" + this.props.gameInstance)
    .then(response => {
      if (response.status !== 200) {
        return this.setState({ message: "Network error" });
      }
      return response.json();
    })
    .then(scores => this.setState({scores: scores}));
  }

  render() {
    var boldStyle = {
      fontWeight: 900
    };

    return <div className="row">
    <div className="col-12">
      {this.state.scores.sort((score1, score2) => score2.value - score1.value).map(score =>
        <p key={score.player}>
          <span style={boldStyle}>{this.props.screenNames[score.player]}</span> scored {score.value} points.
        </p>
      )}
    </div>

    {this.props.submissions.map(sub =>
      <div className="col-12" key={sub.id}>
        <img src={sub.filename} className="candidate" />
        <p>This picture was submitted by <span style={boldStyle}>{this.props.screenNames[sub.author]}</span> with
        the search term <span style={boldStyle}>{sub.search_query}</span>.</p>
        {this.props.guesses.filter(guess => (guess.submission == sub.id) && (guess.guesser != sub.author))
           .sort((a, b) => a.guesser - b.guesser).map(guess =>
          <p key={guess.id}><span style={boldStyle}>{this.props.screenNames[guess.guesser]}</span> guessed
            that <span style={boldStyle}>{this.props.screenNames[guess.author]}</span> submitted it with the search
            term <span style={boldStyle}>{guess.search_query}</span>.</p>
        )}
      </div>
    )}
    </div>;
  }
}

export default Scoreboard;