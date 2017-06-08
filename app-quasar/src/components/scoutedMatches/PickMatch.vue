<template>
    <div>
        <DrawerHead slot="header" :title="`${eventName} - Pick Match`" :backUrl="'/scout/view'" @openDrawerBody="$refs.drawer.$refs.drawer.open()"></DrawerHead>
        <DrawerBody ref="drawer"></DrawerBody>
        <div class="layout-padding">
            <div class="list">
                <ListItemMatch v-for="matchNumber in matchNumbers" :matchNumber="matchNumber" :eventCode="eventCode" :key="matchNumber"></ListItemMatch>
            </div>
        </div>
    </div>
</template>

<script>
    import { eventNames } from '../../statics/js/events.js'
    import DrawerHead from '../DrawerHead.vue'
    import DrawerBody from '../DrawerBody.vue'
    import ListItemMatch from './ListItemMatch.vue'
    import '../../store.js'

    export default {
        components: { DrawerHead, DrawerBody, ListItemMatch },
        mounted () {
            let self = this
            self.populateUniqueMatches()
        },
        computed: {
            eventName () {
                return eventNames[this.eventCode] || this.eventCode
            }
        },
        methods: {
            populateUniqueMatches () {
                let self = this
                let set = new Set()
                Object.keys(self.allMatches.matches).forEach(function (key) {
                    let match = self.allMatches.matches[key]
                    if (match.eventName === self.eventCode) {
                        set.add(match.matchNumber)
                    }
                })
                self.matchNumbers = Array.from(set)
            }
        },
        data () {
            return {
                allMatches: this.$select('matches'),
                eventCode: this.$route.params.eventCode,
                matchNumbers: []
            }
        }
    }
</script>
