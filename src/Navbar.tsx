import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faHome, faBriefcase, faRocket, faLink } from "@fortawesome/free-solid-svg-icons";

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
        <Link to="/" className="flex-fill">
          <FontAwesomeIcon icon={faHome}/>
          About&nbsp;me
        </Link>
        <a href="/static/pdf/resume.pdf" className="flex-fill">
          <FontAwesomeIcon icon={faBriefcase}/>
          Resume
        </a>
        <Link to="/projects" className="flex-fill">
          <FontAwesomeIcon icon={faRocket}/>
          Projects
        </Link>
        <a href="https://linktr.ee/cstuartroe/" className="flex-fill">
          <FontAwesomeIcon icon={faLink}/>
          Links
        </a>
      </div>
    </header>
  );
}