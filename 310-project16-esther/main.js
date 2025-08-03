const { app, BrowserWindow } = require('electron');

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600
  });

  win.loadFile('home.html'); // Make sure you have index.html too
}

app.whenReady().then(createWindow);
