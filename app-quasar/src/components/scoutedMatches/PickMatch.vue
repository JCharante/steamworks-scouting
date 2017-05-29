<template>
    <div class="layout-padding">
        <div class="list">
            <ListItemMatch v-for="matchNumber in matchNumbers" :matchNumber="matchNumber" :eventName="eventName" :key="matchNumber"></ListItemMatch>
        </div>
    </div>
</template>

<script>
    import ListItemMatch from './ListItemMatch.vue'
    import '../../store.js'

    export default {
        components: {
            'ListItemMatch': ListItemMatch
        },
        mounted () {
            let self = this
            self.populateUniqueMatches()
        },
        methods: {
            populateUniqueMatches () {
                let self = this
                let set = new Set()
                Object.keys(self.allMatches.matches).forEach(function (key) {
                    let match = self.allMatches.matches[key]
                    if (match.eventName === self.eventName) {
                        set.add(match.matchNumber)
                    }
                })
                self.matchNumbers = Array.from(set)
            }
        },
        data () {
            return {
                allMatches: this.$select('matches'),
                eventName: this.$route.params.eventName,
                matchNumbers: []
            }
        }
    }
</script>
