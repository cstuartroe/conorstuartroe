import React, { Component } from "react";

import { getSectionTitle } from "./PageHeader.js";
import allContents from "../static/lauvinko/json/contents.json";

function content_ul(section_list, base_number) {
  var children = [];

  for (var i in section_list) {
    var section = section_list[i];
    var section_number = base_number + (base_number !== "" ? "." : "")+ (i-0+1) ;
    var link_text = section_number + " " + getSectionTitle(section);
    children.push(<a href={"/lauvinko/" + section.name} key={i}><li>{link_text}</li></a>)
    if (section.subsections) {
      children.push(content_ul(section.subsections, section_number));
    }
  }

  return React.createElement("ul", {key: base_number + "ul"}, children);
}

class SectionLinks extends Component {
  render() {
    return (
      <div className="scroll" style={{maxHeight: "75vh"}}>
        {content_ul(allContents.subsections, "")}
      </div>
    );
  }
}

export default SectionLinks;