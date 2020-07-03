import React, { Component } from "react";
import { BrowserRouter as Router, Route, Link, Switch } from "react-router-dom";
import ReactDOM from "react-dom";

import Home from "./Home.js";
import Page from "./Page.js";
import Dictionary from "./Dictionary.js";

class App extends Component {
    state = {
        contents: {
            subsections: []
        },
        font: "Lauvinko Smooth Serif"
    };

    switchFonts() {
        if (this.state.font === "Lauvinko Smooth Serif") {
            $(".lauvinko").css({"font-family": "Lauvinko Bubble"});
            $("span.lauvinko").css({"font-size": "1.5vh"});
            $("td.lauvinko").css({"font-size": "2vh"});
            $("h1.lauvinko").css({"font-size": "3vh"});
            this.setState({font: "Lauvinko Bubble"});
        } else {
            $(".lauvinko").css({"font-family": "Lauvinko Smooth Serif"});
            $("span.lauvinko").css({"font-size": "2vh"});
            $("td.lauvinko").css({"font-size": "2.5vh"});
            $("h1.lauvinko").css({"font-size": "4vh"});
            this.setState({font: "Lauvinko Smooth Serif"});
        }
    }

    render() {
        return (
            <div id="mainframe" className="container">
                <div className="row">
                    <div className="col-1 col-md-2"></div>
                    <div className="col-10 col-md-8">
                        <Router>
                            <Switch>
                                <Route exact={true} path="/lauvinko" component={Home}/>
                                <Route exact={true} path="/lauvinko/kasanic_dictionary"
                                       render={(props) => <Dictionary {...props} origins={["kasanic"]}
                                       page_id="kasanic_dictionary"/>}/>
                                <Route exact={true} path="/lauvinko/loanword_dictionary"
                                       render={(props) => <Dictionary {...props} origins={["sanskrit", "malay", "arabic", "tamil", "hokkien", "portuguese", "dutch", "english"]}
                                       page_id="loanword_dictionary"/>}/>
                                <Route path="/lauvinko/:id" render={({match}) => <Page id={match.params.id}/>}/>
                            </Switch>
                        </Router>
                    </div>
                    <div className="col-1 col-md-2"></div>
                </div>

                <hr/>

                <div id="footer">
                    <p style={{textAlign: "center"}}>All content &copy; Conor Stuart Roe 2018 under a <a
                        href="http://creativecommons.org/licenses/by-nc-nd/3.0/">CC BY-NC-ND 3.0</a> license.</p>
                </div>

                <button id="font-toggle" onClick={this.switchFonts.bind(this)}>
                    <p style={{fontFamily: (this.state.font === "Lauvinko Smooth Serif") ? "Lauvinko Bubble" : "Lauvinko Smooth Serif"}}>Aq</p>
                </button>
            </div>
        );
    }
}

const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render(<App />, wrapper) : null;