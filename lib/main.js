/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this file,
 * You can obtain one at http://mozilla.org/MPL/2.0/. */

const {Cc,Ci,Cr} = require("chrome");
const windows = require("window-utils");
const brainwave = require("brainwave.js");
const timers = require("timers");
const {Hotkey} = require("hotkeys");
 
var current_url;

const OPEN_FLAGS = {
    RDONLY: parseInt("0x01"),
    WRONLY: parseInt("0x02"),
    CREATE_FILE: parseInt("0x08"),
    APPEND: parseInt("0x10"),
    TRUNCATE: parseInt("0x20"),
    EXCL: parseInt("0x80")
};

const Logger = {
    init: function() {
        var file = Cc["@mozilla.org/file/directory_service;1"].getService(Ci.nsIProperties).get("Desk", Ci.nsIFile);  
        file.append("brainwave.log");
        Logger.out = Cc['@mozilla.org/network/file-output-stream;1'].createInstance(Ci.nsIFileOutputStream);
        Logger.out.init(file, OPEN_FLAGS.CREATE_FILE | OPEN_FLAGS.WRONLY | OPEN_FLAGS.APPEND, parseInt("0777"), false);
    },
    
    log: function(line) {
        console.log(line);
        line += "\n";
        Logger.out.write(line, line.length);
    }
}

function observe() {
    if (!windows.activeWindow.gBrowser) {
        timers.setTimeout(observe, 100);
        return;
    }
    var url = windows.activeWindow.gBrowser.currentURI.spec;
    if (current_url != url) {
        current_url = url;
        Logger.log("1,"+url);
    }

    var packetCount = brainwave.readPackets();
    if (packetCount > 0) {
        var attention = brainwave.getAttention();
        var meditation = brainwave.getMeditation();
        var delta = brainwave.getDelta();
        var theta = brainwave.getTheta();
        var lowAlpha = brainwave.getLowAlpha();
        var highAlpha = brainwave.getHighAlpha();
        var lowBeta = brainwave.getLowBeta();
        var highBeta = brainwave.getHighBeta();
        var lowGamma = brainwave.getLowGamma();
        var highGamma = brainwave.getHighGamma();
        Logger.log("2,"+attention+","+meditation+","+delta+","+theta+","+lowAlpha+","+highAlpha+","+lowBeta+","+highBeta+","+lowGamma+","+highGamma);
    }

    timers.setTimeout(observe, 100);
}

Hotkey({
    combo: "accel-l",
    onPress: function() {
        Logger.log("3,");
    }
});


Logger.init();
brainwave.open();
observe();