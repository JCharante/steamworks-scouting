<template>
    <div>
        <div class="layout-padding">
            <div class="list">
                <div class="list-label">Aftermatch Info</div>

                <label class="item">
                    <div class="item-primary">
                        <q-checkbox v-model="match.attemptedClimb"></q-checkbox>
                    </div>
                    <div class="item-content">
                        Attempted to Climb
                    </div>
                </label>

                <label class="item">
                    <div class="item-primary">
                        <q-checkbox v-model="match.successfullyClimbed"></q-checkbox>
                    </div>
                    <div class="item-content">
                        Successfully Climbed
                    </div>
                </label>

                <div class="item two-lines">
                    <div class="item-content row items-center">
                        <label style="margin-right: 10px;">Gear Rating:</label>
                        <br>
                        <q-select class="full-width" type="radio" v-model="match.gearRating" :options="selectOptions.gearRating"></q-select>
                    </div>
                </div>

                <div class="item two-lines">
                    <div class="item-content row items-center">
                        <label style="margin-right: 10px;">Low Goal Rating:</label>
                        <br>
                        <q-select class="full-width" type="radio" v-model="match.lowGoalRating" :options="selectOptions.lowGoalRating"></q-select>
                    </div>
                </div>

                <div class="item two-lines">
                    <div class="item-content row items-center">
                        <label style="margin-right: 10px;">High Goal Rating:</label>
                        <br>
                        <q-select class="full-width" type="radio" v-model="match.highGoalRating" :options="selectOptions.highGoalRating"></q-select>
                    </div>
                </div>

                <div class="item multiple-lines">
                    <div class="item-content">
                        <div class="stacked-label" ref="noteDiv">
                            <textarea class="full-width" :class="{'has-error': match.notes.length > 200}" v-model="match.notes"></textarea>
                            <label>Notes ({{ 200 - match.notes.length }} chars remaining)</label>
                        </div>
                    </div>
                </div>

            </div>

            <br>

            <div class="row justify-center">
                <q-knob size="18rem" @input="updateKnobColor" :color="knobColor" v-model="match.estimatedClimbTime" :min="0" :max="30" :placeholder="'Estimated Climb Time: ' + match.estimatedClimbTime + 's'"></q-knob>
            </div>


        </div>
    </div>
</template>

<script>
    export default {
        methods: {
            updateKnobColor: function () {
                let self = this

                if (self.match.estimatedClimbTime > 20) {
                    self.knobColor = '#db2828' // negative
                }
                else if (self.match.estimatedClimbTime > 16) {
                    self.knobColor = '#ff5722' // deep-orange
                }
                else if (self.match.estimatedClimbTime > 14) {
                    self.knobColor = '#ff9800' // orange
                }
                else if (self.match.estimatedClimbTime > 12) {
                    self.knobColor = '#ffc107' // amber
                }
                else if (self.match.estimatedClimbTime > 10) {
                    self.knobColor = '#f2c037' // warning
                }
                else if (self.match.estimatedClimbTime > 8) {
                    self.knobColor = '#cddc39' // lime
                }
                else if (self.match.estimatedClimbTime > 5) {
                    self.knobColor = '#8bc34a' // light-green
                }
                else {
                    self.knobColor = '#21ba45' // positive
                }
            }
        },
        data () {
            return {
                knobColor: '#21ba45', // positive
                match: {
                    gearDispenseMethod: null,
                    gearRating: null,
                    lowGoalRating: null,
                    highGoalRating: null,
                    notes: '',
                    attemptedClimb: false,
                    successfullyClimbed: false,
                    estimatedClimbTime: 0
                },
                selectOptions: {
                    gearDispenseMethod: [
                        {label: 'Non-existent', value: null},
                        {label: 'Passive', value: 'passive'},
                        {label: 'Active', value: 'active'}
                    ],
                    gearRating: [
                        {label: 'Bad', value: 'bad'},
                        {label: 'Okay', value: 'okay'},
                        {label: 'Good', value: 'good'}
                    ],
                    lowGoalRating: [
                        {label: 'Didn\'t Shoot', value: 'ds'},
                        {label: 'Bad', value: 'bad'},
                        {label: 'Okay', value: 'okay'},
                        {label: 'Good', value: 'good'}
                    ],
                    highGoalRating: [
                        {label: 'Didn\'t Shoot', value: 'ds'},
                        {label: 'Bad', value: 'bad'},
                        {label: 'Okay', value: 'okay'},
                        {label: 'Good', value: 'good'}
                    ]
                }
            }
        }
    }
</script>
