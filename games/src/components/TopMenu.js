import React, { Component } from "react";

class TopMenu extends Component {
  state = {};

  render() {
    return (
      <div className="row" id="top-menu">
        <div className="col-4">
          <h2>{this.props.screen_name || ""}</h2>
        </div>
        <div className="col-4">
          <h2>{this.props.gameTitle || ""}</h2>
        </div>
        <div className="col-4">
          <h2>{this.props.gameInstance || ""}</h2>
        </div>
      </div>
    );
  }
}

export default TopMenu;