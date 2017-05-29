<template>
    <div class="layout-padding">
        <div class="list">
            <ListItemTeam v-for="matchID in matchIDs" @updateList="populateUniqueTeams()" :matchID="matchID" :matchNumber="matchNumber" :eventName="eventName" :key="matchID"></ListItemTeam>
        </div>
    </div>
</template>

<script>
    import ListItemTeam from './ListItemTeam.vue'
    import '../../store.js'

    export default {
        components: {
            'ListItemTeam': ListItemTeam
        },
        mounted () {
            let self = this
            self.populateUniqueTeams()
        },
        methods: {
            populateUniqueTeams () {
                let self = this
                self.matchIDs = []
                Object.keys(self.$select('matches').matches).forEach(function (key) {
                    let match = self.$select('matches').matches[key]
                    if (match.eventName === self.eventName && match.matchNumber === self.matchNumber) {
                        self.matchIDs.push(match.matchID)
                    }
                })
            }
        },
        data () {
            return {
                eventName: this.$route.params.eventName,
                matchNumber: parseInt(this.$route.params.matchNumber),
                matchIDs: []
            }
        }
    }
</script>
