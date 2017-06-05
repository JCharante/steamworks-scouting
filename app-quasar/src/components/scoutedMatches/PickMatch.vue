<template>
    <div>
        <DrawerHead slot="header" :title="`${eventName} - Pick Match`" :backUrl="'/scout/view'" @openDrawerBody="$refs.drawer.$refs.drawer.open()"></DrawerHead>
        <DrawerBody ref="drawer"></DrawerBody>
        <div class="layout-padding">
            <div class="list">
                <ListItemMatch v-for="matchNumber in matchNumbers" :matchNumber="matchNumber" :eventName="eventName" :key="matchNumber"></ListItemMatch>
            </div>
        </div>
    </div>
</template>

<script>
    import DrawerHead from '../DrawerHead.vue'
    import DrawerBody from '../DrawerBody.vue'
    import ListItemMatch from './ListItemMatch.vue'
    import '../../store.js'

    export default {
        components: {
            'DrawerHead': DrawerHead,
            'DrawerBody': DrawerBody,
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
