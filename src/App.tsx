import React, { Component } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import Guitar from "./Guitar";
import TwitterMirror from "./TwitterMirror";
import NewCalendar from "./NewCalendar";
import NewCalendarExplanation from "./NewCalendar/explanation";
import Pipes from "./Pipes";
import Navbar from "./Navbar";
import Home from "./Home";
import Projects from "./Projects";
import NoteDrops from "./NoteDrops";
import NotFound from "./NotFound";

import "../static/scss/lander.scss";

class App extends Component<{}> {
  render() {
    return (
      <Router>
        <Switch>
          <Route exact={true} path="/guitar" render={() => (
            <Guitar edo={12}/>
          )}/>
          <Route exact={true} path="/guitar/:edo" render={(t) => (
            <Guitar edo={parseInt(t.match.params.edo)}/>
          )}/>
          <Route exact={true} path="/twitter_mirror" render={() => (
            <TwitterMirror/>
          )}/>
          <Route exact={true} path="/new_calendar" render={() => (
            <NewCalendar/>
          )}/>
          <Route exact={true} path="/new_calendar/explanation" render={() => (
            <NewCalendarExplanation/>
          )}/>
          <Route exact={true} path="/notedrops" render={() => (
            <NoteDrops/>
          )}/>
          <Route exact={false} path="">
            <Pipes/>

            <div className={'lander-style'}>
              <Navbar/>


              <div className="container-fluid" style={{padding: '10vh 0 0'}}>
                <div className="row" style={{marginLeft: 0, marginRight: 0}}>
                  <Switch>
                    <Route exact={true} path={"/"} render={() => (
                      <Home/>
                    )}/>
                    <Route exact={true} path={"/projects"} render={() => (
                      <Projects/>
                    )}/>
                    <Route exact={false} path={''} render={() => (
                      <NotFound/>
                    )}/>
                  </Switch>
                </div>
              </div>
            </div>
          </Route>
        </Switch>
      </Router>
    );
  }
}

export default App;
