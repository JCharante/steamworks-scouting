<template>
    <div>
        <DrawerHead slot="header" title="Scouted Matches - Pick Event" @openDrawerBody="$refs.drawer.$refs.drawer.open()"></DrawerHead>
        <DrawerBody ref="drawer"></DrawerBody>
        <div class="layout-padding">
            <div class="list">
                <ListItemEvent v-for="event in events" :eventName="event" :key="event"></ListItemEvent>
            </div>
        </div>
    </div>
</template>

<script>
    import DrawerHead from '../DrawerHead.vue'
    import DrawerBody from '../DrawerBody.vue'
    import ListItemEvent from './ListItemEvent.vue'
    import * as matchActions from '../../actions/matches.js'
    import store from '../../store.js'

    export default {
        components: { DrawerHead, DrawerBody, ListItemEvent },
        mounted () {
            let self = this
            matchActions.deleteInvalidMatches(store, self.matches.matches)
            self.populateUniqueEvents()
        },
        methods: {
            populateUniqueEvents () {
                let self = this
                let set = new Set()
                Object.keys(self.matches.matches).forEach(function (key) {
                    let match = self.matches.matches[key]
                    set.add(match.eventName)
                })
                self.events = Array.from(set)
            }
        },
        data () {
            return {
                matches: this.$select('matches'),
                events: []
            }
        }
    }
</script>
