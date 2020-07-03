import React, { Component } from "react";
import {Link} from "react-router-dom";

import allContents from "../static/lauvinko/json/contents.json";

function toTitleCase(str) {
  return str.replace(/_/g, ' ').split(' ')
  .map(w => w[0].toUpperCase() + w.substr(1).toLowerCase())
  .join(' ')
}

function getSectionTitle(section) {
  return section.title ? section.title : toTitleCase(section.name);
}

function getSectionDataHelper(contents, section_name) {
  if (contents.name === section_name)  {
    var out = {
      name: section_name,
      title: getSectionTitle(contents)
    };

    if (contents.subsections) {
      var children = [];
      for (var subsection of contents.subsections) {
        children.push([subsection.name, getSectionTitle(subsection)]);
      }
      out.children = children
    }

    return out;

  } else if (contents.subsections) {
    for (var subsection of contents.subsections) {
      var out = getSectionDataHelper(subsection, section_name);
      if (out.name) {
        if (contents.name && !out.parent_name) {
          out.parent_name = contents.name;
          out.parent_title = getSectionTitle(contents);
        }
        return out;
      }
    }
  }

  return {};
}

function getSectionData(section_name) {
  return getSectionDataHelper(allContents, section_name)
}

function flatten(contents) {
  var out = [];
  if (contents.name) {
    out.push({name: contents.name, title: getSectionTitle(contents)});
  }
  if (contents.subsections) {
    for (var subsection of contents.subsections) {
      out = out.concat(flatten(subsection));
    }
  }
  return out;
}

function get_neighbors(section_name) {
  var flat = flatten(allContents);

  for (var i in flat) {
    if (flat[i].name === section_name) {
      var out = {};
      if (i > 0) {
        out.prev = flat[i-1];
      }
      if (i-0+1 < flat.length) {
        out.next = flat[i-0+1];
      }
      return out;
    }
  }

  return {};
}

class PageHeader extends Component {
  render() {
    const section_data = getSectionData(this.props.id);
    const neighbors = get_neighbors(this.props.id);

    return (
      <div>
        <h1 style={{marginTop: "3vh"}}>{section_data ? section_data.title : null}</h1>
        <div className="row">
          <div className="col-12 col-md-4">
            {neighbors.prev ?
              <p className="go-up">
                <Link to={"/lauvinko/" + neighbors.prev.name}>← {neighbors.prev.title}</Link>
              </p>
              : null
            }
          </div>

          <div className="col-12 col-md-4">
            {section_data.parent_name ?
              <p className="go-up">
                <Link to={"/lauvinko/" + section_data.parent_name}>Go up to {section_data.parent_title}</Link>
              </p>
              :
              <p className="go-up">
                <Link to={"/lauvinko"}>Go up to index page</Link>
              </p>
            }
          </div>

          <div className="col-12 col-md-4">
            {neighbors.next ?
              <p className="go-up">
                <Link to={"/lauvinko/" + neighbors.next.name}>{neighbors.next.title} →</Link>
              </p>
              : null
            }
          </div>
        </div>
      </div>
    );
  }
}

export default PageHeader;
export { getSectionTitle, getSectionData, get_neighbors, flatten };