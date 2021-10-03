import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCog } from "@fortawesome/free-solid-svg-icons";

export default function SpinningGear(_props: {}) {
  return (
    <div className={'spinning-gear'}>
      <hr style={{
        height: 0,
        margin: '20px 10vw',
        padding: '4.5px 0',
        borderTop: '2px dashed white',
        textAlign: 'center',
      }}/>
      <FontAwesomeIcon icon={faCog} style={{
        // '-webkit-animation': 'fa-spin 5s infinite linear',
        animation: 'fa-spin 5s infinite linear',
        display: 'inline-block',
        position: 'relative',
        padding: '5px',
        borderRadius: '50%',
        color: 'white',
        top: '-42px',
        fontSize: '25px',
      }}/>
    </div>
  );
}