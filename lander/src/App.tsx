import React, { Component } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import Guitar from "./Guitar"

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

export default App;
