import React, { Component } from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCloud, faSun, faLeaf, faSnowflake, faGlassCheers, faFrog } from "@fortawesome/free-solid-svg-icons";
import { range } from "./utils";

import "../static/scss/calendar.scss";

const WEEKDAYS = ['Sunday','Moonday','Mercuryday','Venusday','Earthday','Marsday','Jupiterday','Saturnday','Starday'];
const HOLIDAYS = ['Spring Equinox','Summer Solstice','Autumn Equinox','Winter Solstice',];
const SEASONS = ["Spring", "Summer", "Autumn", "Winter"];
const SEASON_ICONS = [faCloud, faSun, faLeaf, faSnowflake];
const WEEKEND_DAYS = [0, 1, 7, 8];

const FIRST_NEW_YEARS_DAY = new Date(2016, 2, 21, 0, 0, 0);
const FIRST_YEAR = 5362; // 21 Mar 2016 thru 30 March 2017

type Day = {
  season: number, // -1 for NYD, 0 for spring, so on (-2 for leap day)
  half: number,   // -1 for solstice/equinox, 0 for early, 1 for late
  date: number,   // 0-44 inclusive
}

function dayEq(day1: Day, day2: Day) {
  if (day1.season === -1) {
    return day2.season === -1;
  } else if (day1.half === -1) {
    return (day1.season === day2.season) && (day2.half === -1);
  } else {
    return (day1.season === day2.season) && (day1.half === day2.half) && (day1.date === day2.date);
  }
}

function isLeapYear(year: number) {
  return (year % 4 === 0) && ((year % 100 !== 0) || (year % 1000 === 0));
}

function addDays(date: Date, days: number) {
  let result = new Date(date);
  result.setDate(result.getDate() + days);
  return result;
}

function daysAfter(date1: Date, date2: Date) {
  return Math.floor((date1.getTime() - date2.getTime())/(1000*60*60*24));
}

function dayOfYear(days: number, leapYear: boolean): Day {
  if (leapYear) {
    if (days === 183) {
      return {
        season: -2,
        half: -1,
        date: -1,
      }
    } else if (days > 183) {
      days--;
    }
  }

  let season = Math.floor((days - 1) / 91);
  let dayOfSeason = (days - 1) % 91;
  let half = Math.floor((dayOfSeason - 1) / 45);
  let date = (dayOfSeason - 1) % 45;

  return {
    season,
    half,
    date,
  }
}

function getNewDate(date: Date) {
  let nyd = FIRST_NEW_YEARS_DAY, year = FIRST_YEAR;

  while (true) {
    let next_nyd = addDays(nyd, 365);

    if (isLeapYear(year)) {
      next_nyd = addDays(next_nyd, 1);
    }

    if (next_nyd > date) {
      return {
        year: year,
        day: dayOfYear(daysAfter(date, nyd), isLeapYear(year))
      };
    } else {
      nyd = next_nyd;
      year++;
    }
  }
}

function getMetricTime(date: Date) {
  const millisecondOfDay = date.getTime() % (24 * 60 * 60 * 1000);
  const metricSecondOfDay = Math.floor(millisecondOfDay / 864);
  return{
    hour: Math.floor(metricSecondOfDay/10000),
    minute: Math.floor((metricSecondOfDay % 10000)/100),
    second: metricSecondOfDay % 100,
  }
}

function gregorianDateToNewDate(gregorianDate: Date): CalendarState {
  return {
    ...getNewDate(gregorianDate),
    ...getMetricTime(gregorianDate),
  }
}

function dayToString(day: Day) {
  if (day.season === -1) {
    return "New Years' Day";
  } else if (day.season === -2) {
    return "Leap Day";
  } else if (day.half === -1) {
    return HOLIDAYS[day.season];
  } else {
    return WEEKDAYS[day.date % 9] + " " + (day.date + 1).toString() + "\xa0"
      + (day.half === 0 ? "Early\xa0" : "Late\xa0") + SEASONS[day.season];
  }
}

function DaySquare(props: { day: Day, currentDay: Day }) {
  let { day, currentDay } = props;

  let className = "weekday";
  if (day.season === -1 || day.half === -1 || WEEKEND_DAYS.includes(day.date % 9)) {
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
  } else if (day.half === -1) {
    content = <FontAwesomeIcon icon={SEASON_ICONS[day.season]}/>;
  }

  return (
    <div className={className}>
      <p>{content}</p>
    </div>
  );
}

function Month(props: {season: number, half: number, currentDay: Day}) {
  let { season, half, currentDay } = props;

  return (
    <table className="month">
      <tbody>
        {range(5).map(w => (
          <tr key={w} className="d-flex flex-row">
            {range(9).map(d => (
              <th key={d} className="flex-fill">
                <DaySquare day={{date: w*9 + d, season, half}} currentDay={currentDay}/>
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
                <DaySquare day={{season: index, half: -1, date: -1}} currentDay={currentDay}/>
              </th>
            </tr>
          </tbody>
        </table>
        <h2>{'Early ' + SEASONS[index]}</h2>
        <Month season={index} half={0} currentDay={currentDay}/>
        <h2>{'Late ' + SEASONS[index]}</h2>
        <Month season={index} half={1} currentDay={currentDay}/>
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

type CalendarState = {
  hour: number,
  minute: number,
  second: number,
  day: Day,
  year: number,
}

export default class NewCalendar extends Component<{}, CalendarState> {
  constructor(props: {}) {
    super(props);
    this.state = {
      hour: 0,
      minute: 0,
      second: 0,
      day: { date: -1, season: -1, half: -1 },
      year: 0,
    }
  }

  componentDidMount() {
    this.updateTime();
  }

  updateTime() {
    this.setState(gregorianDateToNewDate(new Date()));
    setTimeout(this.updateTime.bind(this), 86);
  }

  specialDay(season: number) {
    if (this.state.day.season === season) {
      let day = {
        season: season,
        half: -1,
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
        <div className='row' style={{padding: '1em',  backgroundColor: '#222218'}}>
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
