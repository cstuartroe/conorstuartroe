import React from "react";

export default function NotFound(_props: {}) {
  return (
    <>
      <div className="col-2 col-md-3"/>
      <div className="col-8 col-md-6">
        <div className={'lander-plate'} style={{marginTop: '30vh', width:'100%'}}>
          <p style={{textAlign: 'center', paddingBottom: 0}}>
            Woah, hold your horses there, partner. This ain't a page.
          </p>
        </div>
      </div>
    </>
  );
}