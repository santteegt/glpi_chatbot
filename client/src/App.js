import React, { Component } from 'react';

// import { Widget } from 'react-chat-widget';
import { Widget } from 'rasa-webchat';

// import 'react-chat-widget/lib/styles.css';

import logo from './logo.svg';
import './App.css';

class App extends Component {      

  render() {
    return (
      <div className="App">
		<Widget
		 interval={1000}
		 initPayload={"/saludo"}
		 socketUrl={"http://localhost:5005"}
		 socketPath={"/socket.io/"}
		 customData={{"userId": "123"}} // arbitrary custom data. Stay minimal as this will be added to the socket
		 title={"DTIC"}
		 subtitle={"Mesa de Servicios Informáticos"}
		 inputTextFieldHint={"Escribe un mensaje..."}
		 connectingText={"Conectando con el servidor..."}
		 hideWhenNotConnected
		 showFullScreenButton
		 embedded={false}
		 openLauncherImage="chatlogo.png"
		 closeLauncherImage="chatlogo.png"
		 params={{
		   images: {
		     dims: {
		       width: 300,
		       height: 200
		     }
		   },
		   storage: "session"
		 }}
		 customComponent={ (messageData) => (<div>Custom React component</div>) }
		/>
      </div>
    );
  }
}

export default App;
