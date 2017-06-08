<template>
    <q-layout>
        <DrawerHead slot="header" title="Settings" @openDrawerBody="$refs.drawer.$refs.drawer.open()"></DrawerHead>
        <DrawerBody ref="drawer"></DrawerBody>
        <div class="layout-view">
            <div class="layout-padding">
                <div class="list">
                    <div class="list-label">Settings</div>
                    <div class="item two-lines">
                        <i class="item-primary">face</i>
                        <div class="item-content">
                            <input placeholder="Your Name" class="full-width" v-model="scoutName">
                        </div>
                    </div>
                    <div class="item two-lines">
                        <i class="item-primary">pregnant_woman</i> <!-- If anyone Asks, it's because it represents the mothership -->
                        <div class="item-content">
                            <input placeholder="Server Address" class="full-width" v-model="serverAddress">
                        </div>
                    </div>
                    <div class="item two-lines">
                        <i class="item-primary">lock</i>
                        <div class="item-content">
                            <input placeholder="Server Password" class="full-width" v-model="serverPassword">
                        </div>
                    </div>
                    <div class="item two-lines">
                        <i class="item-primary">business</i>
                        <div class="item-content row items-center">
                            <label style="margin-right: 10px;">Event:</label>
                            <br>
                            <q-select class="full-width" type="radio" v-model="defaultEventCode" :options="selectOptions.eventName"></q-select>
                        </div>
                    </div>
                </div>
                <div class="group">
                    <button class="full-width info" @click="testConnection">Test Connection</button>
                    <button class="full-width primary" @click="save">Save</button>
                </div>
            </div>
        </div>
    </q-layout>
</template>

<script>
    import DrawerHead from './DrawerHead.vue'
    import DrawerBody from './DrawerBody.vue'
    import { store, writeStoresToDisk } from '../store.js'
    import { setDefaultEvent, setScoutName, setServerPassword, setServerAddress } from '../statics/js/settings.js'
    import { events } from '../statics/js/events.js'
    import { Toast } from 'quasar'

    export default {
        components: { DrawerHead, DrawerBody },
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
