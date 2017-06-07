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
                            <q-select class="full-width" type="radio" v-model="defaultEventName" :options="selectOptions.eventName"></q-select>
                        </div>
                    </div>
                </div>

                <button class="full-width primary" @click="save">Save</button>
            </div>
        </div>
    </q-layout>
</template>

<script>
    import DrawerHead from './DrawerHead.vue'
    import DrawerBody from './DrawerBody.vue'
    // import '../store.js'
    // import * as matchActions from '../actions/matches.js'
    import { events } from '../statics/js/events.js'
    import { Toast } from 'quasar'

    export default {
        components: { DrawerHead, DrawerBody },
        methods: {
            save () {
                Toast.create.negative('Not yet Implemented')
            }
        },
        data () {
            return {
                scoutName: '',
                serverPassword: '',
                defaultEventName: null,
                selectOptions: {
                    eventName: events
                }
            }
        }
    }
</script>
