function getDeviceType() {
    const userAgent = navigator.userAgent;
    
    if (/mobile/i.test(userAgent)) {
      return 'Mobile Device';
    } else if (/tablet/i.test(userAgent)) {
      return 'Tablet Device';
    } else {
      return 'Desktop Device';
    }
  }
  
  // Function to get the browser name
  function getBrowserName() {
    const userAgent = navigator.userAgent;
    const browsers = {
      chrome: /chrome/i,
      safari: /safari/i,
      firefox: /firefox/i,
      edge: /edge/i,
      opera: /opera|OPR/i,
      ie: /msie|trident/i
    };
    
    for (const browser in browsers) {
      if (browsers[browser].test(userAgent)) {
        return browser;
      }
    }
    
    return 'Unknown Browser';
  }
  
  // Usage example
  const deviceType = getDeviceType();
  const browserName = getBrowserName();




  var currentDate = new Date();
  // Format the date and time
  var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
  var formattedDate = currentDate.toLocaleDateString(undefined, options);
  var formattedTime = currentDate.toLocaleTimeString();



// Update Labels 
var deviceTypeInput = document.getElementById("device-type");
var browserTypeInput = document.getElementById("browser-type");
var loginDateInput = document.getElementById("login-date");
function updateLabels() {
    deviceTypeInput.value =  deviceType
    browserTypeInput.value = browserName
    loginDateInput.value = formattedDate + ' - ' + formattedTime
}
updateLabels()
