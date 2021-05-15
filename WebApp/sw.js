self.addEventListener('activate', async () => {
    console.log('ServiceWorker activate')
})

self.addEventListener('notificationclick', function (event) {
    console.log('Notification click detected');
    // This looks to see if the tab is already open and
    // focuses if it is
    const urlToOpen = new URL('', self.location.origin).href;
    console.log('Opening ' + urlToOpen);
    const promiseChain = clients.matchAll({
        type: 'window',
        includeUncontrolled: true
    }).then((windowClients) => {
        let matchingClient = null;
        for (let i = 0; i < windowClients.length; i++) {
            const windowClient = windowClients[i];
            if (windowClient.url === urlToOpen) {
                matchingClient = windowClient;
                break;
            }
        }
        if (matchingClient) {
            return matchingClient.focus();
        } else {
            return clients.openWindow(urlToOpen);
        }
    });
    event.waitUntil(promiseChain);
});

// References
// https://developers.google.com/web/fundamentals/push-notifications/common-notification-patterns#focus_an_existing_window
// https://notifications.spec.whatwg.org/#using-actions
// https://developer.mozilla.org/en-US/docs/Web/API/WindowClient/focus