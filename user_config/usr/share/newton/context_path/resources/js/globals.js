const messenger  = (window.webkit) ? window.webkit.messageHandlers : (message) => {
    console.log("Message: " + message);
};

