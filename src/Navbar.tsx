import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faHome, faBriefcase, faRocket, faLink } from "@fortawesome/free-solid-svg-icons";
import { IconDefinition } from "@fortawesome/fontawesome-svg-core";

type PagelinkProps = {
  icon: IconDefinition,
  to: string
  text: string,
  inReact: boolean,
}

function Pagelink({icon, to, inReact, text}: PagelinkProps) {
  const content = <>
    <FontAwesomeIcon icon={icon}/>
    <br/>
    {text}
  </>;

  if (inReact) {
    return (
      <Link to={to} className="pagelink">
        {content}
      </Link>
    );
  } else {
    return (
      <a href={to} className="pagelink">
        {content}
      </a>
    );
  }
}

export default function Navbar(_props: {}) {
  return (
    <header id="navbar" style={{
      position: 'fixed',
      width: '100vw',
      top: 0,
      left: 0,
      zIndex: 1,
    }}>
      <div className="pagelinks d-flex flex-row">
        <Pagelink icon={faHome} to={'/'} inReact={true} text={'index'}/>
        <Pagelink icon={faBriefcase} to={'/static/pdf/resume.pdf'} inReact={false} text={'resume'}/>
        <Pagelink icon={faRocket} to={'/projects'} inReact={true} text={'projects'}/>
        <Pagelink icon={faLink} to={'https://linktr.ee/cstuartroe'} inReact={false} text={'links'}/>
      </div>
    </header>
  );
}