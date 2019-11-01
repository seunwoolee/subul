const staticCacheName = "django-pwa-v" + new Date().getTime();
const filesToCache = [
    '../static/offline.html',
    '../static/css/coreui-icons.min.css',
    '../static/css/flag-icon.min.css',
    '../static/css/animate.css',
    '../static/css/simple-line-icons/css/simple-line-icons.css',
    '../static/css/select2/css/select2.min.css',
    '../static/css/fontawesome/css/all.css',
    '../static/css/fontawesome/webfonts/fa-solid-900.woff2',
    '../static/css/fontawesome/webfonts/fa-regular-400.woff2',
    '../static/css/style.css',
    '../static/DataTables/datatables.min.css',
    '../static/django_select2/django_select2.js',
    '../static/js/custom/hotkeys.min.js',
    '../static/popper.js/dist/umd/popper.min.js',
    '../static/bootstrap/dist/js/bootstrap.min.js',
    '../static/@coreui/coreui-pro/dist/js/coreui.min.js',
    '../static/DataTables_custom/datatables.net/js/jquery.dataTables.js',
    '../static/DataTables_custom/datatables.net-bs4/js/dataTables.bootstrap4.js',
    '../static/DataTables_custom/button.js',
    '../static/DataTables_custom/rowreorder.js',
    '../static/DataTables_custom/responsive.js',
    '../static/DataTables_custom/select.js',
    '../static/js/custom/datepicker.js',
    '../static/js/jquery/dist/jquery.min.js',
    '../static/favicon/android-icon-192x192.png',
    '../static/img/kcfeedLogoNew.gif',

    '../static/js/base.js',
    '../static/js/baseList.js',
    '../static/js/baseReg.js',

];


// Cache on install
self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
            .then(cache => {
                return cache.addAll(filesToCache);
            })
    )
});

// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                    .filter(cacheName => (cacheName !== staticCacheName))
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Serve from Cache
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                if(response) {
                    console.log('Static App shell', event.request.url);
                    return response
                } else {
                    console.log('Network Call', event.request.url);
                    return fetch(event.request);
                }

            })
            .catch(() => {
                return caches.match('/offline/');
            })
    )
});

