import React, { Component } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import Guitar from "./Guitar";
import TwitterMirror from "./TwitterMirror";

class App extends Component {
  render() {
    return (
        <Router>
          <Switch>
            <Route exact={true} path="/guitar" render={() => (
                <Guitar/>
            )} />
            <Route exact={true} path="/twitter_mirror" render={() => (
                <TwitterMirror/>
            )} />
          </Switch>
        </Router>
    );
  }
}

export default App;
