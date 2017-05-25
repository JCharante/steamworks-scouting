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
    import store from '../../../store.js'
    import * as matchActions from '../../../actions/matches.js'

    export default {
        mounted () {
            let self = this
            console.log('PreMatch: Mounted with router prop matchID =', self.$route.params.matchID)
            let fetchedMatch = matchActions.fetchMatch(self.$select('matches'), self.$route.params.matchID)
            console.log('PreMatch: fetchedMatch', fetchedMatch)
            if (fetchedMatch === undefined) {
                console.log('PreMatch: Couldn\'t find match in store. Redirecting to create new match')
                self.$router.push('/scout/new')
            }
            else {
                console.log('PreMatch: Loading match data from Redux Store')
                self.match = Object.assign({}, self.match, fetchedMatch)
            }
        },
        beforeDestroy () {
            let self = this
            self.saveChangesInRedux()
        },
        methods: {
            saveChangesInRedux () {
                let self = this
                let fetchedMatch = matchActions.fetchMatch(self.$select('matches'), self.$route.params.matchID)
                if (fetchedMatch !== undefined) {
                    console.log('PreMatch: Saving to Redux Store')
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
                    eventName: [
                        {label: 'Practice', value: 'practice'},
                        {label: 'Granite State', value: 'granite-state'},
                        {label: 'Greater Boston', value: 'greator-boston'},
                        {label: 'Pine Tree', value: 'pine-tree'},
                        {label: 'Carson @ STL!', value: '2017cars'},
                        {label: 'Mayhem in Merrimack', value: '2017nhmm'},
                        {label: 'Beantown Blitz', value: '2017bt'},
                        {label: 'Summer Heat', value: '2017mesh'},
                        {label: 'Apple Town Smackdown', value: '2017apple'}
                    ]
                }
            }
        }
    }
</script>
