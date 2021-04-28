import React, { Component } from "react";
import Tweet, { TweetType } from "./Tweet";

type Props = {}
type State = {
  tweets: TweetType[],
  loading: boolean,
  error: null | string,
}

export default class TwitterMirror extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      tweets: [],
      loading: false,
      error: null,
    }
  }

  componentDidMount() {
    this.fetchTweets();
  }

  fetchTweets() {
    this.setState({loading: true});

    fetch('/tweetlist')
      .then(res => res.json())
      .then(data => this.setState({tweets: data, loading: false}))
      .catch(error => this.setState({error}))

    setTimeout(this.fetchTweets.bind(this), 60000);
  }

  render() {
    let { tweets, loading, error } = this.state;

    return (
      <div className="container">
        <div className="row">
          {
            loading ?
              <img src='/static/img/twitter-spinner.gif' alt='loading'/>
              : null
          }

          {error ? <div>{error}</div> : null}

          <div className="col-md-2 col-sm-1 col-0"/>
          <div className="tweet-list col-md-8 col-sm-10 col-12">
            {tweets.map(t => <Tweet tweet={t} key={t.id}/>)}
          </div>
        </div>
      </div>
    );
  }
}
