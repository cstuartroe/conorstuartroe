import React, { Component } from "react";
import {Link} from "react-router-dom";

import raw_dict from "../dictionary.json";

function parse_outline_word(word, i) {
  const e = word.startsWith("$") ? <span className="abbrev">{word.replace(/\$/g, '')}</span> : word;
  if (!raw_dict[word]) {
    return <Link to="/lauvinko/glossing" key={i} target="_blank">{e}</Link>;
  } else {
    return <Link to={"/lauvinko/kasanic_dictionary?q=@" + word} key={i} target="_blank">{e}</Link>;
  }
}

function parse_outline(line) {
  var out = [], curr_content = "";

  var i = 0;
  while (i < line.length) {
    if (" =-.".includes(line[i])) {
      out.push(parse_outline_word(curr_content, i));
      out.push(line[i]);
      curr_content = "";
      i++;
    }
    else {
      curr_content += line[i];
      i += 1;
    }
  }
  out.push(parse_outline_word(curr_content, -1));

  return out;
}

class InlineGloss extends Component {
  state = {
    gloss: null,
  };

  componentDidMount() {
    const l = this.props.content.split(" ");
    const lang = l[0], rules = l[1], outline = l.splice(2).join('_').replace(/=/g, '~');
    this.setState({rules: rules});

    fetch('/lauvinko/gloss?lang=' + lang + '&outline=' + outline)
        .then(response => {
          if (response.status !== 200) {
            return this.setState({status: "failed", reason: "Network error"});
          }
          return response.json();
        })
        .then(data => data ? this.setState(data) : null);
  }

  render() {
    return (
        this.state.gloss ? <span>
          {this.state.rules.includes('f') ? <span className="lauvinko">{this.state.gloss.falavay + " "}</span> : null}
          {this.state.rules.includes('t') ? <span style={{fontStyle: "italic"}}>{this.state.gloss.transcription}</span> : null}
        </span> : (this.state.status === "failed" ?
            <i>Failed: {this.state.reason}</i>
            : <i>gloss loading...</i>)
    );
  }
}

function AugmentPair(props) {
  return (
      <span>
        <InlineGloss content={"lv ft " + props.content + ".$au$"}/>{", "}
        <InlineGloss content={"lv ft " + props.content + ".$na$"}/>
      </span>
  )
}

class Gloss extends Component {
  state = {
    display_rules: null,
    translation: ""
  };

  componentDidMount() {
    var i = 1, outline = "";
    while (this.props.content[i] !== "") {
      outline += this.props.content[i];
      i++;
    }
    this.setState({translation: this.props.content.slice(i).join(" "), display_rules: this.props.content[0]})

    fetch('/lauvinko/gloss?lang=lv&outline=' + outline.replace(/ /g, '_').replace(/=/g, '~'))
      .then(response => {
        if (response.status !== 200) {
          return this.setState({status: "failed", reason: "Network error"});
        }
        return response.json();
      })
      .then(data => data ? this.setState(data) : null);
  }

  render() {
    return (
      <div className={"gloss"}>{this.state.gloss ?
        <table>
          <tbody>
            <tr>
            {this.state.gloss.falavay.map((word, i) =>
              <td className="lauvinko" key={i}>{word}</td>
            )}
            </tr>
            <tr>
            {this.state.gloss.transcription.map((word, i) =>
              <td style={{fontStyle: "italic"}} key={i}>{word}</td>
            )}
            </tr>
            <tr>
            {this.state.gloss.outline.split(" ").map((word, i) =>
              <td className={"smalltext"} key={i}>{parse_outline(word)}</td>
            )}
            </tr>
            <tr>
              <td colSpan={this.state.gloss.transcription.length}>{this.state.translation}</td>
            </tr>
          </tbody>
        </table>
      : null}
      {this.state.status === "failed" ? <p>{"Failed: " + this.state.reason}</p> : null}
      </div>
    );
  }
}

export default Gloss;
export { InlineGloss, AugmentPair };