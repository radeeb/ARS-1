
var serverUrl = "http:/localhost:8080/visit";

var riveted = (function() {

    var started = false,
      stopped = false,
      turnedOff = false,
      clockTime = 0,
      startTime = new Date(),
      clockTimer = null,
      idleTimer = null,
      visitTime = 0,
      hiddenTimer,
      hiddenTime = 0,
      sendEvent,
      sendUserTiming,
      reportInterval,
      idleTimeout,
      nonInteraction,
      universalGA,
      classicGA,
      universalSendCommand,
      googleTagManager,
      rivetedClass,
      gaGlobal;

    function init(userRivetedClass, options) {

      rivetedClass = userRivetedClass || '';

      var element = $('#' + rivetedClass);

      options = options || {};
      reportInterval = parseInt(options.reportInterval, 10) || 5;
      idleTimeout = parseInt(options.idleTimeout, 10) || 30;
      gaGlobal = options.gaGlobal || 'ga';
      totalTimeEvent();
      addEvent();
      console.log("Hello from riveted.init()");

      if (typeof window[gaGlobal] === "function") {
        universalGA = true;
      }

      if (typeof _gaq !== "undefined" && typeof _gaq.push === "function") {
        classicGA = true;
      }

      if (typeof dataLayer !== "undefined" && typeof dataLayer.push === "function") {
        googleTagManager = true;
      }

      if ('gaTracker' in options && typeof options.gaTracker === 'string') {
        universalSendCommand = options.gaTracker + '.send';
      } else {
        universalSendCommand = 'send';
      }

      if (typeof options.eventHandler == 'function') {
        sendEvent = options.eventHandler;
      }

      if (typeof options.userTimingHandler == 'function') {
        sendUserTiming = options.userTimingHandler;
      }

      if ('nonInteraction' in options && (options.nonInteraction === false || options.nonInteraction === 'false')) {
        nonInteraction = false;
      } else {
        nonInteraction = true;
      }


      $(element).on('click', trigger); //jquery

      //addListener(document, 'click', trigger);
      // 'keydown click mousemove scroll'
      addListener(document, 'visibilitychange', visibilityChange);
      addListener(document, 'webkitvisibilitychange', visibilityChange);
    }

    function throttle(func, wait) {
      var context, args, result;
      var timeout = null;
      var previous = 0;
      var later = function() {
        previous = new Date;
        timeout = null;
        result = func.apply(context, args);
      };
      return function() {
        var now = new Date;
        if (!previous) previous = now;
        var remaining = wait - (now - previous);
        context = this;
        args = arguments;
        if (remaining <= 0) {
          clearTimeout(timeout);
          timeout = null;
          previous = now;
          result = func.apply(context, args);
        } else if (!timeout) {
          timeout = setTimeout(later, remaining);
        }
        return result;
      };
    }

    function addListener(element, eventName, handler) {
      if (element.addEventListener) {
        element.addEventListener(eventName, handler, false);
      }
      else if (element.attachEvent) {
        element.attachEvent('on' + eventName, handler);
      }
      else {
        element['on' + eventName] = handler;
      }
    }



    sendUserTiming = function (timingValue) {

      if (googleTagManager) {

        dataLayer.push({'event':'RivetedTiming', 'eventCategory':'Riveted', 'timingVar': 'First Interaction', 'timingValue': timingValue});

      } else {

        if (universalGA) {
          window[gaGlobal](universalSendCommand, 'timing', 'Riveted', 'First Interaction', timingValue);
        }

        if (classicGA) {
          _gaq.push(['_trackTiming', 'Riveted', 'First Interaction', timingValue, null, 100]);
        }

      }

    };

    sendEvent = function (time) {

      if (googleTagManager) {

        dataLayer.push({'event':'Riveted', 'eventCategory':'Riveted', 'eventAction': 'poop', 'eventLabel': time, 'eventValue': reportInterval, 'eventNonInteraction': nonInteraction});

      } else {

        if (universalGA) {
          window[gaGlobal](universalSendCommand, 'event', rivetedClass.toString(), 'Time Spent', time.toString(), reportInterval, {'nonInteraction': nonInteraction});
        }

        if (classicGA) {
          _gaq.push(['_trackEvent', 'Riveted', 'hello', time.toString(), reportInterval, nonInteraction]);
        }

      }

    };

    function setIdle() {
      clearTimeout(idleTimer);
      stopClock();
    }

    function visibilityChange() {
      if (document.hidden || document.webkitHidden) {
        setIdle();
        hiddenTimeEvent();
      }
    }

    function clock() {
      clockTime += 1;
      if (clockTime > 0 && (clockTime % reportInterval === 0)) {
        sendEvent(clockTime);
      }

    }

    function stopClock() {
      stopped = true;
      clearTimeout(clockTimer);
    }

    function turnOff() {
      setIdle();
      turnedOff = true;
    }

    function turnOn() {
      turnedOff = false;
    }

    function restartClock() {
      stopped = false;
      clearTimeout(clockTimer);
      clockTimer = setInterval(clock, 1000);
      clearTimeout(hiddenTimer);

    }

    function startRiveted() {

      var currentTime = new Date();
      var diff = currentTime - startTime;


      started = true;


      sendUserTiming(diff);


      clockTimer = setInterval(clock, 1000);

    }

    function resetRiveted() {
      startTime = new Date();
      clockTime = 0;
      started = false;
      stopped = false;
      clearTimeout(clockTimer);
      clearTimeout(idleTimer);
    }

    function trigger() {
      console.log("Hello from trigger");
      if (turnedOff) {
        return;
      }

      if (!started) {
        startRiveted();
        console.log("Hello from startRiveted");
      }

      if (stopped) {
        restartClock();
      }

      clearTimeout(idleTimer);
      idleTimer = setTimeout(setIdle, idleTimeout * 1000 + 100);
    }

    return {
      init: init,
      trigger: trigger,
      setIdle: setIdle,
      on: turnOn,
      off: turnOff,
      reset: resetRiveted
    };

    function totalTimeEvent() {
        //console.log("Hello from total time event");
  setTimeout(totalTime, 1000);
  };

function hiddenTimeEvent() {
    hiddenTimer = setTimeout(totalIdleTime, 1000);
  };


function totalTime() {
  visitTime = visitTime + 1;
  console.log(visitTime);
  totalTimeEvent();
};

function totalIdleTime() {
  hiddenTime = hiddenTime + 1;
  hiddenTimeEvent();
};

function getKeywords() {
  //
  var keywords = ['sports', 'money'];
  return keywords;
}

function addEvent() {
  console.log("Hello from addEvent outside");

  //called before resources of page unloads
  window.addEventListener("beforeunload", function (event) {

  //to display a confirm alert uncomment the line below
  event.returnValue = "Are you sure?";

  console.log("Hello from addEvent");
  var activeRatio = Math.floor((clockTime / visitTime) * 100);
  console.log("Active Ratio: ", activeRatio);
  console.log("ClockTime: ", clockTime);
  console.log("VisitTime: ", visitTime);

  var visibleTime = visitTime - hiddenTime;
  var focusRatio = Math.floor((visibleTime / visitTime) * 100);
  console.log("focusRatio:", focusRatio);
  console.log("visibleTime", visibleTime);
  console.log("VisitTime: ", visitTime);
  console.log("hiddenTime:", hiddenTime);
  console.log("totalIdleTime:", totalIdleTime);

  window[gaGlobal](universalSendCommand, 'event', rivetedClass.toString(), 'Active', activeRatio.toString(), 1, {'nonInteraction': nonInteraction});
  window[gaGlobal](universalSendCommand, 'event', rivetedClass.toString(), 'Focus', focusRatio.toString(), 1, {'nonInteraction': nonInteraction});
  sendDataToWebServer();  
  return undefined;

}); //end of window unload call
};

function sendDataToWebServer() {
  var keywords = getKeywords();
	var aR = Math.floor((clockTime / visitTime) * 100);
	var visiableTime = visitTime - hiddenTime;
  var fR = Math.floor((visiableTime / visitTime) * 100);
  var outputData = {'url': window.location.pathname, 'keywords': keywords, 'activeRatio' : aR, 'FocusRatio' : fR};

  outputData = JSON.stringify(outputData);
  console.log(outputData);
  //website needs jquery 
  $.ajax({url: serverUrl,
  type: "POST",
  contentType: "application/json",
  data: outputData,
  error: function(xhr, status, err){
    console.log(err);
  }
  });
  console.log("sent data to server");
}


  })();
