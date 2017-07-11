<template>
    <q-layout ref="layout">
        <drawer-head slot="header" title="Settings" @toggleLeft="$refs.layout.toggleLeft()"></drawer-head>
        <drawer-body slot="left"></drawer-body>
        <div class="layout-view">
            <div class="layout-padding">
                <q-list>
                    <q-list-header>Settings</q-list-header>
                    <q-item>
                        <q-item-main>
                            <q-field icon="face">
                                <q-input float-label="Your Name:" v-model="scoutName"></q-input>
                            </q-field>
                        </q-item-main>
                    </q-item>
                    <q-item>
                        <q-item-main>
                            <q-field icon="pregnant_woman">
                                <q-input type="url" float-label="Server Address" v-model="serverAddress"></q-input>
                            </q-field>
                        </q-item-main>
                    </q-item>
                    <q-item>
                        <q-item-main>
                            <q-field icon="lock">
                                <q-input type="password" float-label="Server Password" v-model="serverPassword"></q-input>
                            </q-field>
                        </q-item-main>
                    </q-item>
                    <q-item>
                        <q-item-main>
                            <q-field icon="business">
                                <q-select float-label="Event:" class="full-width" type="radio" v-model="defaultEventCode" :options="selectOptions.eventName"></q-select>
                            </q-field>
                        </q-item-main>
                    </q-item>
                </q-list>
                <br>
                <div class="group">
                    <q-btn class="full-width" color="info" @click="testConnection">Test Connection</q-btn>
                    <q-btn class="full-width" color="primary" @click="save">Save</q-btn>
                </div>
            </div>
        </div>
    </q-layout>
</template>

<script>
    import {
        dom,
        event,
        openURL,
        QLayout,
        QField,
        QInput,
        QToolbar,
        QToolbarTitle,
        QBtn,
        QIcon,
        QList,
        QListHeader,
        QItem,
        QItemSide,
        QItemMain,
        QKnob,
        QRadio,
        Toast,
        QSelect
    } from 'quasar'
    import DrawerHead from './Drawer/Head.vue'
    import DrawerBody from './Drawer/Body.vue'
    import { store, writeStoresToDisk } from '../store.js'
    import { setDefaultEvent, setScoutName, setServerPassword, setServerAddress } from '../statics/js/settings.js'
    import { events } from '../statics/js/events.js'

    export default {
        components: {
            dom,
            event,
            openURL,
            QLayout,
            QField,
            QInput,
            QToolbar,
            QToolbarTitle,
            QBtn,
            QIcon,
            QList,
            QListHeader,
            QItem,
            QItemSide,
            QItemMain,
            QKnob,
            QSelect,
            QRadio,
            DrawerHead,
            DrawerBody
        },
        methods: {
            save () {
                store.dispatch(setDefaultEvent(this.defaultEventCode))
                store.dispatch(setScoutName(this.scoutName))
                store.dispatch(setServerPassword(this.serverPassword))
                store.dispatch(setServerAddress(this.serverAddress))
                writeStoresToDisk()
                Toast.create.positive('Saved Settings')
            },
            testConnection () {
                Toast.create.negative('Not yet Implemented')
            }
        },
        data () {
            return {
                serverAddress: this.$select('settings.serverAddress'),
                scoutName: this.$select('settings.scoutName'),
                serverPassword: this.$select('settings.serverPassword'),
                defaultEventCode: this.$select('settings.defaultEvent'),
                selectOptions: {
                    eventName: events
                }
            }
        }
    }
</script>
