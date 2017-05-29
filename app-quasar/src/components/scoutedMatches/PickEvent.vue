<template>
    <div class="layout-padding">
        <div class="list">
            <ListItemEvent v-for="event in events" :eventName="event" :key="event"></ListItemEvent>
        </div>
    </div>
</template>

<script>
    import ListItemEvent from './ListItemEvent.vue'
    import '../../store.js'

    export default {
        components: {
            'ListItemEvent': ListItemEvent
        },
        mounted () {
            let self = this
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
