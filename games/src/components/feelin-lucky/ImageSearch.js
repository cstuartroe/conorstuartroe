import React, { Component } from "react";
const qs = require('querystring');

class ImageSearch extends Component {
  state = {
    currentQuery: "",
    loading: false,
    message: ""
  };

  sendSearch(query) {
    this.setState({loading: true});

    fetch('feelin_lucky/search', {
      method: "POST",
      body: qs.stringify({username: this.props.username, gameInstance: this.props.gameInstance, query: query}),
      headers: { "Content-Type": "application/x-www-form-urlencoded" }
    }).then(response => {
      if (response.status !== 200) {
        return this.setState({ message: "Network error", loading: false });
      }
      return response.json();
    }).then(data => {
      this.props.setCandidates(data);
      this.setState({loading: false});
    });
  }

  render() {
    return <div className="row">
      <div className = "col-12">
        <h2>Please enter a search term:</h2>
        <input type="text" onChange={event => {this.setState({currentQuery: event.target.value})}}></input>
        <button onClick={() => this.sendSearch(this.state.currentQuery)}>Search!</button>
        <p>{this.state.message}</p>
        <img src="/static/img/loading.gif" style={{display: this.state.loading ? "inline-block" : "none"}}/>
      </div>
    </div>;
  }
}

export default ImageSearch;