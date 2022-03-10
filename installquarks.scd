var args = thisProcess.argv;
var failed = false;
args.do{|qName|
    "Installing Quark: %".format(qName).postln;
    {
        Quarks.install(qName);
    }.try({
        "Failed to install %".format(qName).error;
        failed = true;
    });

};

failed.asInteger.exit;
