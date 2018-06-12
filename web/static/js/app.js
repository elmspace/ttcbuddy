// Register Service Worker
if ('serviceWorker' in navigator) {
    navigator.serviceWorker
    .register('/static/service-worker.js')
    .then(function(registration) {
        console.log('Service Worker Registered');
        return registration;
    })
    .catch(function(err) {
        console.error('Unable to register service worker.', err);
    });
}