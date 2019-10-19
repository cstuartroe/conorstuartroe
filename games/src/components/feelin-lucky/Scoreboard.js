import React, { Component } from "react";

class Scoreboard extends Component {
  state = {};

  render() {
    var boldStyle = {
      fontWeight: 900
    };

    return <div className="row">
    {this.props.submissions.map(sub =>
      <div className="col-12" key={sub.id}>
        <img src={"/static/img/feelin_lucky_downloads/" + sub.filename} className="candidate" />
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