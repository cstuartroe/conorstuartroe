import React, { Component } from "react";
const qs = require('querystring');

class ImageSelect extends Component {
  state = {};

  sendSelection(filename) {
    fetch('feelin_lucky/select', {
      method: "POST",
      body: qs.stringify({username: this.props.username, gameInstance: this.props.gameInstance, selection: filename}),
      headers: { "Content-Type": "application/x-www-form-urlencoded" }
    }).then(response => {
        if (response.status !== 200) {
          return this.setState({ message: "Network error" });
        } else {
          this.props.finishSelecting();
        }
      })
  }

  render() {
    return <div className="row">
      <div className = "col-12">
        <h2>Please select an image:</h2>
        <p>{this.state.message}</p>
      </div>
      {this.props.candidateImages.map(cand =>
        <div className="col-6" key={cand}>
          <img src={"/static/img/feelin_lucky_downloads/" + cand} className="candidate" onClick={() => this.sendSelection(cand)} />
        </div>
      )}
    </div>;
  }
}

export default ImageSelect;