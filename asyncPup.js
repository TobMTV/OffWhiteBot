//------------------- Puppeteer.conf
const puppeteer = require('puppeteer');
const iPhone = puppeteer.devices['iPhone X'];
// ------------------- Server.conf
var sys = require("sys"),
my_http = require("http");
const request = require('request');
var fs = require('fs');
/*
function decode_utf8(s) {
  return decodeURIComponent(escape(s));
}

function getJSTodecrypt(){
  return new Promise(resolve => {
      setTimeout(() => {
        request
          .get('http://127.0.0.1:6050')
          .on('response', function(response) {
          console.log(response.statusCode) // 200
          console.log(response.headers['content-type']) // 'image/png'
          console.log(decode_utf8(response.toJSON()))
          })
        resolve('JS ricevuto');
      }, 10000);
  });
}

*/

async function timeout(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

(async () => {
  const browser = await puppeteer.launch({
    headless: false
  });
  const page = await browser.newPage();
  //await page.setCookie();
  await page.emulate(iPhone);
  await page.goto('https://www.off---white.com/en/IT/cart');
  await page.setRequestInterception(true)
  page.on('request', request => {
    var headers = request.headers();
    console.log(headers);
  })
  await page.screenshot({path: 'screenshot.png'})
  owCookies = await page._client.send('Network.getAllCookies');
  await page.close();
  
  //console.log(headers);
  //owCookies = await page.cookies();
  console.log(owCookies);
  console.log('====================================================================')
  // console.log(typeof owCookies);
  console.log(process.argv)
  //JS importa i cookies da OW e PY si collega e si scarica i cookies
  var requestToServer = 0;
  console.log('Server part:')
  async function serverCook(callback){
  my_http.createServer(function(request,response){
    console.log("sto dentro")
    if(requestToServer == 0){
    console.log("Rispondo per cookies");
    response.writeHeader(200, {"Content-Type": "application/json"});
    response.end(JSON.stringify(owCookies));
    }
    requestToServer++;
    console.log("Richieste :");
    console.log(requestToServer);
    if(requestToServer == 2){
      response.writeHeader(200, {"Content-Type": "application/json"});
      response.end();
      callback();
    }
    
  }).listen(process.argv[2]);
  }

  async function recuperoIPP(){
    var ippSign;
    console.log("sono prima dell'if");
      if(requestToServer == 2){
          console.log('IPP_SIGN in arrivo');
          //await page.setCacheEnabled(false);
          const page = await browser.newPage();
          await page.emulate(iPhone);
          await page.goto('file:///home/tob/Documents/OWBot/jsToDecrypt.html',{waitUntil: "load"});
          await page.waitFor(1000);
          page.on('dialog', async dialog => {
            ippSign = dialog.message();
            console.log(dialog.message());
            await dialog.dismiss();
            await browser.close();
            my_http.createServer(function(request,response){
              console.log("Rispondo per per ipp");
              response.writeHeader(200, {"Content-Type": "application/json"});
              response.end(JSON.stringify(ippSign));
          }).listen(process.argv[3]);
            });
      }
    
    
  }
  //serverC.close()
  //Se py mi sta dicendo che posso partire con il decrypt (se ho fatto una seconda richiesta)
  //var result = await getJSTodecrypt();
  serverCook(recuperoIPP);
  
})();