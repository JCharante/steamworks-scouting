<template>
    <div>
        <div class="layout-padding">
            <div class="list">
                <div class="list-label">Pre Match Information</div>

                <div class="item two-lines">
                    <i class="item-primary">business</i>
                    <div class="item-content row items-center">
                        <label style="margin-right: 10px;">Event:</label>
                        <br>
                        <q-select class="full-width" type="radio" v-model="match.eventName" :options="selectOptions.eventName"></q-select>
                    </div>
                </div>

                <div class="item multiple-lines">
                    <i class="item-primary">label</i>
                    <div class="item-content row items-center">
                        <div class="stacked-label">
                            <input class="full-width" v-model.number="match.matchNumber" type="number">
                            <label>Qualification Match Number:</label>
                        </div>
                    </div>
                </div>


                <div class="item two-lines">
                    <i class="item-primary">perm_identity</i>
                    <div class="item-content row items-center wrap">
                        <div style="margin-right: 10px;" class="item-label">Team:</div>
                        <input class="auto" v-model.number="match.teamNumber" type="number">
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
    import { Dialog } from 'quasar'
    import store from '../../store.js'
    import { events } from '../../statics/js/events.js'
    import * as matchActions from '../../actions/matches.js'

    export default {
        mounted () {
            let self = this
            console.info('%cPreMatch: %cMounted with router prop matchID = %O', 'color: blue', 'color: black', self.$route.params.matchID)
            let fetchedMatch = matchActions.fetchMatch(self.$select('matches'), self.$route.params.matchID)
            console.info('%cPreMatch: %cfetchedMatch = %O', 'color: blue', 'color: black', fetchedMatch)
            if (fetchedMatch === undefined) {
                console.info('%cPreMatch: %cCouldn\'t find match in store. Redirecting to create new match', 'color: blue', 'color: red')
                self.$router.push('/scout/new')
            }
            else {
                console.info('%cPreMatch: %cLoading match data from Redux Store', 'color: blue', 'color: green')
                self.match = Object.assign({}, self.match, fetchedMatch)
            }
        },
        beforeDestroy () {
            let self = this
            if ((self.match.eventName === null || self.match.eventName === '') || (self.match.matchNumber === '' || self.match.matchNumber === null) || (self.match.teamNumber === '' || self.match.teamNumber === null)) {
                Dialog.create({
                    title: 'Attention',
                    message: 'When leaving the event name, match number, or team number empty the match will be deleted on exit by the rubbish collector'
                })
            }
            self.saveChangesInRedux()
            matchActions.saveStoreToLocalStorage(self.$select('matches'))
        },
        methods: {
            saveChangesInRedux () {
                let self = this
                let fetchedMatch = matchActions.fetchMatch(self.$select('matches'), self.$route.params.matchID)
                if (fetchedMatch !== undefined) {
                    console.info('%cPreMatch: %cSaving to Redux Store', 'color: blue', 'color: black')
                    store.dispatch(matchActions.updateMatch(self.match.matchID, self.match))
                }
            }
        },
        data () {
            return {
                store: store,
                matches: this.$select('matches'),
                match: {
                    matchID: null,
                    eventName: null,
                    matchNumber: null,
                    teamNumber: null
                },
                selectOptions: {
                    eventName: events
                }
            }
        }
    }
</script>
