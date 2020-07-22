# How to integrate Chatbot web client on a Joomla website 

1. Clone the following repository and execute the following:

```bash
$ cd rasa-webchat
$ npm run install
$ npm run build
```

2. Copy the file `lib/index.js` and paste it at the following location on your Joomla server:

```bash
scp lib/index.js root@<server-ip>:/var/www/html/ucuenca.edu.ec/public_html/chatbot.js
```

3. Open your Joomla Admin and Go to your `Template > Custom Code` section and apply the following custom code:

* Before \<\/body\>

```js
<div style="width: 400px; height: 2000px; border: 3px solid lightsalmon;" id="webchat" />
<script src="chatbot.js"  type="text/javascript"></script>

<script>
  WebChat.default.init({
    // embedded: true,
    selector: "#webchat",
    initPayload: "/greet",
    socketUrl: "http://127.0.0.1:5005/",
    tooltipPayload: "/utter_help",
    tooltipDelay: 40000,
    socketPath: "/socket.io/",
    customData: {
      language: 'en'
    },
    subtitle: '',
    inputTextFieldHint: "Type a message...",
    connectingText: "Waiting for server...",
    profileAvatar: "https://www.edina.com.ec/logos/1200104991-368427.jpg",
    hideWhenNotConnected: false,
  //   defaultHighlightAnimation: `@-webkit-keyframes default-botfront-blinker-animation {
  //     from {
  //     outline: solid rgba(255,0,0,0);
  //   }
  //   to {
  //     outline: solid red;
  //   }
  // }`,
    onSocketEvent: {
      'bot_uttered': () => console.log('bot uttered'),
    },
    showCloseButton: true,
    fullScreenMode: true,
    showFullScreenButton: true,
    docViewer: false,
    params: {
      images: {
        dims: {
          width: 300,
          height: 200
        }
      },
      storage: "local"
    }
  })
</script>
```

* Custom CSS

```css
img.rw-open-launcher {
    margin: 0 auto 5px;
}
```