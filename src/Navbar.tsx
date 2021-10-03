import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faHome, faBriefcase, faRocket, faLink } from "@fortawesome/free-solid-svg-icons";

export default function Navbar(_props: {}) {
  return (
    <header id="navbar">
      <div className="pagelinks d-flex flex-row">
        <a href="/" className="flex-fill">
          <FontAwesomeIcon icon={faHome}/>
          About&nbsp;me
        </a>
        <a href="/static/pdf/resume.pdf" className="flex-fill">
          <FontAwesomeIcon icon={faBriefcase}/>
          Resume
        </a>
        <a href="/projects" className="flex-fill">
          <FontAwesomeIcon icon={faRocket}/>
          Projects
        </a>
        <a href="https://linktr.ee/cstuartroe/" className="flex-fill">
          <FontAwesomeIcon icon={faLink}/>
          Links
        </a>
      </div>
    </header>
  );
}