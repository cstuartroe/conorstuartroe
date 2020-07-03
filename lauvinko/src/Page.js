import React, { Component } from "react";
import { Link } from "react-router-dom";

import PageHeader, { getSectionData } from "./PageHeader.js"
import SectionLinks from "./SectionLinks.js";
import Gloss, {InlineGloss, AugmentPair} from "./Gloss.js";

function grab_inline_gloss(line, i) {
  var content = "";
  while (line[i] !== '`') {
    content += line[i];
    i++;
  }
  return {
    content: content,
    i: i+1
  };
}

function parse_md_line(line, i=0, closer=null) {
  let out = [], curr_content = "";

  while (i < line.length) {
    if (closer && (line.substring(i, i+closer.length) === closer &&
        ((closer !== "*") || (line.substring(i, i+2) !== "**")) )) {
      out.push(curr_content);
      return {
        content: out,
        i: i + closer.length
      };
    }

    let r = null, new_element = null;

    if (line.substring(i, i+2) === '{{') {
      r = parse_md_line(line, i+2, "}}")
      if (r.content.length > 1) { throw("Don't put content inside a cf"); }
      const section_data = getSectionData(r.content[0]);
      new_element = <Link to={'/lauvinko/' + section_data.name} key={i}>{section_data.title}</Link>;
    }
    else if (line.substring(i, i+2) === '![') {
      const alt = parse_md_line(line, i+2, "]");
      if (line[alt.i] === "(") {
        r = parse_md_line(line, alt.i+1, ')');
        if (r.content.length > 1 || alt.content.length > 1) { throw("Img stuff can't be nested!"); }
        new_element = <img src={r.content[0]} key={i} alt={alt.content[0]}/>;
      } else {
        out.push(curr_content + "![");
        out.concat(alt.content);
        out.push("]");
        curr_content = "";
        i = alt.i;
      }
    }
    else if (line[i] === '[') {
      const text = parse_md_line(line, i+1, "]");
      if (line[text.i] === "(") {
        r = parse_md_line(line, text.i+1, ')');
        if (r.content.length > 1) { throw("href can't be nested!"); }
        new_element = <a href={r.content[0]} key={i}>{text.content[0]}</a>;
      } else {
        out.push(curr_content + "[");
        out = out.concat(text.content);
        out.push("]");
        curr_content = "";
        i = text.i;
      }
    }
    else if (line.substring(i, i+2) === '**') {
      r = parse_md_line(line, i+2, '**');
      new_element = React.createElement("span", {key: i, className: "bold"}, r.content);
      i = r.i;
    }
    else if (line[i] === '*') {
      r = parse_md_line(line, i+1, '*');
      new_element = React.createElement("span", {key: i, className: "italic"}, r.content);
      i = r.i;
    }
    else if (line[i] === '$') {
      r = parse_md_line(line, i+1, '$');
      new_element = React.createElement("span", {key: i, className: "abbrev"}, r.content);
      i = r.i;
    }
    else if (line[i] === '`') {
      if (line.substring(i+1, i+4) === "ap ") {
        r = grab_inline_gloss(line, i+4);
        new_element = <AugmentPair content={r.content} key={JSON.stringify(r)}/>;
      } else {
        r = grab_inline_gloss(line, i + 1);
        new_element = <InlineGloss content={r.content} key={JSON.stringify(r)}/>;
      }
    }
    else if (line[i] === '^') {
      if (line[i+1] === '{') {
        r = parse_md_line(line, i+2, "}");
        new_element = React.createElement("sup", {key: i}, r.content);
      } else {
        out.push(curr_content);
        out.push(React.createElement("sup", {key: i}, line[i + 1]));
        i += 2;
        curr_content = "";
      }
    }
    else if (line[i] === '@') {
      curr_content += '\u06de';
      i++;
    }
    else {
      curr_content += line[i];
      i++;
    }

    if (r) {
      out.push(curr_content);
      curr_content = "";
      out.push(new_element);
      i = r.i;
    }
  }

  if (closer === null) {
    out.push(curr_content);
    return out;
  } else {
    throw("oops!");
  }
}

function MDTable(props) {
  var headrow;
  var rows = [];

  var alignment_strings = props.lines[1].split('|'), alignments = [];
  for (var i = 1; i + 1 < alignment_strings.length; i++) {
    if (alignment_strings[i].endsWith(':')) {
      alignments.push(alignment_strings[i].startsWith(':') ? "center" : "right");
    } else {
      alignments.push("left");
    }
  }

  for (var i in props.lines) {
    if (i === '1') { continue; }

    const tds = [];
    const td_strings = props.lines[i - 0].split('|');
    const numcols = Math.min(alignments.length, td_strings.length - 2);
    for (var j = 0; j < numcols; j++) {
      if (td_strings[j + 1] !== "+") {
        let colSpan = 1;
        while ((numcols > j + colSpan) && (td_strings[j + colSpan + 1] === "+")) {
          colSpan++;
        }
        tds.push(React.createElement((i === '0' ? "th" : "td"), {
              key: j, style: {textAlign: alignments[j]},
              colSpan: colSpan,
              className: (td_strings[j + 1] === "^") ? "merge-above" : ""
            },
            parse_md_line((td_strings[j + 1] === "^") ? "" : td_strings[j + 1])))
      }
    }

    if (i === '0') {
      headrow = React.createElement("tr", {key: i}, tds);
    } else {
      rows.push(React.createElement("tr", {key: i}, tds));
    }
  }

  return <table>
    <thead>{headrow}</thead>
    <tbody>{rows}</tbody>
  </table>;
}

function parse_md(markdown) {
  var children = [];
  var curr_content = [];
  var curr_type = null;
  var child_no = 0;

  for (const line of (markdown + "\n").split('\n')) {
    if (curr_type) {
      if (curr_type === "table") {
        if(line.startsWith('|')) {
          curr_content.push(line);
        } else {
          children.push(<MDTable lines={curr_content} key={child_no++}/>);
          curr_content = [];
          curr_type = null;
        }
      }
      else if (curr_type === "gloss") {
        curr_content.push(line.replace(/```/g, ''));
        if (line.endsWith('```')) {
          children.push(<Gloss key={child_no++} content={curr_content}/>);
          curr_content = []
          curr_type = null;
        }
      }
      else if (line === "") {
        children.push(React.createElement(curr_type, {key: child_no++}, curr_content));
        curr_content = [];
        curr_type = null;
      }
      else {
        curr_content = curr_content.concat(parse_md_line(line + " "));
      }
    } else {
      if (line === "") {
      }
      else if (line.startsWith('# ')) {
        curr_type = "h1";
        curr_content = parse_md_line(line.substring(2) + " ");
      }
      else if (line.startsWith('## ')) {
        curr_type = "h2";
        curr_content = parse_md_line(line.substring(3) + " ");
      }
      else if (line.startsWith('### ')) {
        curr_type = "h3";
        curr_content = parse_md_line(line.substring(4) + " ");
      }
      else if (line.startsWith('|')) {
        curr_type = "table";
        curr_content.push(line);
      }
      else if (line.startsWith('```')) {
        curr_type = "gloss";
        curr_content.push(line.substring(3));
      }
      else {
        curr_type = "p";
        curr_content = parse_md_line(line + " ");
      }
    }
  }

  return React.createElement("div", {}, children);
}

class Page extends Component {
  state = {
    markdown: "",
    prev_id: null
  };

  componentDidMount() {
    this.componentDidUpdate();
  }

  componentDidUpdate() {
    if (this.props.id !== this.state.prev_id) {
      fetch('/static/lauvinko/md/' + this.props.id + '.md')
        .then(response => {
          if (response.status !== 200) {
            return this.setState({markdown: "This page does not appear to be written yet."});
          }
          return response.text();
        })
        .then(text => text ? this.setState({markdown: text}) : null);
      this.setState({prev_id: this.props.id});
    }
  }

  render() {
    return (
      <div>
        <PageHeader id={this.props.id}/>
        {parse_md(this.state.markdown)}
        <SectionLinks id={this.props.id}/>
      </div>
    );
  }
}

export default Page;
export {parse_md_line};