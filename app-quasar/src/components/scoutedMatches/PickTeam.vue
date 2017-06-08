<template>
    <div>
        <DrawerHead slot="header" :title="`${eventName} - Q${matchNumber} - Matches`" :backUrl="`/scout/view/event/${eventCode}`" @openDrawerBody="$refs.drawer.$refs.drawer.open()"></DrawerHead>
        <DrawerBody ref="drawer"></DrawerBody>
        <div class="layout-padding">
            <div class="list">
                <ListItemTeam v-for="matchID in matchIDs" @updateList="populateUniqueTeams()" :matchID="matchID" :key="matchID"></ListItemTeam>
            </div>
        </div>
    </div>
</template>

<script>
    import { eventNames } from '../../statics/js/events.js'
    import DrawerHead from '../DrawerHead.vue'
    import DrawerBody from '../DrawerBody.vue'
    import ListItemTeam from './ListItemTeam.vue'
    import '../../store.js'

    export default {
        components: { DrawerHead, DrawerBody, ListItemTeam },
        mounted () {
            let self = this
            self.populateUniqueTeams()
        },
        computed: {
            eventName () {
                return eventNames[this.eventCode] || this.eventCode
            }
        },
        methods: {
            populateUniqueTeams () {
                let self = this
                self.matchIDs = []
                Object.keys(self.$select('matches').matches).forEach(function (key) {
                    let match = self.$select('matches').matches[key]
                    if (match.eventName === self.eventCode && match.matchNumber === self.matchNumber) {
                        self.matchIDs.push(match.matchID)
                    }
                })
            }
        },
        data () {
            return {
                eventCode: this.$route.params.eventCode,
                matchNumber: parseInt(this.$route.params.matchNumber),
                matchIDs: []
            }
        }
    }
</script>
