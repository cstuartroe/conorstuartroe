import React, { Component } from "react";
import { BrowserRouter as Router, Route, Link, Switch } from "react-router-dom";
import ReactDOM from "react-dom";

import Guitar from "./Guitar.js"

class App extends Component {
  render() {
    return (
      <Router>
        <Switch>
          <Route exact={true} path="/guitar" render={() => (
            <Guitar/>
          )} />
        </Switch>
      </Router>
    );
  }
}

const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render(<App />, wrapper) : null;