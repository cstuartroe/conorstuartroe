import React, { Component } from "react";
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCloud, faSun, faLeaf, faSnowflake, faGlassCheers, faFrog } from "@fortawesome/free-solid-svg-icons";
import { range } from "../utils";
import {
  Day,
  NewDateTime,
  WEEKEND_DAYS,
  SEASONS,
  HOLIDAYS,
  MONTHS,
  gregorianDateToNewDate,
  dayToString,
  dayEq,
} from "./utils";

import "../../static/scss/calendar.scss";

const MONTH_SYMBOLS = ['♈︎', '♉︎', '♊︎', '♋︎', '♌︎', '♍︎', '♎︎', '♏︎', '♐︎', '♑︎', '♒︎', '♓︎'];
const SEASON_ICONS = [faCloud, faSun, faLeaf, faSnowflake];

function DaySquare(props: { day: Day, currentDay: Day }) {
  let { day, currentDay } = props;

  let className = "weekday";
  if (day.season === -1 || day.month === -1 || WEEKEND_DAYS.includes(day.date % 10)) {
    className = "weekend";
  }

  if (dayEq(day, currentDay)) {
    className += ' activeDay';
  }

  let content: string | JSX.Element = (day.date + 1).toString();
  if (day.season === -1) {
    content = <FontAwesomeIcon icon={faGlassCheers}/>;
  } else if (day.season === -2) {
    content = <FontAwesomeIcon icon={faFrog}/>;
  } else if (day.month === -1) {
    content = <FontAwesomeIcon icon={SEASON_ICONS[day.season]}/>;
  }

  return (
    <div className={className}>
      <p>{content}</p>
    </div>
  );
}

function Month(props: {season: number, month: number, currentDay: Day}) {
  let { season, month, currentDay } = props;

  return (
    <table className="month">
      <tbody>
        {range(3).map(w => (
          <tr key={w} className="d-flex flex-row">
            {range(10).map(d => (
              <th key={d} className="flex-fill">
                <DaySquare day={{date: w*10 + d, season, month}} currentDay={currentDay}/>
              </th>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

type SeasonProps = {
  currentDay: Day,
  index: number,
}

function Season(props: SeasonProps) {
  let { currentDay, index } = props;

  return (
    <div className='col-12 col-md-6 season-wrapper'>
      <div className='season' id={SEASONS[index]}>
        <h2>{HOLIDAYS[index]}</h2>
        <table className='month'>
          <tbody>
            <tr>
              <th>
                <DaySquare day={{season: index, month: -1, date: -1}} currentDay={currentDay}/>
              </th>
            </tr>
          </tbody>
        </table>
        {range(3).map(month => (
          <div key={month}>
            <h2>{MONTHS[index*3 + month]} {MONTH_SYMBOLS[index*3 + month]}</h2>
            <Month season={index} month={month} currentDay={currentDay}/>
          </div>
        ))}
      </div>
    </div>
  );
}

function lpad(s: string, width: number, padding: string) {
  while (s.length < width) {
    s += padding;
  }

  return s;
}

export default class NewCalendar extends Component<{}, NewDateTime> {
  private __is_mounted: boolean;

  constructor(props: {}) {
    super(props);
    this.__is_mounted = false;
    this.state = {
      hour: 0,
      minute: 0,
      second: 0,
      day: { date: -1, season: -1, month: -1 },
      year: 0,
    }
  }

  componentDidMount() {
    this.__is_mounted = true;
    this.updateTime();
  }

  componentWillUnmount() {
    this.__is_mounted = false;
  }

  updateTime() {
    if (!this.__is_mounted) {
      return;
    }

    this.setState(gregorianDateToNewDate(new Date()));
    setTimeout(this.updateTime.bind(this), 86);
  }

  specialDay(season: number) {
    if (this.state.day.season === season) {
      let day = {
        season: season,
        month: -1,
        date: -1,
      };

      return (
        <div className='col-12 season-wrapper'>
          <div className='season' id='new-year'>
            <h2>{dayToString(day)}</h2>
            <table className='month'>
              <tbody>
              <tr>
                <th>
                  <DaySquare day={day} currentDay={this.state.day}/>
                </th>
              </tr>
              </tbody>
            </table>
          </div>
        </div>
      );
    } else {
      return null;
    }
  }

  render() {
    return (
      <div className='container-fluid'>
        <div className='row'>
          <div className='col-12'>
            <h1 id='current'>
              {this.state.hour}
              {':'}
              {lpad(this.state.minute.toString(), 2, '0')}
              {':'}
              {lpad(this.state.second.toString(), 2, '0')}
              {' '}
              {dayToString(this.state.day)}
              {'\xa0'}
              {this.state.year}
            </h1>
          </div>
          <div className='col-12 explanation'>
            <p style={{textAlign: 'center'}}>
              <Link to={'/new_calendar/explanation'}>explanation</Link>
            </p>
          </div>

          {this.specialDay(-1)}
          {[0, 1].map(s => (
            <Season key={s} currentDay={this.state.day} index={s}/>
          ))}
          {this.specialDay(-2)}
          {[2, 3].map(s => (
            <Season key={s} currentDay={this.state.day} index={s}/>
          ))}
        </div>
      </div>
    );
  }
}
