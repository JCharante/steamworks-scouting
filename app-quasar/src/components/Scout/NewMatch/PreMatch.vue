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
    export default {
        data () {
            return {
                match: {
                    eventName: 'practice',
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
                        {label: 'Summer Heat', value: '2017mesh'}
                    ]
                }
            }
        }
    }
</script>
