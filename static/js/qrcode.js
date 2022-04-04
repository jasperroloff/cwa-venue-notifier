import QrScanner from "qr-scanner";

const videoElem = document.getElementById('qrcode-scanner-video');

const qrScanner = new QrScanner(videoElem, async result => {
    if (result) {
        qrScanner.stop();
        await fetch("/api/locations/", {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({url: result}),
        }).then(res => res.json()).then(res => {
            alert(res.description + "\n" + res.address);
            qrScanner.start();
        });
    }
});

qrScanner.start();
