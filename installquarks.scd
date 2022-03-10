var args = thisProcess.argv;
args.do{|qName|
    var thisquark;
    "Installing Quark: %".format(qName).postln;
    thisquark = Quarks.install(qName);
    if(thisquark.isInstalled.not, { "Failed to install %".format(qName).error; 1.exit})
};

0.exit;
