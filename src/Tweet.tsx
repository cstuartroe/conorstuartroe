import React, { Component } from "react";

import "../static/scss/tweets.scss";

export type TwitterUser = {
  handle: string,
  name: string,
  pic: string,
}

export type TweetType = {
  id: number,
  created_at: string,
  author: TwitterUser,
  text?: string,
  retweeted_status?: TweetType,
}

type Props = {
  tweet: TweetType,
}
type State = {}

export default class Tweet extends Component<Props, State>{
  constructor(props: Props) {
    super(props);
  }

  render() {
    let { tweet } = this.props;

    return (
      <div className="tweet">
        <div className="prof-pic">
          <img src={tweet.author.pic} alt={tweet.author.handle}/>
        </div>
        <div className="tweet-right">
          <div className="tweet-author-info">
            <div className="tweet-author-name">
              {tweet.author.name}
            </div>
            <div className="tweet-author-handle">
              {tweet.author.handle}
            </div>
          </div>
          {
            tweet.text ?
              <div className="tweet-text">
                {tweet.text}
              </div>
              : null
          }
          {
            tweet.retweeted_status ?
              <Tweet tweet={tweet.retweeted_status}/>
              : null
          }
        </div>
      </div>
    );
  }
}
