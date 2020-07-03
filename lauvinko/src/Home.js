import React, { Component } from "react";

import SectionLinks from "./SectionLinks.js";
import Contents from "./Contents.js";
import {flatten} from "./PageHeader.js";
import allContents from "../static/lauvinko/json/contents.json";

class Home extends Component {
  render() {
    return (
      <div>
        <h1 style={{marginTop: "3vh"}}>Lauvìnko</h1>

        <img src="/static/lauvinko/img/LotusWithText.png" style={{width: "30vh", height: "30vh", margin: "2em auto"}}/>

        <p style={{textAlign: "center", padding: ".5em"}}>Lauvìnko is a constructed language created by Conor Stuart Roe. The table of contents for this site can be found at the bottom.</p>

        <p style={{textAlign: "center", padding: ".5em"}}>Not sure what to read first? Here are a few good places to start to get a feel for the project!</p>

        <SectionLinks sections={[
          ["introduction", "Introduction to the Project"],
          ["class_words", "Lesson #1"],
          ["north_wind", "The North Wind and the Sun"]
        ]}/>

        <p style={{textAlign: "center", padding: ".5em"}}>These are some of my favorite pages:</p>

        <SectionLinks sections={[
          ["colors", <p style={{display: "inline-block"}}>
            <span style={{color: "red"}}>C</span>
            <span style={{color: "orange"}}>o</span>
            <span style={{color: "yellow"}}>l</span>
            <span style={{color: "green"}}>o</span>
            <span style={{color: "blue"}}>r</span>
            <span style={{color: "purple"}}>s</span>
            <span style={{color: "pink"}}>!</span>
          </p>],
          ["proto", "Proto-Kasanic (Lauvìnko's ancestor language)"],
          ["case_aspect_interaction", "Case-Aspect Interaction (a grammatical wonder!)"]
        ]}/>

        <p style={{textAlign: "center", padding: ".5em"}}>For those interested in the whole shebang, here are all {flatten(allContents).length} pages on this site:</p>

        <Contents/>
      </div>
    );
  }
}

export default Home;