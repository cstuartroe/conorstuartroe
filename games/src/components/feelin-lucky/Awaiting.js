import React, { Component } from "react";

class Awaiting extends Component {
  state = {
    loop: null
  };

  componentDidMount() {
    this.props.update();
    this.state.loop = setInterval(this.props.update, 5000);
  }

  componentWillUnmount() {
    clearInterval(this.state.loop);
  }

  render() {
    return <div className="row">
      <div className = "col-12">
        <p>Awaiting all submissions...</p>
        <img src="/static/img/loading.gif"/>
      </div>
    </div>;
  }
}

export default Awaiting;