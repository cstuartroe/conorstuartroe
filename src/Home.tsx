import Navbar from "./Navbar";
import SpinningGear from "./SpinningGear";
import React from "react";

export default function Home(_props: {}) {
  return (
    <>
      <div className="col-2 col-md-3"/>
      <div className="col-8 col-md-6">
        <div id="mainframe">
          <img className="circle" src="/static/img/conor.jpg" style={{width: 'min(40vw, 30vh)', height: 'min(40vw, 30vh)'}}/>
          <p style={{textAlign: "center"}}>
            I write software and make art, often at the same time. I currently work at Google.
          </p>
          <SpinningGear/>
        </div>
      </div>
    </>
  );
}
