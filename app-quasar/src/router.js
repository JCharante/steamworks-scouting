import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

function load (component) {
    return () => System.import(`components/${component}.vue`)
}

export default new VueRouter({
    /*
     * NOTE! VueRouter "history" mode DOESN'T works for Cordova builds,
     * it is only to be used only for websites.
     *
     * If you decide to go with "history" mode, please also open /config/index.js
     * and set "build.publicPath" to something other than an empty string.
     * Example: '/' instead of current ''
     *
     * If switching back to default "hash" mode, don't forget to set the
     * build publicPath back to '' so Cordova builds work again.
     */

    routes: [
        { path: '/scout/view', component: load('scoutedMatches/layout') },
        { path: '/scout/new', component: load('scout/NewMatch') },
        { path: '/scout/edit/:matchID',
            component: load('scout/layout'),
            children: [
                {path: '', component: load('scout/PreMatch')},
                {path: 'auto', component: load('scout/Auto')},
                {path: 'teleop', component: load('scout/Teleop')},
                {path: 'after_match', component: load('scout/AfterMatch')}
            ]
        },
        { path: '/demo',
            component: load('demo/layout'),
            children: [
                {path: '', component: load('demo/TabOne')},
                {path: 'tabtwo', component: load('demo/TabTwo')}
            ]
        },
        { path: '/soundboard', component: load('SoundBoard') },
        { path: '/', component: load('Index') }, // Default
        { path: '*', component: load('Error404') } // Not found
    ]
})
