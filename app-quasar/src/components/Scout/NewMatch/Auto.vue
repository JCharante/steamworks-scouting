<template>
    <div>
        <div class="layout-padding">
            <div class="list">
                <div class="list-label">Autonomous Info</div>

                <div class="item two-lines">
                    <div class="item-content">
                        <span class="item-label">kPa: </span>
                        <q-numeric v-model="match.akPa" :min="0"></q-numeric>
                    </div>
                </div>

                <label class="item">
                    <div class="item-primary">
                        <q-checkbox v-model="match.aCrossedLine"></q-checkbox>
                    </div>
                    <div class="item-content">
                        Crossed Line
                    </div>
                </label>

                <label class="item">
                    <div class="item-primary">
                        <q-checkbox v-model="match.aDumpedHopper"></q-checkbox>
                    </div>
                    <div class="item-content">
                        Dumped Hopper
                    </div>
                </label>

                <label class="item">
                    <div class="item-primary">
                        <q-checkbox v-model="match.aCollectedFromHopper"></q-checkbox>
                    </div>
                    <div class="item-content">
                        Collected from Hopper
                    </div>
                </label>

                <label class="item">
                    <div class="item-primary">
                        <q-checkbox v-model="match.aLowGoal"></q-checkbox>
                    </div>
                    <div class="item-content">
                        Low Goal
                    </div>
                </label>

                <div class="item two-lines">
                    <div class="item-content row items-center">
                        <label style="margin-right: 10px;">Gear Position:</label>
                        <br>
                        <q-select class="full-width" type="radio" v-model="match.aGearPosition" :options="selectOptions.aGearPosition"></q-select>
                    </div>
                </div>

                <label class="item">
                    <div class="item-primary">
                        <q-checkbox v-model="match.aSuccessfulGearPlacement"></q-checkbox>
                    </div>
                    <div class="item-content">
                        Successful Gear Placement
                    </div>
                </label>

                <div class="item two-lines">
                    <div class="item-content row items-center">
                        <label style="margin-right: 10px;">High Goal Position:</label>
                        <br>
                        <q-select class="full-width" type="radio" v-model="match.aHighGoalShotFrom" :options="selectOptions.aHighGoalShotFrom"></q-select>
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
            console.info('%cAuto: %cMounted with router prop matchID = %O', 'color: blue', 'color: black', self.$route.params.matchID)
            let fetchedMatch = matchActions.fetchMatch(self.$select('matches'), self.$route.params.matchID)
            console.info('%cAuto: %cfetchedMatch = %O', 'color: blue', 'color: black', fetchedMatch)
            if (fetchedMatch === undefined) {
                console.info('%cAuto: %cCouldn\'t find match in store. Redirecting to create new match', 'color: blue', 'color: red')
                self.$router.push('/scout/new')
            }
            else {
                console.info('%cAuto: %cLoading match data from Redux Store', 'color: blue', 'color: green')
                self.match = Object.assign({}, self.match, fetchedMatch)
            }
        },
        beforeDestroy () {
            let self = this
            self.saveChangesInRedux()
            matchActions.saveStoreToLocalStorage(self.$select('matches'))
        },
        methods: {
            saveChangesInRedux () {
                let self = this
                let fetchedMatch = matchActions.fetchMatch(self.$select('matches'), self.$route.params.matchID)
                if (fetchedMatch !== undefined) {
                    console.info('%cAuto: %cSaving to Redux Store', 'color: blue', 'color: black')
                    store.dispatch(matchActions.updateMatch(self.match.matchID, self.match))
                }
            }
        },
        data () {
            return {
                match: {
                    /*
                    Autonomous Information is prefixed with a
                     */
                    akPa: 0,
                    aCrossedLine: false,
                    aDumpedHopper: false,
                    aCollectedFromHopper: false,
                    aLowGoal: false,
                    aGearPosition: null,
                    aSuccessfulGearPlacement: false,
                    aHighGoalShotFrom: null
                },
                selectOptions: {
                    aGearPosition: [
                        {label: 'None', value: null},
                        {label: 'Left', value: 'left'},
                        {label: 'Middle', value: 'middle'},
                        {label: 'Right', value: 'right'}
                    ],
                    aHighGoalShotFrom: [
                        {label: 'None', value: null},
                        {label: 'Key', value: 'key'},
                        {label: 'Wall', value: 'wall'},
                        {label: 'Afar', value: 'afar'}
                    ]
                }
            }
        }
    }
</script>
