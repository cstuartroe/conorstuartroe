import Navbar from "./Navbar";
import SpinningGear from "./SpinningGear";
import Pipes from "./Pipes";

import "../static/scss/lander.scss";

export default function Home(_props: {}) {
  return (
    <div className={'lander-style'}>
      <Navbar/>
      <Pipes/>

      <div className="container-fluid">
        <div className="row">
          <div className="col-2 col-md-3"/>
          <div id="mainframe" className="col-8 col-md-6">
            <img className="circle" src="/static/img/conor.png" style={{width: 'min(40vw, 30vh)', height: 'min(40vw, 30vh)'}}/>
            <p style={{textAlign: "center"}}>
              I write software and make art, often at the same time. I currently work at{' '}
              <a href="https://www.academia.edu/">Academia.edu</a>.
            </p>
            <SpinningGear/>
          </div>
        </div>
      </div>
    </div>
  );
}