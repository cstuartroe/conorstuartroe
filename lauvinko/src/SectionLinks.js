import React, { Component } from "react";

import { getSectionData } from "./PageHeader.js";

class SectionLinks extends Component {
  render() {
    let sections;

    if (this.props.sections) {
      sections = this.props.sections;
    } else {
      let section_data = getSectionData(this.props.id);

      if (!section_data || !section_data.children) {
        return null;
      } else {
        sections = section_data.children;
      }
    }

    var width;
    if (sections.length === 2) {
      width = 6;
    } else if (sections.length === 4) {
      width = 3;
    } else {
      width = 4;
    }


    return (
      <div className="row">
        {sections.map((section, i) =>
          <div className={"go-down col-" + width} onClick={() => location.href = "/lauvinko/" + section[0]} key={i}>
            <div>
              <h3>{section[1]}</h3>
            </div>
          </div>
        )}
      </div>
    );
  }
}

export default SectionLinks;