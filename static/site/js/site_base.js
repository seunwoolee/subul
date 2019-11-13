Date.prototype.yyyymmdd = function() {
  var mm = this.getMonth() + 1; // getMonth() is zero-based
  var dd = this.getDate();

  return [this.getFullYear(),
          (mm>9 ? '' : '0') + mm,
          (dd>9 ? '' : '0') + dd
         ].join('-');
};

function displayConfirmNotification() {
    let options = {
        body: '사용자가 알림을 허용했습니다. 조아요!',
        icon: '/src/images/icons/app-icon-96x96.png',
        badge: '/src/images/icons/app-icon-96x96.png',
        image: '/src/images/sf-boat.jpg',
        dif: 'ltr',
        lang: 'ko-KR',
        vibrate: [100, 50, 200],
        tag: 'confirm-notification',
        renotify: true,
        actions: [
            { action: 'confirm', title: 'Okay', icon: '/src/images/icons/app-icon-96x96.png'},
            { action: 'cancel', title: 'Cancel', icon: '/src/images/icons/app-icon-96x96.png'},
        ]
    };
    // 일반 js에서 notification
    // new Notification('알림 허용.',options);

    // 서비스 워커에서 notification
    navigator.serviceWorker.ready
        .then(swreg => {
            swreg.showNotification('알림허용ddddd', options);
        });
}

function configurePushSub() {
    if(!('serviceWorker' in navigator)) {
        return;
    }

    let reg;
    navigator.serviceWorker.ready
        .then((swreg) =>{
            reg = swreg;
            return swreg.pushManager.getSubscription();
        })
        .then((sub) => {
            if (sub === null) {
                // Create a new subscription
                reg.pushManager.subscribe({
                    userVisibleOnly: true
                });
            } else {
                // We have a subscription
            }
        })


}

function askForNotificationPermission(){
    Notification.requestPermission( result => {
        console.log('User chice', result);
        if(result === 'granted') {
            configurePushSub();
        }
    });
}

askForNotificationPermission();
